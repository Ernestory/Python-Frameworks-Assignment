from importlib import import_module
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    mod = import_module('app')
    df = mod.load_data()
    print('Loaded df shape:', df.shape)
    print('Columns:', list(df.columns))
except Exception as e:
    print('ERROR:', e)
    raise
