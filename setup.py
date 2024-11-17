#!/usr/bin/python3

import os
import subprocess

# List of packages to install via DNF
packages = [
    "cowsay",
    "figlet",
    "fastfetch",
    "htop",
    "hugo",
    "jq",
    "ncdu",
    "neovim",
    "git",
    "git-lfs",
    "tldr",
    "tmux",
    "tree",
    "zoxide",
    "cmatrix",
    "ripgrep",
    "fd",
    "vim",
    "unzip",
    "wget",
    "htop",
    "hugo",
    "jq",
    "ncdu",
    "neovim",
    "git",
    "git-lfs",
    "tldr",
    "tmux",
    "tree",
    "zoxide",
    "cmatrix",
    "ripgrep",
    "fd",
    "gcc",
    "alacritty",
    "nodejs",
    "python3"
]

# Define paths
user = "russ"
home_directory = f"/home/{user}"
bashrc_path = os.path.join(home_directory, ".bashrc")
ascii_art_path = os.path.join(home_directory, ".ascii-art")
nvim_config_path = os.path.join(home_directory, ".config/nvim")
tmux_config_path = os.path.join(home_directory, ".config/tmux")
editor = "nvim"

# Git configuration settings
git_user_name = "Russell-Waterhouse"
git_user_email = "Russell.L.Waterhouse@gmail.com"
git_extra_config = {
    "pull.rebase": "false",
    "init.defaultBranch": "main"
}


def run_command(command):
    """Helper function to run shell commands."""
    subprocess.run(command, shell=True, check=True)


def setup_groups():
    groups = ["docker", "uinput"]

    # Get the current user's groups
    user_groups = subprocess.check_output("groups", shell=True).decode().strip().split()

    for group in groups:
        # Check if the user is already in the group
        if group not in user_groups:
            # If not, create the group (if necessary) and add the user
            run_command(f"sudo groupadd {group}")
            run_command(f"sudo usermod -aG {group} $USER")
        else:
            print(f"User is already in the '{group}' group.")


def install_packages():
    try:
        # Get the list of installed packages using `dnf list installed`
        installed_packages = subprocess.check_output(
            ['dnf', 'list', '--installed'], text=True
        ).splitlines()
        # Extract just the package names (first column) from the output
        # installed_packages = {line.split()[0] for line in installed_packages[1:]}  # skip the header line
        # installed_packages = []
        # breakpoint()
        installed = []
        for line in installed_packages[1:]:
            package = line.split('.')[0]
            installed.append(package)
        # Iterate over the list of packages to install
        for package in packages:
            # If the package is not installed, install it
            if package not in installed:
                print(f"Installing package: {package}")
                run_command(f"sudo dnf install -y {package}")
            else:
                print(f"Package {package} is already installed.")
    except subprocess.CalledProcessError as e:
        print(f"Error running dnf: {e}")
        print(f"Command output: {e.output}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# 2. Set environment variables (for example, `EDITOR=nvim`)
def set_environment_variables():
    print("Setting environment variables...")
    bashrc_content = ""
    if os.path.exists(bashrc_path):
        with open(bashrc_path, "r") as bashrc_file:
            bashrc_content = bashrc_file.read()
    
    # Add the EDITOR environment variable
    bashrc_content += f"\nexport EDITOR={editor}\n"
    
    # Save back to the file
    with open(bashrc_path, "w") as bashrc_file:
        bashrc_file.write(bashrc_content)


def configure_git():
    print("Configuring Git settings...")
    run_command(f"git config --global user.name \"{git_user_name}\"")
    run_command(f"git config --global user.email \"{git_user_email}\"")
    
    for key, value in git_extra_config.items():
        run_command(f"git config --global {key} {value}")


def copy_files():
    print("Copying configuration files...")
    
    # Example paths for the configuration files
    config_files = {
        ".bashrc": bashrc_path,
        ".ascii-art": ascii_art_path,
        "nvim": nvim_config_path,
        "tmux": tmux_config_path
    }
    
    for src, dest in config_files.items():
        if os.path.exists(src):
            print(f"Copying {src} to {dest}")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            subprocess.run(["cp", "-r", src, dest])
        else:
            print(f"Source file {src} not found. Skipping.")


def set_up_workspaces():
    run_command("gsettings set org.gnome.mutter dynamic-workspaces false")
    run_command("gsettings set org.gnome.desktop.wm.preferences num-workspaces 9")
    for i in range(1, 9):
        run_command(f"gsettings set \"org.gnome.shell.keybindings\" \"switch-to-application-{i}\" \"[]\"")
        run_command(f"gsettings set \"org.gnome.desktop.wm.keybindings\" \"switch-to-workspace-{i}\" \"['<Super>{i}']\"")
        run_command(f"gsettings set \"org.gnome.desktop.wm.keybindings\" \"move-to-workspace-{i}\" \"['<Super><Shift>{i}']\"")


def setup_tpm():
    tpm_dir = os.path.expanduser('~/.tmux/plugins/tpm')
    if not os.path.isdir(tpm_dir):
        run_command("git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm")


# Main function to execute the steps
def main():
    install_packages()
    set_environment_variables()
    configure_git()
    copy_files()
    setup_groups()
    set_up_workspaces()
    setup_tpm()

    print("Setup completed successfully!")


# Run the script
if __name__ == "__main__":
    main()
