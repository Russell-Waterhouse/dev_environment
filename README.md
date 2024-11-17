# My Development Environment Setup Script

I'm tired of having my development environment split between my various
development machines, VM's, disposable cloud environments, and other places
where I write code. I'm tired of installing some dependency on one machine and
then having to remember to run those same 4 commands on all of my machines.

The solution?

An impotent script that I can run that sets up my machine exactly how I like.


## But Russ, why not use Docker?

I do! I rarely run any code without it! However, I don't want to set up:
- my LSP in Docker
- my neovim in Docker
- my terminal in Docker

## But Russ, why not use Nix?

I tried! If you look back in the git history of this repo, you can see
that I originally set up this script as a nix home-manager config.
You can also probably find my NixOS config archived on my GitHub.

Here's what I found:

1. I sometimes do work with third party software that isn't packaged in Nix,
or is packaged in Nix but requires some download that an upstream has updated,
which changes the sha256 hash, which breaks the build.
2. Some software just does not run out of the box. Cypress tests are a good
example
3. In these edge cases, I often found confusing and conflicting documentation
describing how to fix this.

I liked nix! I liked what it offered and how it works! Unfortunately it just
didn't do what I need my production machines to do yet. I will try it again
when either my requirements change or 

