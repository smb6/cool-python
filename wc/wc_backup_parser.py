# wechat_backup_parser.py
from __future__ import annotations
import sqlite3, zlib, xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional
from pydantic import BaseModel


# ---------- Pydantic models ----------
class Message(BaseModel):
    msg_id: int
    sender: str
    timestamp: int          # seconds since epoch (UTC)
    mtype: int
    body: str               # utf-8 text (for Type 1) or raw XML/hex

class Chat(BaseModel):
    chat_id: str                    # userName / roomID
    members: List[str] = []         # wxid list
    messages: List[Message] = []

    def add(self, m: Message) -> None:
        self.messages.append(m)


# ---------- Helpers ----------
def _maybe_decompress(blob: bytes) -> bytes:
    """WeChat compresses long text bodies with zlib (0x78 0x9C header)."""
    if blob and blob[:1] == b"x":
        try:
            return zlib.decompress(blob)
        except zlib.error:
            pass
    return blob


def _decode_text(b: bytes) -> str:
    return _maybe_decompress(b).decode("utf-8", errors="replace").replace("\x02", "")


def _parse_chatroom_xml(xml_blob: Optional[bytes]) -> List[str]:
    if not xml_blob:
        return []
    try:
        root = ET.fromstring(xml_blob.decode("utf-8", "ignore"))
        return [m.get("userName") for m in root.findall(".//Member") if m.get("userName")]
    except ET.ParseError:
        return []


# ---------- Core extractor ----------
def load_wechat_backup(db_folder: Path) -> Dict[str, Chat]:
    """
    :param db_folder: path that contains WCDB_Contact.sqlite and message_*.sqlite
                      e.g. .../Documents/<md5(wxid)>/DB
    :return: dict keyed by chat_id
    """
    chats: Dict[str, Chat] = {}

    # 1) Contacts & group membership -----------------
    contact_db = sqlite3.connect(db_folder / "WCDB_Contact.sqlite")
    contact_db.execute("PRAGMA key=''")           # empty key for backups
    for row in contact_db.execute(
            "SELECT userName, dbContactChatRoom FROM Friend"):
        uid, room_xml = row
        chat = chats.setdefault(uid, Chat(chat_id=uid))
        if uid.endswith("@chatroom"):
            chat.members = _parse_chatroom_xml(room_xml)

    # 2) Iterate every shard -------------------------
    for shard_path in db_folder.glob("message_*.sqlite"):
        db = sqlite3.connect(shard_path)
        db.text_factory = bytes                 # raw blobs
        db.execute("PRAGMA key=''")

        # list all Chat_ tables in this shard
        for (tbl,) in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Chat_%'"):
            chat_id = tbl[5:]                   # strip "Chat_"
            chat = chats.setdefault(chat_id, Chat(chat_id=chat_id))

            # pull messages (you can window / paginate here)
            for mid, svr, ts, body, status, img, mtype, des in db.execute(
                    f"SELECT MesLocalID, MesSvrID, CreateTime, Message,"
                    f"       Status, ImgStatus, Type, Des "
                    f"FROM {tbl} ORDER BY MesLocalID"):
                if mtype == 1:
                    body_text = _decode_text(body)
                else:
                    body_text = body.hex()      # keep non-text as hex

                msg = Message(
                    msg_id=svr or mid,
                    sender=chat_id if des else "me",  # quick heuristic
                    timestamp=ts,
                    mtype=mtype,
                    body=body_text
                )
                chat.add(msg)

    # 3) Sort messages per chat (optional)
    for c in chats.values():
        c.messages.sort(key=lambda m: m.timestamp)

    return chats


# ---------- CLI runner ----------
if __name__ == "__main__":
    import json, sys
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    data = load_wechat_backup(root)
    # pretty-print summary
    for cid, chat in data.items():
        print(f"{cid} – {len(chat.members)} members – {len(chat.messages)} msgs")
    # dump to JSON if wanted
    # Path("wechat_backup.json").write_text(json.dumps(data, default=lambda o: o.dict(), ensure_ascii=False, indent=2))
