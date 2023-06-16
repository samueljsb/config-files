#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os.path
import subprocess
import uuid
import venv


def get_dir_path(dir_name: str | None) -> str:
    if dir_name:
        return f'/tmp/{dir_name}'
    else:
        uid = uuid.uuid4().hex[:5]
        return f'/tmp/tmpvenv-{uid}'


def make_tmp_dir(dir_path: str) -> None:
    os.mkdir(dir_path)


def create_virtual_env(dir_path: str) -> None:
    try:
        subprocess.run(('virtualenv', 'venv'), cwd=dir_path, capture_output=True)
    except FileNotFoundError:
        venv.create(os.path.join(dir_path, 'venv'), with_pip=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description='create a virtual environment in a directory in /tmp',
    )
    parser.add_argument('dir_name', nargs='?')
    # fmt: off
    parser.add_argument(
        '-p', '--packages', nargs='*',
        help='packages to install in the virtual environment',
    )
    # fmt: on
    args = parser.parse_args()

    dir_path = get_dir_path(args.dir_name)

    make_tmp_dir(dir_path)
    create_virtual_env(dir_path)
    if args.packages:
        subprocess.run(
            ('venv/bin/python', '-mpip', 'install', *args.packages),
            cwd=dir_path,
            capture_output=True,
        )

    print(dir_path)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
