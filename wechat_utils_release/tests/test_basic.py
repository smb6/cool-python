from click.testing import CliRunner
from pathlib import Path
from wechat_utils.mockgen import gen
from wechat_utils.dump import cli as dump_cli
import json

def test_dump(tmp_path:Path):
    cont=tmp_path/'mock'
    gen(cont,1,3,5,1)
    out=tmp_path/'dump.json'
    runner=CliRunner()
    res=runner.invoke(dump_cli,[str(cont),'-o',str(out)])
    assert res.exit_code==0
    data=json.loads(out.read_text())
    assert len(data)==3
