# PYRCLONE

## Installation

From `github`

To install it via `pip`,

```bash
pip install git+https://github.com/taicaile/pyrclone

pip install --ignore-installed git+https://github.com/taicaile/pyrclone
```

or clone it first,

```bash
git clone https://github.com/taicaile/pyrclone.git
cd pyrclone
python setup.py install
```

To install specific version,

```bash
# replace the version `v0.1.0` as you expect,
pip install git+https://github.com/taicaile/pyrclone@v0.1.0
```

### Usage

```python
# settings.py
RCLONE_REMOTE="xxx"

# move
from pyrclone.move import RcloneMoveProducer
rclone_move = RcloneMoveProducer.from_settings({"RCLONE_REMOTE": "test"})
rclone_move.push("test.txt")
```
