
from pathlib import Path
from click.testing import CliRunner
import json, mockgen, wechat_dump

def test_dump(tmp_path:Path):
    container = tmp_path/'mock'
    mockgen.build(container, accounts=1, contacts=3, messages=10, slices=1)
    out = tmp_path/'dump.json'
    runner = CliRunner()
    res = runner.invoke(wechat_dump.cli, [str(container), '-o', str(out)])
    assert res.exit_code == 0
    data = json.loads(out.read_text())
    assert len(data) == 3
    for c in data:
        assert c['message_count'] > 0
