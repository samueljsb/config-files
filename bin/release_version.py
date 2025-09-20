#!/usr/bin/env python3.13
from __future__ import annotations

import argparse
import datetime
import enum
import fileinput
import subprocess
from collections.abc import Sequence


def _update_files(version: str, date: datetime.date) -> None:
    for line in fileinput.input('pyproject.toml', inplace=True):
        if line.startswith('version = '):
            print(f'version = "{version}"')  # noqa: B907
        else:
            print(line, end='')

    for line in fileinput.input('CHANGELOG.md', inplace=True):
        print(line, end='')
        if line in ('## Unreleased\n', '## [Unreleased]\n'):
            print('')
            print(f'## [{version}] - {date.isoformat()}')


def _git(*args: str) -> None:
    subprocess.check_call(('git', *args))


def _gh(*args: str) -> None:
    subprocess.check_call(('gh', *args))


class Method(enum.Enum):
    COMMIT_AND_TAG = enum.auto()
    TAG_ONLY = enum.auto()
    PULL_REQUEST = enum.auto()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            'release a new version '
            'by updating pyproject.toml and CHANGELOG.md '
            'and pushing a commit/tag'
        ),
    )
    parser.add_argument('new_version')
    method_mutex = parser.add_argument_group('method').add_mutually_exclusive_group()
    method_mutex.set_defaults(method=Method.COMMIT_AND_TAG)
    method_mutex.add_argument(
        '--commit-and-tag',
        dest='method', action='store_const', const=Method.COMMIT_AND_TAG,
        help='change files, commit, tag, and push to the current branch (default)',
    )
    method_mutex.add_argument(
        '--tag-only',
        dest='method', action='store_const', const=Method.TAG_ONLY,
        help='create and push a tag for the version',
    )
    method_mutex.add_argument(
        '--pull-request', '--pr',
        dest='method', action='store_const', const=Method.PULL_REQUEST,
        help='change files and create a pull request',
    )
    args = parser.parse_args(argv)

    new_version: str = args.new_version
    method: Method = args.method

    commit_msg = f'v{new_version}'
    branch_name = f'version--{new_version}'
    tag = f'v{new_version}'

    if method is Method.TAG_ONLY:
        _git('tag', tag)
        _git('push', 'origin', 'HEAD', '--tags')
        return 0

    _update_files(new_version, datetime.date.today())
    _git('add', '-u')

    if method is Method.PULL_REQUEST:
        _git('switch', '--create', branch_name)
        _git('commit', '-m', commit_msg)
        _git('push', '--set-upstream', 'origin', branch_name)
        _gh('pr', 'create', '--fill', '--web', '--head', branch_name)
    elif method is Method.COMMIT_AND_TAG:
        _git('commit', '-m', commit_msg)
        _git('tag', tag)
        _git('push', 'origin', 'HEAD', '--tags')
    else:
        raise TypeError(method)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())


from unittest import mock  # noqa: E402

import pytest  # noqa: E402


@pytest.mark.parametrize('options', ([], ['--commit-and-tag']))
def test_commit_and_tag(options: list[str]) -> None:
    with (
        mock.patch(f'{__name__}._update_files', autospec=True),
        mock.patch.object(subprocess, 'check_call', autospec=True) as subprocess_,
    ):
        main([*options, '1.2.3'])

    assert subprocess_.call_args_list == [
        mock.call(('git', 'add', '-u')),
        mock.call(('git', 'commit', '-m', 'v1.2.3')),
        mock.call(('git', 'tag', 'v1.2.3')),
        mock.call(('git', 'push', 'origin', 'HEAD', '--tags')),
    ]


@pytest.mark.parametrize('options', (['--pull-request'], ['--pr']))
def test_pull_request(options: list[str]) -> None:
    with (
        mock.patch(f'{__name__}._update_files', autospec=True),
        mock.patch.object(subprocess, 'check_call', autospec=True) as subprocess_,
    ):
        main([*options, '1.2.3'])

    assert subprocess_.call_args_list == [
        mock.call(('git', 'add', '-u')),
        mock.call(('git', 'switch', '--create', 'version--1.2.3')),
        mock.call(('git', 'commit', '-m', 'v1.2.3')),
        mock.call(('git', 'push', '--set-upstream', 'origin', 'version--1.2.3')),
        mock.call(
            ('gh', 'pr', 'create', '--fill', '--web', '--head', 'version--1.2.3'),
        ),
    ]


def test_tag_only() -> None:
    with (
        mock.patch(f'{__name__}._update_files', autospec=True),
        mock.patch.object(subprocess, 'check_call', autospec=True) as subprocess_,
    ):
        main(['--tag-only', '1.2.3'])

    assert subprocess_.call_args_list == [
        mock.call(('git', 'tag', 'v1.2.3')),
        mock.call(('git', 'push', 'origin', 'HEAD', '--tags')),
    ]
