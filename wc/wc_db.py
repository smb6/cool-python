# wechat_db.py
from __future__ import annotations
import sqlite3, zlib, xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Iterable, Iterator, Tuple, Optional


def _maybe_decompress(blob: bytes) -> bytes:
    """Transparent zlib-inflate if needed."""
    if blob[:1] == b"x":
        try:
            return zlib.decompress(blob)
        except zlib.error:
            pass
    return blob


def _parse_chatroom_xml(xml_blob: Optional[bytes]) -> List[str]:
    if not xml_blob:
        return []
    try:
        root = ET.fromstring(xml_blob.decode("utf-8", "ignore"))
        return [m.get("userName") for m in root.findall(".//Member") if m.get("userName")]
    except ET.ParseError:
        return []


class WeChatSQLite:
    """Low-level helper for *decrypted* WeChat 8.x backup databases."""
    def __init__(self, db_folder: Path):
        self.root = Path(db_folder)

    # ---------- contacts ----------
    def load_contacts(self) -> Dict[str, List[str]]:
        """Returns {chat_id: [member wxids]}. Plain chats map to []."""
        out: Dict[str, List[str]] = {}
        db = sqlite3.connect(self.root / "WCDB_Contact.sqlite")
        db.execute("PRAGMA key=''")                     # plain-key backup
        for uid, room_xml in db.execute(
                "SELECT userName, dbContactChatRoom FROM Friend"):
            out[uid] = _parse_chatroom_xml(room_xml) if uid.endswith("@chatroom") else []
        return out

    # ---------- messages ----------
    def iter_shards(self) -> Iterable[Path]:
        """Yields every message_*.sqlite path found under the folder."""
        return self.root.glob("message_*.sqlite")

    def iter_chat_tables(self, shard_path: Path) -> Iterator[Tuple[str, sqlite3.Connection]]:
        """Yield (chat_id, db_handle) pairs for each Chat_<id> table in a shard."""
        db = sqlite3.connect(shard_path)
        db.text_factory = bytes
        db.execute("PRAGMA key=''")
        for (tbl,) in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Chat_%'"):
            yield tbl[5:], db                           # strip "Chat_"

    def messages(self, types: Tuple[int, ...] = (1,)) -> Iterator[Tuple[str, dict]]:
        """
        Yields (chat_id, raw_msg_dict).

        raw_msg_dict has keys:
            mid, sender_flag (0=rx,1=tx), ts, mtype, body_bytes
        """
        for shard in self.iter_shards():
            for chat_id, db in self.iter_chat_tables(shard):
                q = (f"SELECT MesLocalID, Des, CreateTime, Type, Message "
                     f"FROM Chat_{chat_id} WHERE Type IN ({','.join(map(str, types))})")
                for mid, des, ts, tp, body in db.execute(q):
                    yield chat_id, dict(mid=mid, sender_flag=des, ts=ts,
                                        mtype=tp, body=_maybe_decompress(body))
