# My Home-Manager Config


## WARNING: EXPERIMENTAL

I have no idea what I'm doing, I'm investigating a technology that I think solves a problem that I have, namely reproducibility of my dev environments.


## How to use this configuration

1. Install the nix package manager from https://nixos.org/download/
2. Clone this repo to your `~/.config` directory and rename it to `home-manager`
3. TODO

I THINK what I should do next is run: 
```
cd ~/.config/home-manager
nix-shell -p home-manager
```
and in the shell that spawns, run: 
```
home-manager switch --flake .
```
But I haven't tested that yet. 

## How I set this up

I ran this command 
```
nix run home-manager/master -- init --switch
```

## How to update your system

run 
```
cd ~/.config/home-manager
home-manager switch --flake .
```

## How to find more

run 
```
man home-configuration.nix
```
