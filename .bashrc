#
# ~/.bashrc
#

GOPATH=$HOME/go  PATH=$PATH:/usr/local/go/bin:$GOPATH/bin

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

export HISTCONTROL=ignoreboth:erasedups

# Make nvim the default editor
export EDITOR='nvim'
export VISUAL='nvim'


if [ -d "$HOME/.bin" ] ;
  then PATH="$HOME/.bin:$PATH"
fi

if [ -d "$HOME/.local/bin" ] ;
  then PATH="$HOME/.local/bin:$PATH"
fi

if [ -d "$HOME/scripts" ] ;
  then PATH="$HOME/scripts:$PATH"
fi

# add java to path
PATH="$PATH:$HOME/.jdks/openjdk-20.0.2/bin/"

# Add ruby to path
PATH="$PATH:/usr/share/gems:$HOME/.local/share/gem/ruby:/usr/local/share/gems"
PATH="$PATH:$HOME/.local/share/gem/ruby/3.3.0/bin"
PATH="$PATH:$HOME/bin/"
GEM_PATH="$GEM_PATH:$HOME/.local/share/gem/ruby/3.3.0/bin"

#ignore upper and lowercase when TAB completion
bind "set completion-ignore-case on"

alias dnf='sudo dnf'

###################################
# Shortcuts for things I do often #
###################################

# tldr is a short man page 
alias ma=tldr

# vim-like exit
alias :q='exit'

# git shortcuts
alias gp="git push"
alias st="git status"
alias di="git diff"
alias co="git checkout"
alias gaa="git add -A"
gpu() {
    CURRBRANCH=$(git rev-parse --abbrev-ref HEAD)
    chromium-browser $(git push --set-upstream origin $CURRBRANCH 2>&1 | grep --only-matching https://github.com/.*/$CURRBRANCH)
}
gcam() {
    git add -A
    git commit -m "$*" && git pull && git push
}
gcamu() {
    git add -A
    git commit -m "$*" && gpu
}


#list
alias ls='ls -lah --color=auto'

# v is shorter than vim
alias v='nvim'
alias vim='nvim'

# e - short for edit
alias e='nvim $(fzf --preview "bat --color=always {}")'


#fix obvious typo's
alias cd..='cd ..'
alias pdw="pwd"
alias cim='vim'
alias jsut='just'

## Colorize the grep command output for ease of use (good for log files)##
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'

#continue download
alias wget="wget -c"

# this command updates the packages
alias up='sudo dnf update -y && flatpak update -y'

# update & shut down
alias usd='up && shutdown now'

#ps
alias psa="ps auxf"

# docker commands
alias dockerup='sudo systemctl start docker.service'

# Node version manager
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion


# ghcup for haskell setup
#[ -f "/home/russ/.ghcup/env" ] && source "/home/russ/.ghcup/env" # ghcup-env
[ -f "/home/russ/.ghcup/env" ] && source "/home/russ/.ghcup/env" # ghcup-env

# source the utils needed for flashing firmware to ESP32 board
source ~/export-esp.sh

alias open='nautilus'
alias fabric='~/repos/fabric/client/fabric'
alias t='tmux'
alias ta='tmux attach'

# Show the current git branch in the terminal prompt
# Prompt
export PS1="\\w[\$(git branch 2>/dev/null | grep '^*' | colrm 1 2)]\$ "

# set up zoxide for navigation
eval "$(zoxide init bash)"
alias cd="z"

alias prune="git fetch -p; git branch -r | awk '{print \$1}' | grep -E -v -f /dev/fd/0 <(git branch -vv | grep origin) | awk '{print \$1}' | xargs git branch -d"
alias dn="docker compose down"

# https://github.com/Russell-Waterhouse/query
alias qp="query --perplexity"
alias qg="query --google"

# start a terminal with a fun little ascii art drawing
cat ~/.ascii-art/iron_ring.txt

