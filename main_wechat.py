#!/usr/bin/env python3
"""
wechat_export.py – walk an iOS WeChat backup and dump every conversation
Copyright 2025  •  MIT-licensed
"""

import hashlib
import csv
import sqlite3
from pathlib import Path
import shutil
import sys
import click

# ---------- helpers ---------------------------------------------------------

def md5_hex(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def find_accounts(backup_root: Path):
    """Yield every Documents/<uid>/ folder that looks like a WeChat account"""
    for p in (backup_root / "AppDomain-com.tencent.xin" / "Documents").glob("*"):
        if (p / "DB" / "WCDB_Contact.sqlite").is_file():
            yield p

def slice_dbs(db_dir: Path):
    """Return MM.sqlite + ordered message_n.sqlite paths"""
    mm = db_dir / "MM.sqlite"
    slices = sorted(db_dir.glob("message_*.sqlite"),
                    key=lambda fp: int(fp.stem.split("_")[1]))
    return [mm, *slices]

def list_contacts(contact_db: Path):
    q = ("SELECT UsrName, NickName, Alias "
         "FROM Friend WHERE UsrName IS NOT NULL")
    with sqlite3.connect(contact_db) as con:
        return con.execute(q).fetchall()

def export_messages(slice_paths, hash_, out_csv):
    rows = []
    for db in slice_paths:
        alias = db.stem            # mm / message_n
        with sqlite3.connect(db) as con:
            tbl = f"Chat_{hash_}"
            try:
                for r in con.execute(
                        f"SELECT CreateTime,Des,Type,Message,MesLocalID "
                        f"FROM {tbl}"):
                    rows.append((*r, alias))
            except sqlite3.OperationalError:
                pass  # slice doesn't contain that chat
    rows.sort(key=lambda r: r[0])  # by CreateTime
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(
            ["CreateTime","Direction","Type","Message","MesLocalID","Slice"])
        w.writerows(rows)
    return rows

MEDIA_MAP = {3: "Img",   # image
             34: "Audio", # voice
             43: "Video"} # video

def copy_media(account_root: Path, rows, dest_dir: Path):
    copied = 0
    for _, _, mtype, _, mid, _ in rows:
        sub = MEDIA_MAP.get(mtype)
        if not sub:
            continue
        src_dir = account_root / sub
        for ext in src_dir.glob(f"{mid}*"):
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ext, dest_dir / ext.name)
            copied += 1
    return copied

# ---------- CLI -------------------------------------------------------------

@click.group()
@click.option("--backup", "backup_root",
              type=click.Path(path_type=Path, exists=True, readable=True),
              required=True,
              help="Path to the un-encrypted iTunes/Finder backup root")
@click.pass_context
def cli(ctx, backup_root):
    """WeChat conversation dumper for *iOS* backups."""
    ctx.obj = {"backup_root": backup_root}

@cli.command("list")
@click.pass_context
def list_conversations(ctx):
    """Show every account and its conversations"""
    for acc in find_accounts(ctx.obj["backup_root"]):
        contact_db = acc / "DB" / "WCDB_Contact.sqlite"
        click.echo(f"\n📱 Account: {acc.name}")
        for usr, nick, alias in list_contacts(contact_db):
            click.echo(f"  • {usr:<35} | {nick or ''} {alias or ''}")

@cli.command("export-all")
@click.option("--out", "out_dir",
              type=click.Path(path_type=Path, writable=True),
              default="wechat_export",
              help="Destination folder (default: ./wechat_export)")
@click.pass_context
def export_all(ctx, out_dir):
    """Dump every conversation (+media) into OUT/"""
    backup_root = ctx.obj["backup_root"]
    out_dir = Path(out_dir)
    for acc in find_accounts(backup_root):
        acc_id = acc.name
        acc_out = out_dir / acc_id
        db_dir = acc / "DB"
        slices = slice_dbs(db_dir)
        contact_db = db_dir / "WCDB_Contact.sqlite"

        click.echo(f"\n🔍 Processing account {acc_id} …")
        for usr, nick, alias in list_contacts(contact_db):
            h = md5_hex(usr)
            conv_tag = nick or alias or usr
            click.echo(f"   • {conv_tag} … ", nl=False)

            rows = export_messages(slices, h,
                                   acc_out / f"{conv_tag}.csv")
            media_count = copy_media(acc, rows,
                                     acc_out / "media" / conv_tag)
            click.echo(f"{len(rows):5d} msgs, {media_count:4d} media")

    click.echo(f"\n✅ Finished. Outputs in {out_dir.resolve()}")

# ---------- main ------------------------------------------------------------
if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        sys.exit(130)
