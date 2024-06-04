import os
import shutil
import sys

import nox

HERE = os.path.dirname(__file__)
BIN = os.path.join(HERE, 'bin')

nox.options.sessions = ['write', 'write_bin']


@nox.session(python=False)
def bootstrap(session: nox.Session) -> None:
    """Bootstrap a new machine.

    Write config files and install all the packages I like to have available.
    """
    session.notify('write')
    session.notify('write_bin')
    session.notify('brew')
    session.notify('pipx')
    session.notify('npm')
    session.notify('vs_code')
    session.notify('macos')


@nox.session
def write(session: nox.Session) -> None:
    """Write config files."""
    session.install('write-config-files')
    session.run(
        'write-config-files', 'write', *session.posargs,
        '-t', os.path.join(HERE, 'templates.yaml'),
        '-c', os.path.join(HERE, 'context.yaml'),
    )


@nox.session
def diff(session: nox.Session) -> None:
    """Write config files."""
    session.install('write-config-files')

    options = session.posargs
    if shutil.which('diff-so-fancy'):
        options.append('-pdiff-so-fancy')

    session.run(
        'write-config-files', 'diff', *options,
        '-t', os.path.join(HERE, 'templates.yaml'),
        '-c', os.path.join(HERE, 'context.yaml'),
    )


@nox.session(python=False)
def write_bin(session: nox.Session) -> None:
    """Copy executables into person bin directory."""
    LOCAL_BIN = os.path.expanduser('~/.local/bin')
    os.makedirs(LOCAL_BIN, exist_ok=True)

    for program in os.listdir(BIN):
        src = os.path.join(BIN, program)
        if not os.path.isfile(src):
            continue

        if program.endswith('.py'):
            bin_name = program.replace('_', '-').removesuffix('.py')
            dest = os.path.join(LOCAL_BIN, bin_name)
        else:
            dest = os.path.join(LOCAL_BIN, program)

        shutil.copy(src, dest)
        session.log(f'installed {program} in {dest}')


@nox.session
def test_bin(session: nox.Session) -> None:
    """Run tests on Python executables."""
    session.install('pytest')

    python_scripts = [
        os.path.join(BIN, file)
        for file in os.listdir(BIN)
        if file.endswith('.py')
    ]
    session.run('pytest', *python_scripts)


BREW_PACKAGES = (
    'atuin',
    'bat',
    'eza',
    'fzf',
    'less',
    'pipx',
    'starship',
    'zsh',
    'zsh-autosuggestions',
    'zsh-syntax-highlighting',
    # git
    'diff-so-fancy',
    'gh',
    'git',
    'git-absorb',
    'gitui',
)
BREW_MACOS_PACKAGES = (
    'findutils',  # find, locate, updatedb, xargs
    'gawk',  # awk
    'gnu-sed',  # sed
    'grep',  # egrep, fgrep, grep
    'trash',
)


@nox.session(python=False)
def brew(session: nox.Session) -> None:
    """Install packages with Brew."""
    if not shutil.which('brew'):
        session.error('brew not installed')

    session.run('brew', 'analytics', 'off')
    session.run(
        'brew', 'install', *BREW_PACKAGES,
        env={'HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK': '1'},
    )
    if sys.platform == 'darwin':
        session.run(
            'brew', 'install', *BREW_MACOS_PACKAGES,
            env={'HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK': '1'},
        )


PIPX_PACKAGES = (
    'aactivator',
    'nox',
    'pgcli',
    'pre-commit',
    'tox',
    'twine',
    'virtualenv',
)


@nox.session(python=False)
def pipx(session: nox.Session) -> None:
    """Install packages with pipx."""
    if not shutil.which('pipx'):
        session.error('pipx not installed')

    for package in PIPX_PACKAGES:
        session.run('pipx', 'install', package)


VS_CODE_EXTENSIONS = (
        # VS Code
        'aaron-bond.better-comments',
        'alefragnani.Bookmarks',
        'artdiniz.quitcontrol-vscode',
        'byi8220.indented-block-highlighting',
        'EditorConfig.EditorConfig',
        'formulahendry.auto-close-tag',
        'mikestead.dotenv',
        'naumovs.color-highlight',
        'PKief.material-icon-theme',
        'stkb.rewrap',
        'swyphcosmo.spellchecker',
        # Git
        'codezombiech.gitignore',
        'fabiospampinato.vscode-open-in-github',
        'sidneys1.gitconfig',
        'waderyan.gitblame',
        # Python
        'charliermarsh.ruff',
        'lextudio.restructuredtext',
        'mgesbert.python-path',
        'ms-python.python',
        'ms-python.vscode-pylance',
        # Other
        'DavidAnson.vscode-markdownlint',
        'ms-azuretools.vscode-docker',
)


@nox.session(python=False)
def vs_code(session: nox.Session) -> None:
    """Install VS Code extensions."""
    if not shutil.which('code'):
        session.error('VS Code CLI not installed')

    for extension in VS_CODE_EXTENSIONS:
        session.run('code', '--install-extension', extension)


@nox.session(python=False)
def macos(session: nox.Session) -> None:
    """Set up macOS with my preferred defaults."""
    if sys.platform != 'darwin':
        session.skip('not macOS')

    session.run(os.path.join(HERE, 'macos-defaults.sh'))
