
#!/usr/bin/env python3
"""wechat_dump.py – dump conversations to JSON."""
from __future__ import annotations
import json, sqlite3, hashlib, click
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, time, timezone
from pathlib import Path
from typing import List
md5_hex = lambda s: hashlib.md5(s.encode('utf-8')).hexdigest()
LOCAL_TZ = timezone.utc
def utc_iso(ts:int)->str: return datetime.utcfromtimestamp(ts).isoformat()+'Z'

@dataclass
class Message:
    timestamp:str; direction:str; msg_type:int; body:str; mes_local_id:int

@dataclass
class Conversation:
    account_uid:str; usrname:str; nickname:str; chat_type:str
    messages:List[Message]; first_ts:str; last_ts:str; message_count:int

def scan_accounts(root:Path)->List[Path]:
    res=[]
    for docs in root.rglob('Documents'):
        for uid in docs.iterdir():
            if (uid/'DB'/'WCDB_Contact.sqlite').is_file():
                res.append(uid)
    return res

def db_chain(db:Path)->List[Path]:
    mm=db/'MM.sqlite'
    slices=sorted(db.glob('message_*.sqlite'), key=lambda p:int(p.stem.split('_')[1]))
    return ([mm] if mm.exists() else [])+slices

def load_contacts(path:Path):
    m={}
    if path.exists():
        with sqlite3.connect(path) as con:
            for usr,nick,alias in con.execute('SELECT UsrName,NickName,Alias FROM Friend'):
                m[md5_hex(usr)]=(usr,nick or alias or '')
    return m

def list_chats(con):
    q="SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Chat_%' AND name NOT LIKE 'ChatExt2_%'"
    return [(n[5:], n) for (n,) in con.execute(q)]

def fetch(db:Path, tbl:str, tmin, tmax):
    clauses=[]; params=[]
    if tmin is not None: clauses.append('CreateTime>=?'); params.append(int(tmin))
    if tmax is not None: clauses.append('CreateTime<=?'); params.append(int(tmax))
    where=(' WHERE '+' AND '.join(clauses)) if clauses else ''
    sql=f'SELECT CreateTime,Des,Type,Message,MesLocalID FROM {tbl}{where}'
    msgs=[]
    with sqlite3.connect(db) as con:
        for ts,des,tp,body,mid in con.execute(sql, params):
            msgs.append(Message(utc_iso(ts), 'out' if des==1 else 'in', tp, body, mid))
    return msgs

def chat_kind(u:str)->str:
    if u.endswith('@chatroom'): return 'GRP'
    if u.startswith(('gh_','app')): return 'OA'
    return 'PP'

def build_window(frm, to, ld, lh):
    if ld is not None:
        mx=datetime.now(LOCAL_TZ); mn=mx-timedelta(days=ld)
    elif lh is not None:
        mx=datetime.now(LOCAL_TZ); mn=mx-timedelta(hours=lh)
    elif frm or to:
        def parse(s,end):
            if not s: return datetime.max.replace(tzinfo=LOCAL_TZ) if end else datetime.min.replace(tzinfo=LOCAL_TZ)
            if 'T' in s: return datetime.fromisoformat(s).replace(tzinfo=LOCAL_TZ)
            y,m,d=map(int,s.split('-')); t=time.max if end else time.min
            return datetime(y,m,d,t.hour,t.minute,t.second,tzinfo=LOCAL_TZ)
        mn=parse(frm,False); mx=parse(to,True)
    else:
        return None,None
    return mn.timestamp(), mx.timestamp()

@click.command()
@click.argument('root', type=click.Path(path_type=Path, exists=True))
@click.option('-o','--out-file', type=click.Path(path_type=Path), default='dump.json')
@click.option('--from-date'); click.option('--to-date')
@click.option('--last-days', type=int); click.option('--last-hours', type=int)
def cli(root:Path, out_file:Path, from_date,to_date,last_days,last_hours):
    if sum(x is not None for x in (last_days,last_hours))>1:
        raise click.UsageError('choose one of --last-days / --last-hours')
    if (last_days or last_hours) and (from_date or to_date):
        raise click.UsageError('relative and absolute windows cannot mix')
    tmin,tmax = build_window(from_date,to_date,last_days,last_hours)
    convs=[]
    for acc in scan_accounts(root):
        db = acc/'DB'
        contacts=load_contacts(db/'WCDB_Contact.sqlite')
        bucket={}
        for f in db_chain(db):
            with sqlite3.connect(f) as con:
                for h,tbl in list_chats(con):
                    bucket.setdefault(h, []).extend(fetch(f,tbl,tmin,tmax))
        for h,msgs in bucket.items():
            if not msgs: continue
            msgs.sort(key=lambda m:m.timestamp)
            usr,nick = contacts.get(h,('<unknown>',''))
            convs.append(Conversation(acc.name, usr, nick, chat_kind(usr),
                                      msgs, msgs[0].timestamp, msgs[-1].timestamp, len(msgs)))
    with open(out_file,'w',encoding='utf-8') as fh:
        json.dump([asdict(c) for c in convs], fh, ensure_ascii=False, indent=2)
    click.echo(f"{len(convs)} convs -> {out_file}")

if __name__=='__main__':
    cli()
