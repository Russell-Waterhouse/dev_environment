#!/usr/bin/python3

import os
import subprocess
import argparse
import time

# List of packages to install via apt
packages = [
    "cowsay",
    "figlet",
    "htop",
    "hugo",
    "jq",
    "ncdu",
    "git",
    "git-lfs",
    "tldr",
    "tmux",
    "tree",
    "zoxide",
    "cmatrix",
    "ripgrep",
    "fd-find",
    "vim",
    "unzip",
    "wget",
    "htop",
    "hugo",
    "jq",
    "ncdu",
    "gcc",
    "alacritty",
    "nodejs",
    "python3",
    "ruby-full",
    "bat",
    "just",
    "fzf",
    "chromium-browser",
    "npm"
]

snap_packages = [
    "storage-explorer",
    "ghostty",
    "nvim",
    "kubectl",
    "kontena-lens",
    "code"
]
# Define paths
user = "russ"
home_directory = f"/home/{user}"
bashrc_path = os.path.join(home_directory, ".bashrc")
ascii_art_path = os.path.join(home_directory, ".ascii-art")
nvim_config_path = os.path.join(home_directory, ".config/nvim")
tmux_config_path = os.path.join(home_directory, ".config/tmux")
restart_keybinds_path = os.path.join(home_directory, "restart_keybinds.sh")
stop_keybinds_path = os.path.join(home_directory, "stop_keybinds.sh")
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


def run_command_no_check(command):
    """Helper function to run shell commands that are expected to possibly fail"""
    subprocess.run(command, shell=True, check=False)


def setup_groups():
    groups = ["docker", "uinput", "input"]

    # Get the current user's groups
    user_groups = subprocess.check_output("groups", shell=True).decode().strip().split()

    for group in groups:
        # Check if the user is already in the group
        if group not in user_groups:
            # If not, create the group (if necessary) and add the user
            run_command_no_check(f"sudo groupadd {group}")
            run_command(f"sudo usermod -aG {group} $USER")
        else:
            print(f"User is already in the '{group}' group.")


def install_packages():
    try:
        # Get the list of installed packages using `apt list installed`
        installed_packages = subprocess.check_output(
            ['apt', 'list', '--installed'], text=True
        ).splitlines()
        # Extract just the package names (first column) from the output
        installed_packages = {line.split()[0] for line in installed_packages[1:]}  # skip the header line
        installed = []
        for line in installed_packages:
            package = line.split('/')[0]
            installed.append(package)
        # Iterate over the list of packages to install
        print("got here")
        for package in packages:
            # If the package is not installed, install it
            if package not in installed:
                print(f"Installing package: {package}")
                run_command(f"sudo apt install -y {package}")
            else:
                print(f"Package {package} is already installed.")
        for package in snap_packages:
            print(f"Installing package: {package}")
            run_command(f"sudo snap install {package} --classic")
    except subprocess.CalledProcessError as e:
        print(f"Error running apt: {e}")
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


def sync_files():
    print("Syncing configuration files...")

    # Example paths for the configuration files
    config_files = {
        ".bashrc": bashrc_path,
        ".ascii-art": ascii_art_path,
        "nvim": nvim_config_path,  # This is a directory
        "tmux": tmux_config_path,  # This is a directory
        "kanata_configs/restart_keybinds.sh": restart_keybinds_path,
        "kanata_configs/stop_keybinds.sh": stop_keybinds_path,
    }

    for src, dest in config_files.items():
        if os.path.exists(src):
            print(f"Copying {src} to {dest}")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            run_command(f"rm -rf {dest}")
            run_command(f"cp -r {src} {dest}")
        else:
            print(f"Source file {src} not found. Skipping.")


def set_up_workspaces():
    run_command("gsettings set org.gnome.mutter dynamic-workspaces false")
    run_command("gsettings set org.gnome.desktop.wm.preferences num-workspaces 9")
    for i in range(1, 10):
        run_command(f"gsettings set \"org.gnome.shell.keybindings\" \"switch-to-application-{i}\" \"[]\"")
        run_command(f"gsettings set \"org.gnome.desktop.wm.keybindings\" \"switch-to-workspace-{i}\" \"['<Super>{i}']\"")
        run_command(f"gsettings set \"org.gnome.desktop.wm.keybindings\" \"move-to-workspace-{i}\" \"['<Super><Shift>{i}']\"")


def setup_tpm():
    tpm_dir = os.path.expanduser('~/.tmux/plugins/tpm')
    if not os.path.isdir(tpm_dir):
        run_command("git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm")


def setup_docker_desktop():
    docker_desktop_install_path = "/opt/docker-desktop"
    if os.path.exists(docker_desktop_install_path):
        print("Docker desktop is already installed!")
        return
    # install prerequisites
    run_command("""# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update""")
    run_command("sudo apt install -y gnome-terminal")
    run_command("sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")
    run_command("cd /tmp \
            && wget https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb")
    run_command("cd /tmp \
            && sudo apt-get update")
    time.sleep(30) # allow time for .deb file to download
    run_command("cd /tmp \
            && sudo apt-get install -y ./docker-desktop-amd64.deb")
    run_command("cd /tmp \
            && rm -rf ./docker-desktop-amd64.deb")

def install_az_cli():
    if (run_command_no_check('which az') == 0):
        print("az cli is already installed")
        return
    run_command('curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash')


def setup_homerow_mods():
    if (run_command_no_check('which kanata') == 0):
        print("Home Row Mods with Kanata are already set up")
        return

    print("Installing Home Row Mods with Kanata")
    run_command('sudo wget --directory-prefix /usr/local/bin https://github.com/jtroo/kanata/releases/download/v1.7.0/kanata')
    run_command('sudo chmod +x /usr/local/bin/kanata')
    run_command('mkdir -p /home/russ/.config/kanata')
    run_command('cp kanata_configs/config.kbd /home/russ/.config/kanata/config.kbd')

    print("Setting up Kanata to run in the background")
    run_command('sudo touch /etc/udev/rules.d/99-input.rules')
    run_command('sudo cp kanata_configs/99-input.rules /etc/udev/rules.d/99-input.rules')
    # with open('/etc/udev/rules.d/99-input.rules', 'w') as f:
    # f.write('KERNEL=="uinput", MODE="0660", GROUP="uinput", OPTIONS+="static_node=uinput""')
    run_command('sudo udevadm control --reload-rules && sudo udevadm trigger')
    run_command('sudo modprobe uinput')
    run_command('mkdir -p ~/.config/systemd/user')
    run_command('cp kanata_configs/kanata.service ~/.config/systemd/user/kanata.service')

    run_command('systemctl --user daemon-reload')
    run_command('systemctl --user enable kanata.service')
    run_command('systemctl --user start kanata.service')
    run_command('systemctl --user status kanata.service')


def install_ghostty():
    if (run_command_no_check('which ghostty') == 0):
        print("Ghostty is already installed")
        return
    print("Installing Ghostty")
    run_command('dnf copr enable pgdev/ghostty')
    run_command('dnf install ghostty')


# Main function to execute the steps
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Install Packages", action="store_true")
    parser.add_argument("-a", "--all", help="Run full setup", action="store_true")
    args = parser.parse_args()
    # copy files must be run first because other commands will try to modify
    # .bashrc such as installing fd
    sync_files()

    if args.install or args.all:
        install_packages()

    if args.all:
        set_environment_variables()
        configure_git()
        setup_groups()
        set_up_workspaces()
        setup_tpm()
        setup_docker_desktop()
        install_az_cli()
        setup_homerow_mods()

    print("Setup completed successfully!")


# Run the script
if __name__ == "__main__":
    main()
