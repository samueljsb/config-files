#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os


def main() -> int:
    parser = argparse.ArgumentParser(
        description='set up aactivator',
    )
    parser.add_argument(
        'venv',
        nargs='?', default='venv',
        help='path to venv (default: %(default)s)',
    )
    args = parser.parse_args()

    activate_script = os.path.join(args.venv, 'bin', 'activate')
    os.symlink(activate_script, '.activate.sh')
    os.chmod('.activate.sh', 0o600)

    with open('.deactivate.sh', 'w') as fd:
        fd.write('deactivate\n')
    os.chmod('.deactivate.sh', 0o600)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
