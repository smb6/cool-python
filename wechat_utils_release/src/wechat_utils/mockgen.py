"""wechat_utils.mockgen – generate realistic mock iOS WeChat containers."""
from __future__ import annotations

import argparse
import random
import sqlite3
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple

from mimesis import Person, Text
from mimesis.enums import Gender

from ._helpers import md5_hex

# ───────────────────────── providers ───────────────────────── #
NOW = datetime.utcnow()
PERSON = Person("en")
TEXT = Text("en")


# ───────────────────────── tiny helpers ─────────────────────── #
def rand_ts(within_days: int) -> int:
    """Unix-epoch seconds somewhere in the last <within_days> days."""
    offset = random.randint(0, within_days * 86_400)
    return int((NOW - timedelta(seconds=offset)).timestamp())


def contacts_list(n: int) -> List[Tuple[str, str]]:
    """[(UsrName, Nickname), …]"""
    res = []
    for _ in range(n):
        usr = f"wxid_{uuid.uuid4().hex[:12]}"
        nick = PERSON.full_name(gender=random.choice([Gender.MALE, Gender.FEMALE]))
        res.append((usr, nick))
    return res


def random_body(tp: int) -> str:
    if tp == 1:  # text
        return TEXT.sentence() + random.choice([" 🙂", " 🤔", ""])
    if tp == 3:  # image placeholder
        return "<img src='qpic://123'/>"
    if tp == 34:  # voice placeholder
        return "<voice len='3s'/>"
    return "<media/>"


# ─────────────────────── schema helpers ─────────────────────── #
TEMPLATE_SQL = """
CREATE TABLE Chat(
  CreateTime INTEGER,
  Des        INTEGER,
  Type       INTEGER,
  Message    TEXT,
  MesLocalID INTEGER PRIMARY KEY AUTOINCREMENT
);
CREATE TABLE ChatExt2(
  MesLocalID INTEGER PRIMARY KEY,
  msgFlag    INTEGER DEFAULT 0,
  MsgSource  TEXT,
  MsgIdentify TEXT
);
"""


def make_slice(
    db_path: Path,
    contacts: List[Tuple[str, str]],
    msgs_each: int,
    slice_idx: int,
) -> None:
    """
    Build a single message_<n>.sqlite slice containing BOTH Chat_<hash>
    and ChatExt2_<hash> tables.
    """
    with sqlite3.connect(db_path) as con:
        con.executescript(TEMPLATE_SQL)

        for usr, _ in contacts:
            h = md5_hex(usr)
            chat = f"Chat_{h}"
            ext = f"ChatExt2_{h}"

            # clone template schemas
            con.execute(f"CREATE TABLE {chat} AS SELECT * FROM Chat  LIMIT 0;")
            con.execute(f"CREATE TABLE {ext}  AS SELECT * FROM ChatExt2 LIMIT 0;")

            for _ in range(msgs_each):
                tp = random.choice([1, 1, 1, 3, 34])  # mostly text
                body = random_body(tp)
                ts = rand_ts(10 + slice_idx * 5)      # stagger per slice
                des = random.randint(0, 1)

                cur = con.execute(
                    f"INSERT INTO {chat}(CreateTime,Des,Type,Message) "
                    "VALUES (?,?,?,?)",
                    (ts, des, tp, body),
                )
                mes_id = cur.lastrowid

                # matching row in ChatExt2_<hash>
                con.execute(
                    f"INSERT INTO {ext}(MesLocalID,msgFlag,MsgSource) "
                    "VALUES (?,?,?)",
                    (mes_id, 0, "<src>mockgen</src>"),
                )

        # ❶  remove the templates so only Chat_<hash> & ChatExt2_<hash> remain
        con.execute("DROP TABLE Chat;")
        con.execute("DROP TABLE ChatExt2;")
        con.commit()


# ────────────────── container-level builder ─────────────────── #
def build_container(
    root: Path,
    accounts: int,
    contacts_n: int,
    messages_n: int,
    slices_n: int,
) -> None:
    """
    Create a complete fake WeChat-for-iOS container under *root*.
    """
    docs = root / "AppDomain-com.tencent.xin" / "Documents"

    for _ in range(accounts):
        acc_dir = docs / uuid.uuid4().hex
        db_dir = acc_dir / "DB"
        db_dir.mkdir(parents=True, exist_ok=True)

        # minimal media folders
        for sub in ("Img", "Audio", "Video"):
            (acc_dir / sub).mkdir(exist_ok=True)

        # contacts
        contacts = contacts_list(contacts_n)
        with sqlite3.connect(db_dir / "WCDB_Contact.sqlite") as con:
            con.execute(
                "CREATE TABLE Friend(UsrName TEXT PRIMARY KEY, NickName TEXT, Alias TEXT);"
            )
            con.executemany(
                "INSERT INTO Friend VALUES (?,?,?)",
                [(u, n, "") for u, n in contacts],
            )

        # message slices
        for n in range(1, slices_n + 1):
            make_slice(
                db_dir / f"message_{n}.sqlite",
                contacts,
                messages_n,
                n,
            )


# ───────────────────────────── CLI ──────────────────────────── #
def cli() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a mock iOS WeChat backup with Chat & ChatExt2 tables"
    )
    parser.add_argument("dest", type=Path, help="Destination folder")
    parser.add_argument("--accounts", type=int, default=1)
    parser.add_argument("--contacts", type=int, default=5)
    parser.add_argument("--messages", type=int, default=20)
    parser.add_argument("--slices", type=int, default=2)
    args = parser.parse_args()

    build_container(
        args.dest,
        accounts=args.accounts,
        contacts_n=args.contacts,
        messages_n=args.messages,
        slices_n=args.slices,
    )
    print(f"✅ Mock WeChat backup written to: {args.dest.resolve()}")


if __name__ == "__main__":
    cli()
