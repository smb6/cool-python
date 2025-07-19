# chat_builder.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, List
from pydantic import BaseModel
from wc_db import WeChatSQLite


class Message(BaseModel):
    msg_id: int
    timestamp: int
    is_outgoing: bool
    mtype: int
    text: str


class Chat(BaseModel):
    chat_id: str
    members: List[str] = []
    messages: List[Message] = []

    def add(self, msg: Message):
        self.messages.append(msg)


def build_chats(db_folder: Path) -> Dict[str, Chat]:
    db = WeChatSQLite(db_folder)

    # 1) basic roster --------------------------------------------------
    chats: Dict[str, Chat] = {cid: Chat(chat_id=cid, members=mem)
                              for cid, mem in db.load_contacts().items()}

    # 2) messages (text only for brevity) ------------------------------
    for cid, raw in db.messages(types=(1,)):
        chat = chats.setdefault(cid, Chat(chat_id=cid))
        chat.add(Message(
            msg_id=raw["mid"],
            timestamp=raw["ts"],
            is_outgoing=bool(raw["sender_flag"]),
            mtype=raw["mtype"],
            text=raw["body"].decode("utf-8", "replace").replace("\x02", "")
        ))

    # 3) final tidy – sort by time ------------------------------------
    for c in chats.values():
        c.messages.sort(key=lambda m: m.timestamp)

    return chats


# ------------- CLI entry point -------------
if __name__ == "__main__":
    import sys, json
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    result = build_chats(root)
    print(f"Loaded {len(result)} chats.")
    # Optional: dump to pretty JSON
    # print(json.dumps({k: v.dict() for k, v in result.items()},
    #                 ensure_ascii=False, indent=2))
