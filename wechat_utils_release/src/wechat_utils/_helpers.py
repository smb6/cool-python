from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("Asia/Jerusalem")
md5_hex = lambda s: hashlib.md5(s.encode('utf-8')).hexdigest()
def utc_iso(ts:int)->str:
    return datetime.utcfromtimestamp(ts).isoformat()+'Z'
