"""Remove only the known local prototype DB after explicit development confirmation."""
import argparse
import os
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--confirm-prototype-reset',action='store_true');args=p.parse_args()
if os.environ.get('KER_ENV')!='development' or not args.confirm_prototype_reset:
    p.error('Set KER_ENV=development and pass --confirm-prototype-reset. Stop the server first.')
root=Path(__file__).resolve().parent.parent
folder=root/'data'
if folder.is_symlink():p.error('Refusing a symlink data directory.')
for name in ['prototype.sqlite3','prototype.sqlite3-wal','prototype.sqlite3-shm','prototype.sqlite3-journal']:
    target=folder/name
    if target.is_symlink():p.error('Refusing a symlink database.')
for name in ['prototype.sqlite3','prototype.sqlite3-wal','prototype.sqlite3-shm','prototype.sqlite3-journal']:
    (folder/name).unlink(missing_ok=True)
print('Development prototype DB reset. No other file was removed.')
