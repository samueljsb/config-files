#!/usr/bin/env python3.10
from __future__ import annotations

import argparse
import subprocess


def _git(*args: str) -> str:
    return subprocess.check_output(('git', *args), text=True)


def _parse_branches(lines: list[str], base_ref: str, remotes: list[str]) -> list[str]:
    branches = []

    for line in lines:
        refs = [ref.strip() for ref in line.removeprefix('HEAD -> ').split(',')]
        for ref in refs:
            if not ref:
                continue
            elif ref == base_ref:
                continue
            elif any(ref.startswith(f'{remote}/') for remote in remotes):
                continue
            else:
                branches.append(ref)

    return list(reversed(branches))


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            'Push a sequence of branches that correspond to a chain of PRs. '
            'This is useful to run immediately after a successful rebase '
            'with the `--update-refs` option.'
        ),
    )
    parser.add_argument('base_ref', nargs='?', default='main')
    parser.add_argument(
        '-f', '--force',
        action='store_const', dest='force_flag',
        const='--force', default='--force-with-lease',
        help="force push (default uses 'force-with-lease')",
    )
    args = parser.parse_args()

    remotes = _git('remote').split()
    log_lines = _git('log', f'{args.base_ref}..', '--format=format:%D').split('\n')

    branches = _parse_branches(log_lines, args.base_ref, remotes)
    _git('push', args.force_flag, '--atomic', 'origin', *branches)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())


def test_parse_branches_up_to_date() -> None:
    log_output = """\
HEAD -> my-test-2, origin/my-test-2


origin/my-test-1, my-test-1

origin/my-test-0, my-test-0
origin/main, origin/HEAD, main
"""
    assert _parse_branches(log_output.split('\n'), 'main', ['origin']) == [
        'my-test-0',
        'my-test-1',
        'my-test-2',
    ]


def test_parse_branches_behind() -> None:
    log_output = """\
HEAD -> my-test-2

my-test-1

my-test-0
"""
    assert _parse_branches(log_output.split('\n'), 'main', ['origin']) == [
        'my-test-0',
        'my-test-1',
        'my-test-2',
    ]
