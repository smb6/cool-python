
#!/usr/bin/env python3
"""mockgen.py – generate a mock iOS WeChat backup (Chat & ChatExt2 pairs)."""
from __future__ import annotations
import argparse, random, sqlite3, hashlib, uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple
from mimesis import Person, Text
from mimesis.enums import Gender

NOW = datetime.utcnow()
PERSON, TEXT = Person('en'), Text('en')
md5_hex = lambda s: hashlib.md5(s.encode('utf-8')).hexdigest()

def rand_ts(days:int)->int:
    return int((NOW - timedelta(seconds=random.randint(0, days*86400))).timestamp())

def contacts_list(n:int)->List[Tuple[str,str]]:
    res=[]
    for _ in range(n):
        usr=f'wxid_{uuid.uuid4().hex[:12]}'
        nick=PERSON.full_name(gender=random.choice([Gender.MALE, Gender.FEMALE]))
        res.append((usr,nick))
    return res

def random_body(tp:int)->str:
    if tp==1: return TEXT.sentence() + random.choice([' 🙂',' 🤔',''])
    if tp==3: return '<img/>'
    return '<voice/>'

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

def make_slice(path:Path, contacts, msgs_each:int, idx:int):
    with sqlite3.connect(path) as con:
        con.executescript(TEMPLATE_SQL)
        for usr,_ in contacts:
            h=md5_hex(usr)
            chat=f'Chat_{h}'
            ext=f'ChatExt2_{h}'
            con.execute(f'CREATE TABLE {chat} AS SELECT * FROM Chat LIMIT 0;')
            con.execute(f'CREATE TABLE {ext}  AS SELECT * FROM ChatExt2 LIMIT 0;')
            for _ in range(msgs_each):
                tp=random.choice([1,1,1,3,34])
                body=random_body(tp)
                ts=rand_ts(10+idx*5)
                des=random.randint(0,1)
                cur=con.execute(f'INSERT INTO {chat}(CreateTime,Des,Type,Message) VALUES (?,?,?,?)',
                                 (ts,des,tp,body))
                mes_id=cur.lastrowid
                con.execute(f'INSERT INTO {ext}(MesLocalID,msgFlag,MsgSource) VALUES (?,?,?)',
                            (mes_id,0,'<src>mockgen</src>'))
        con.execute('DROP TABLE Chat;')
        con.execute('DROP TABLE ChatExt2;')
        con.commit()

def build(dest:Path, accounts:int, contacts:int, messages:int, slices:int):
    docs = dest / 'AppDomain-com.tencent.xin' / 'Documents'
    for _ in range(accounts):
        acc = docs / uuid.uuid4().hex
        dbdir = acc / 'DB'
        dbdir.mkdir(parents=True, exist_ok=True)
        for sub in ('Img','Audio','Video'):
            (acc/sub).mkdir(exist_ok=True)
        cts = contacts_list(contacts)
        with sqlite3.connect(dbdir/'WCDB_Contact.sqlite') as con:
            con.execute('CREATE TABLE Friend(UsrName TEXT PRIMARY KEY, NickName TEXT, Alias TEXT);')
            con.executemany('INSERT INTO Friend VALUES (?,?,?)', [(u,n,'') for u,n in cts])
        for n in range(1, slices+1):
            make_slice(dbdir/f'message_{n}.sqlite', cts, messages, n)

def cli():
    ap=argparse.ArgumentParser()
    ap.add_argument('dest', type=Path)
    ap.add_argument('--accounts', type=int, default=1)
    ap.add_argument('--contacts', type=int, default=5)
    ap.add_argument('--messages', type=int, default=20)
    ap.add_argument('--slices', type=int, default=2)
    args=ap.parse_args()
    build(args.dest, args.accounts, args.contacts, args.messages, args.slices)
    print('✅ mock backup in', args.dest.resolve())

if __name__=='__main__':
    cli()
