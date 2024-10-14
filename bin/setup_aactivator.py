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
    parser.add_argument(
        '--git-exclude',
        action='store_true',
        help='add the aactivator scripts to the local git exclude file',
    )
    args = parser.parse_args()

    activate_script = os.path.join(args.venv, 'bin', 'activate')
    os.symlink(activate_script, '.activate.sh')
    os.chmod('.activate.sh', 0o600)

    with open('.deactivate.sh', 'w') as fd:
        fd.write('deactivate\n')
    os.chmod('.deactivate.sh', 0o600)

    if args.git_exclude:
        with open('.git/info/exclude', 'a') as fd:
            fd.write('.activate.sh\n')
            fd.write('.deactivate.sh\n')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
