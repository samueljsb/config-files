######
# XDG
######

export XDG_DATA_HOME="$HOME/.local/share"
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_STATE_HOME="$HOME/.local/state"
export XDG_CACHE_HOME="$HOME/.cache"


############
# oh-my-zsh
############

export ZSH="$XDG_DATA_HOME/oh-my-zsh"
plugins=(
  colored-man-pages
)
export ZSH_DISABLE_COMPFIX=true
DISABLE_AUTO_UPDATE=true . "$ZSH/oh-my-zsh.sh"


##################
# zsh & oh-my-zsh
##################

export HISTFILE="$XDG_STATE_HOME"/zsh/history
HISTSIZE=10000
SAVEHIST=10000

setopt NO_BG_NICE  # don't nice background tasks
setopt NO_HUP
setopt NO_LIST_BEEP
setopt LOCAL_OPTIONS  # allow functions to have local options
setopt LOCAL_TRAPS  # allow functions to have local traps
setopt HIST_VERIFY
setopt SHARE_HISTORY  # share history between sessions ???
setopt EXTENDED_HISTORY  # add timestamps to history
setopt PROMPT_SUBST
setopt CORRECT
setopt COMPLETE_IN_WORD
setopt IGNORE_EOF

setopt APPEND_HISTORY  # adds history
setopt INC_APPEND_HISTORY SHARE_HISTORY  # adds history incrementally and share it across sessions
setopt HIST_IGNORE_ALL_DUPS  # don't record dupes in history
setopt HIST_REDUCE_BLANKS

bindkey '^[^[[D' backward-word
bindkey '^[^[[C' forward-word
bindkey '^[[5D' beginning-of-line
bindkey '^[[5C' end-of-line
bindkey '^[[3~' delete-char
bindkey '^?' backward-delete-char

# Better history
# Credits to https://coderwall.com/p/jpj_6q/zsh-better-history-searching-with-arrow-keys
autoload -U up-line-or-beginning-search
autoload -U down-line-or-beginning-search
zle -N up-line-or-beginning-search
zle -N down-line-or-beginning-search
bindkey "^[[A" up-line-or-beginning-search  # Up
bindkey "^[[B" down-line-or-beginning-search  # Down

. "$HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh"
. "$HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"

# Load fzf before atuin
# fzf binds its own history search to ctrl+r;
# atuin needs to run afterwards to override it.
if [ -x "$(command -v fzf)" ]; then
  eval "$(fzf --zsh)"
fi

if [ -x "$(command -v atuin)" ]; then
  eval "$(atuin init zsh --disable-up-arrow)"
fi


##########
# editors
##########

export VIMINIT='source ~/.config/vim/vimrc'

# Use this to re-build custom spelling files when they change.
alias ,mkspell='vim + "mkspell! $(echo -e $XDG_CONFIG_HOME/vim/spell/*.add)" +qall'

if [ -x "$(command -v hx)" ]; then
  export EDITOR=hx
  export VISUAL=hx
elif [ -x "$command -v vim}" ]; then
  export EDITOR=vim
  export VISUAL=vim
fi


######
# git
######

_git_main_branch () {
  git branch 2> /dev/null \
  | grep -o -m 1 \
    -e ' main$' \
    -e ' master$' \
  | xargs \
  || return
}

_git_main_branch_origin () {
    git rev-parse --abbrev-ref origin/HEAD | cut -d/ -f2-
}

alias gpp='git push --set-upstream origin $(git branch --show-current)'
alias glrbom='git pull --rebase origin master'

alias gcml='gcm && gl'
alias clb='clear; PAGER= git log $(_git_main_branch)..HEAD --oneline'

function co-author(){
  git log --author=$1 | grep -m 1 $1 | gsed 's/Author/Co-authored-by/'
}

# Aliases adapted from OMZ
alias ga='git add'
alias gb='git branch'
alias gbda='git branch --no-color --merged | command grep -vE "^([+*]|\s*$(_git_main_branch)\s*$)" | command xargs -r git branch -d 2>/dev/null'
alias gc='git commit'
alias gc!='git commit --amend'
alias gcn!='git commit --no-edit --amend'
alias gca='git commit --all'
alias gca!='git commit --all --amend'
alias gcan!='git commit --all --no-edit --amend'
alias gcm='git checkout $(_git_main_branch)'
alias gco='git checkout'
alias gcp='git cherry-pick'
alias gd='git diff'
alias gds='git diff --staged'
alias gfm='git fetch origin $(_git_main_branch_origin)'
alias gl='git pull'
alias glog='git log --oneline --decorate --graph'
alias gpf='git push --force-with-lease'
alias grb='git rebase'
alias grbc='git rebase --continue'
alias grbm='git rebase $(_git_main_branch)'
alias grbom='git rebase origin/$(_git_main_branch_origin)'
alias gst='git status'
alias gsw='git switch'
alias gswc='git switch -c'
alias gswm='git switch $(_git_main_branch)'

alias gwip='git add -A; git rm $(git ls-files --deleted) 2> /dev/null; git commit --no-verify --no-gpg-sign -m "--wip-- [skip ci]"'

alias git-branches="git branch --format='%(color:green)%(HEAD)%(color:reset) %(if)%(upstream)%(then)%(else)%(color:dim)%(end)%(refname:short)%(color:reset) %(color:blue)%(upstream:track)%(color:reset)'"


function _changed_files() {
git diff ORIG_HEAD HEAD --name-only --no-relative | grep --silent "$@"
}

# "Git refresh"
function grf() {
  git checkout "$(_git_main_branch)" || return
  git pull origin "$(_git_main_branch_origin)" || return
  gbda

  clear

  if _changed_files 'requirements'; then
    echo "\033[33mrequirements have changed\033[0m"
  fi
  if _changed_files '/migrations/' ; then
    echo "\033[33mmigrations have changed\033[0m"
  fi

  git-branches
}

function gfu(){
  preview_function='echo {} | cut -c -7 | xargs git show --no-patch --color=always'
  commit_sha="$(git log --pretty=format:"%h %s" --no-merges origin/HEAD.. | fzf --preview=$preview_function --preview-window='up' | cut -c -7)"

  git commit --fixup "$commit_sha" $@
}

function gswf(){
  git branch --format='%(refname:short)' | fzf --select-1 --query="$@" | xargs git switch
}

function gaf(){
  git diff --name-only --no-relative | fzf --multi --query="$@" | xargs git -C "$(git rev-parse --show-toplevel)" add
}

# Create a new PR in the origin repo
function newpr() {
  currentBranch="$(git branch --show-current)"

  git push --set-upstream origin "$currentBranch" || return
  gh pr create --fill --web --head "$currentBranch"
}

# View a PR in the origin repo
alias viewpr='gh pr view --web'

# View files in the origin repo
function gh-file() {
  REPO_URL="$(gh repo view --json url --jq .url)"

  for file in "$@"; do
    open "$REPO_URL/blob/HEAD/$file"
  done
}

function gh-blame() {
  REPO_URL="$(gh repo view --json url --jq .url)"

  for file in "$@"; do
    open "$REPO_URL/blame/HEAD/$file"
  done
}

function pre-commit-changes() {
  git diff --relative --name-only | xargs pre-commit run $@ --files
}


#######
# Node
#######

export NPM_CONFIG_USERCONFIG="$XDG_CONFIG_HOME/npm/npmrc"
export NODE_REPL_HISTORY="$XDG_DATA_HOME/node/repl_history"

export PATH="$PATH:${XDG_DATA_HOME}/npm/bin"

if [ -x "$(command -v fnm)" ]; then
  eval "$(fnm env)"
fi


#########
# Python
#########

alias python=python3

export PYTHONSTARTUP="$XDG_CONFIG_HOME/python/startup.py"

export MYPY_CACHE_DIR="$XDG_CACHE_HOME/mypy"

export NOX_DEFAULT_VENV_BACKEND='uv|virtualenv'

export PIP_REQUIRE_VIRTUALENV=1

export PIPX_DEFAULT_PYTHON=python3.12
export PIPX_HOME="$XDG_STATE_HOME/pipx"
export PIPX_BIN_DIR="$HOME/.local/bin"

export VIRTUALENV_CONFIG_FILE="$XDG_CONFIG_HOME/virtualenv/virtualenv.ini"

if [ -x "$(command -v "$PIPX_BIN_DIR/aactivator")" ]; then
  eval "$("$PIPX_BIN_DIR/aactivator" init)"
fi

alias zen="python -c 'import this'"

alias tmpvenv='cd "$(mktmpvenv -p mypy rich)"; . venv/bin/activate'

# Kill mypy processes.
# Sometimes I end up with lots of concurrent mypy processes, which hog the CPU.
# This kills them all.
alias kill-mypy="ps -x | grep -E 'python[\d.]* -m mypy' | grep -v grep | tee /dev/stderr | awk '{print \$1}' | xargs kill -9"


#######
# Rust
#######

export RUSTUP_HOME="$XDG_DATA_HOME/rustup"

export CARGO_HOME="$XDG_DATA_HOME/cargo"
export PATH="$PATH:$CARGO_HOME/bin"


########
# misc.
########

alias reload!='. ~/.zshrc'

alias local-ip="ifconfig | grep 'inet ' | grep -v 127.0.0.1 | awk '{print \$2}'"

# ls & eza
export LSCOLORS=gxfxhxdxcxegedabagacad
if [ -x "$(command -v eza)" ]; then
  alias ll="eza --long --header --group"
  alias la="ll --all"
else
  alias ll='ls -lh'
  alias la='ls -lAh'
fi

# pager options
export LESS='-SRF --tabs=4'
export LESSHISTFILE="$XDG_CACHE_HOME"/less/history

if [ -x "$(command -v bat)" ]; then
  export PAGER='bat -p'
  export BAT_THEME='Visual Studio Dark+'
  # Disable gutter items and headers (makes it more like highlighted cat).
  export BAT_STYLE='snip'
fi

{% if one_password_agent %}
export SSH_AUTH_SOCK='{{ one_password_agent }}'
{% endif %}

if [ -x "$(command -v starship)" ]; then
  eval "$(starship init zsh)"
fi

# PostgreSQL
# CLI tools that come with the app.
export PATH="$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin"
export PSQL_HISTORY="$XDG_DATA_HOME/psql/history"

# Docker
export COLIMA_HOME="$XDG_CONFIG_HOME/colima"
export DOCKER_CONFIG="$XDG_CONFIG_HOME/docker"


{% if macos %}
########
# macOS
########

# Show/hide hidden files in the Finder
alias showfiles="defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder"
alias hidefiles="defaults write com.apple.finder AppleShowAllFiles -bool false && killall Finder"

# Prefer GNU tools over the MacOS BSD ones.
export PATH="$HOMEBREW_PREFIX/opt/findutils/libexec/gnubin:$HOMEBREW_PREFIX/opt/gawk/libexec/gnubin:$HOMEBREW_PREFIX/opt/gnu-sed/libexec/gnubin:$HOMEBREW_PREFIX/opt/grep/libexec/gnubin:$PATH"


{% endif %}
{% if kraken %}
################
# Work (Kraken)
################

# kraken-db-tools
export KRAKEN_CLIENT=oegb
export KRAKEN_DB_PG_CLIENT=pgcli
export KRAKEN_DB_CONCURRENCY=26
alias kdb=kraken-db

function all-dbs-count(){
  all-dbs --all "select count(1) from $@"
}


{% endif %}
#####

# Add user bin directory to PATH
export PATH="$HOME/.local/bin:$PATH"


######################
# Local customization
######################

LOCALRC="$XDG_CONFIG_HOME/zsh/local"
if [[ -a "$LOCALRC" ]]; then
  . "$LOCALRC"
fi
