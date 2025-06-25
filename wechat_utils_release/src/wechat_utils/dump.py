"""
wechat_utils.dump  –  export iOS WeChat backups to JSON
(no one-liner statements with “;”)
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, time, timezone
from pathlib import Path
from typing import List, Tuple

import click
from zoneinfo import ZoneInfo

from ._helpers import LOCAL_TZ, md5_hex, utc_iso

# ───────────────────────── dataclasses ──────────────────────────
@dataclass
class Message:
    timestamp: str
    direction: str               # "in" | "out"
    msg_type: int
    body: str
    mes_local_id: int


@dataclass
class Conversation:
    account_uid: str
    usrname: str
    nickname: str
    chat_type: str               # "PP" | "GRP" | "OA"
    messages: List[Message]
    first_ts: str
    last_ts: str
    message_count: int


# ───────────────────────── helpers ──────────────────────────────
def scan_accounts(root: Path) -> List[Path]:
    """Return every Documents/<uid>/ folder that has a DB/ directory."""
    accounts: List[Path] = []
    for docs in root.rglob("Documents"):
        for uid_dir in docs.iterdir():
            contact_db = uid_dir / "DB" / "WCDB_Contact.sqlite"
            if contact_db.is_file():
                accounts.append(uid_dir)
    return accounts


def db_chain(db_dir: Path) -> List[Path]:
    """Return [MM.sqlite] + ordered message_n.sqlite paths."""
    slices: List[Path] = sorted(
        db_dir.glob("message_*.sqlite"),
        key=lambda p: int(p.stem.split("_")[1]),
    )
    if (db_dir / "MM.sqlite").exists():
        return [db_dir / "MM.sqlite"] + slices
    return slices


def chat_kind(usr_name: str) -> str:
    if usr_name.endswith("@chatroom"):
        return "GRP"
    if usr_name.startswith(("gh_", "app")):
        return "OA"
    return "PP"


# ──────────────── time-window calculation ───────────────────────
def _parse_local_date(date_str: str, end_of_day: bool) -> datetime:
    """Parse YYYY-MM-DD or YYYY-MM-DDThh:mm into LOCAL_TZ datetime."""
    if "T" in date_str:
        return datetime.fromisoformat(date_str).replace(tzinfo=LOCAL_TZ)
    year, month, day = map(int, date_str.split("-"))
    t_val = time.max if end_of_day else time.min
    return datetime(year, month, day,
                    t_val.hour, t_val.minute, t_val.second,
                    tzinfo=LOCAL_TZ)


def build_window(
    from_str: str | None,
    to_str: str | None,
    last_days: int | None,
    last_hours: int | None,
) -> Tuple[float | None, float | None]:
    """Return (min_epoch_utc, max_epoch_utc) or (None, None)."""
    if last_days is not None:
        max_local = datetime.now(LOCAL_TZ)
        min_local = max_local - timedelta(days=last_days)
    elif last_hours is not None:
        max_local = datetime.now(LOCAL_TZ)
        min_local = max_local - timedelta(hours=last_hours)
    elif from_str or to_str:
        min_local = _parse_local_date(from_str, False) if from_str else datetime.min.replace(tzinfo=LOCAL_TZ)
        max_local = _parse_local_date(to_str, True)    if to_str   else datetime.max.replace(tzinfo=LOCAL_TZ)
    else:
        return None, None

    min_utc = min_local.astimezone(timezone.utc).timestamp()
    max_utc = max_local.astimezone(timezone.utc).timestamp()
    return min_utc, max_utc


# ──────────────── DB-level helpers ──────────────────────────────
def load_contacts(contact_db: Path) -> dict[str, Tuple[str, str]]:
    """Return MD5(UsrName) → (UsrName, Nick/Alias)."""
    mapping: dict[str, Tuple[str, str]] = {}
    if not contact_db.exists():
        return mapping

    with sqlite3.connect(contact_db) as con:
        rows = con.execute(
            "SELECT UsrName, NickName, Alias FROM Friend WHERE UsrName IS NOT NULL"
        )
        for usr, nick, alias in rows:
            mapping[md5_hex(usr)] = (usr, nick or alias or "")
    return mapping


def list_chat_tables(con: sqlite3.Connection) -> List[Tuple[str, str]]:
    sql = (
        "SELECT name FROM sqlite_master "
        "WHERE type='table' AND name LIKE 'Chat_%' "
        "AND name NOT LIKE 'ChatExt2_%'"
    )
    # return [(name[5:], name) for (name,) in con.execute(sql)]
    n = [(name[5:], name) for (name,) in con.execute(sql)]
    print(n)
    return n


def fetch_messages(
    db_path: Path,
    table: str,
    t_min: float | None,
    t_max: float | None,
) -> List[Message]:
    clauses: List[str] = []
    params: List[int] = []

    if t_min is not None:
        clauses.append("CreateTime >= ?")
        params.append(int(t_min))
    if t_max is not None:
        clauses.append("CreateTime <= ?")
        params.append(int(t_max))

    where = ""
    if clauses:
        where = " WHERE " + " AND ".join(clauses)

    sql = (
        f"SELECT CreateTime, Des, Type, Message, MesLocalID "
        f"FROM {table}{where}"
    )
    print(f"DEBUG - {table=}\n{where=}")
    messages: List[Message] = []
    with sqlite3.connect(db_path) as con:
        for ts, des, msg_type, body, mes_id in con.execute(sql, params):
            direction = "out" if des == 1 else "in"
            messages.append(
                Message(utc_iso(ts), direction, msg_type, body, mes_id)
            )
    return messages


# ─────────────── conversation builder ──────────────────────────
def build_conversations(
    acc_dir: Path,
    t_min: float | None,
    t_max: float | None,
) -> List[Conversation]:
    db_dir = acc_dir / "DB"
    contacts = load_contacts(db_dir / "WCDB_Contact.sqlite")

    bucket: dict[str, List[Message]] = {}

    for db_path in db_chain(db_dir):
        with sqlite3.connect(db_path) as con:
            for hash_id, chat_tbl in list_chat_tables(con):
                messages = fetch_messages(db_path, chat_tbl, t_min, t_max)
                if messages:
                    bucket.setdefault(hash_id, []).extend(messages)

    conversations: List[Conversation] = []
    for hash_id, msgs in bucket.items():
        msgs.sort(key=lambda m: m.timestamp)

        usr_name, nickname = contacts.get(hash_id, ("<unknown>", ""))
        first_ts = msgs[0].timestamp
        last_ts = msgs[-1].timestamp
        conversations.append(
            Conversation(
                account_uid=acc_dir.name,
                usrname=usr_name,
                nickname=nickname,
                chat_type=chat_kind(usr_name),
                messages=msgs,
                first_ts=first_ts,
                last_ts=last_ts,
                message_count=len(msgs),
            )
        )

    return conversations


# ─────────────────────────── CLI ───────────────────────────────
@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("root", type=click.Path(path_type=Path, exists=True))
@click.option("-o", "--out-file", type=click.Path(path_type=Path), default="dump.json")
@click.option("--from-date")
@click.option("--to-date")
@click.option("--last-days", type=int)
@click.option("--last-hours", type=int)
def cli(
    root: Path,
    out_file: Path,
    from_date: str | None,
    to_date: str | None,
    last_days: int | None,
    last_hours: int | None,
) -> None:
    """
    Export WeChat chats to JSON.

    • Use --last-hours or --last-days for relative windows.
    • Use --from-date / --to-date for absolute local-time windows.
    """
    relative_count = sum(
        item is not None for item in (last_days, last_hours)
    )
    if relative_count > 1:
        raise click.UsageError("--last-days and --last-hours are mutually exclusive")

    if relative_count and (from_date or to_date):
        raise click.UsageError("Relative and absolute windows cannot mix")

    t_min, t_max = build_window(from_date, to_date, last_days, last_hours)

    all_conversations: List[Conversation] = []
    for account in scan_accounts(root.expanduser().resolve()):
        all_conversations.extend(build_conversations(account, t_min, t_max))

    with open(out_file, "w", encoding="utf-8") as fh:
        json.dump([asdict(conv) for conv in all_conversations], fh,
                  ensure_ascii=False, indent=2)

    click.echo(f"✅ Dumped {len(all_conversations)} conversations to {out_file}")


if __name__ == "__main__":
    cli()
