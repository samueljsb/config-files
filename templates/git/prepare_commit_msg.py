#!/usr/bin/env python3
from __future__ import annotations

import os
import sys


def main() -> int:
    # get the co-author to add
    co_author = os.getenv('GIT_CO_AUTHOR')
    if not co_author:
        return 0
    co_author_trailer = f'Co-authored-by: {co_author}\n'

    # read the commit message
    filepath = sys.argv[1]
    with open(filepath) as f:
        message = f.readlines()

    if co_author_trailer in message:
        # already contains the line
        return 0

    # insert the line in the right section of the template
    try:
        idx = message.index('# Co-authored-by:\n')
    except ValueError:
        message.extend(['\n', co_author_trailer])
    else:
        message.insert(idx + 1, co_author_trailer)

    # write the message back
    with open(filepath, 'w') as f:
        f.writelines(message)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
