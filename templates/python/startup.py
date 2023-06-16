"""Python startup file.

See https://docs.python.org/3/using/cmdline.html#envvar-PYTHONSTARTUP
"""
# Modules I often want to have available
import datetime  # noqa: F401
from pprint import pprint as pp

# Use rich (https://rich.readthedocs.io/en/latest/introduction.html) to get
# prettier output in the REPL; if it isn't available, just use ``pprint``.
try:
    from rich import inspect as __inspect
    from rich import pretty as __pretty
except ImportError:
    inspect = pp
else:
    __pretty.install()

    def inspect(*args, **kwargs):
        # Custom rich.inspect wrapper to ensure methods are inspected by default.
        if 'methods' not in kwargs:
            kwargs['methods'] = True
        __inspect(*args, **kwargs)

# Print the commands that have been imported as a memory jogger.
print('>>> from pprint import pprint as pp')
print('>>> from rich import inspect')
print('>>> import datetime')

# Define aliases for true, false and null so JSON can be pasted straight in.
true = True
false = False
null = None
