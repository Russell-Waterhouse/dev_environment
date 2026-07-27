#!/usr/bin/python3

import os
import subprocess
import argparse
import time

# List of packages to install via DNF
dnf_packages = [
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
    "ruby-devel",
    "zlib-devel",
    "bat",
    "just",
    "helm",
    "libubsan",
    "gnome-terminal",  # Needed for docker-desktop
    "luarocks",  # Needed for nvim
    "valgrind",
    "btop",
    "clang"
]

flatpak_packages = [
    "AzureStorageExplorer",
]
# Define paths
user = "russ"
home_directory = f"/home/{user}"
bashrc_path = os.path.join(home_directory, ".bashrc")
ascii_art_path = os.path.join(home_directory, ".ascii-art")
nvim_config_path = os.path.join(home_directory, ".config/nvim")
tmux_config_path = os.path.join(home_directory, ".config/tmux")
restart_keybinds_path = os.path.join(home_directory, "restart_keybinds.sh")
fix_homerow_mods = os.path.join(home_directory, "fix_homerow_mods_temporarily.sh")
ghostty_config_path = os.path.join(home_directory, ".config/ghostty/config.ghostty")
stop_keybinds_path = os.path.join(home_directory, "stop_keybinds.sh")
kanata_config_path = os.path.join(home_directory, ".config/systemd/user/kanata.service")
opencode_config_path = os.path.join(home_directory, ".config/opencode")
docker_desktop_install_path = "/opt/docker-desktop"
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


def install_dnf_and_flatpak_packages():
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
        for package in dnf_packages:
            # If the package is not installed, install it
            if package not in installed:
                print(f"Installing package: {package}")
                run_command(f"sudo dnf install -y {package}")
            else:
                print(f"Package {package} is already installed.")
        for package in flatpak_packages:
            print(f"Installing package: {package}")
            run_command(f"flatpak install -y {package}")
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
        "fix_homerow_mods_temporarily.sh": fix_homerow_mods,
        "./config.ghostty": ghostty_config_path,
        "kanata_configs/kanata.service": kanata_config_path,
        "opencode": opencode_config_path,
    }

    for src, dest in config_files.items():
        if os.path.exists(src):
            print(f"Copying {src} to {dest}")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            run_command(f"rm -rf {dest}")
            run_command(f"cp -r {src} {dest}")
        else:
            print(f"Source file {src} not found. Skipping.")

    compile_nvim_spell()


def compile_nvim_spell():
    """Build .spl from the personal word list so spell check sees new words."""
    spell_add = os.path.join(nvim_config_path, "spell", "en.utf-8.add")
    if not os.path.isfile(spell_add):
        print(f"No spell word list at {spell_add}, skipping mkspell.")
        return
    print(f"Compiling spell file {spell_add}...")
    run_command(f'nvim --headless "+mkspell! {spell_add}" +qa')


def set_up_workspaces():
    run_command("gsettings set org.gnome.mutter dynamic-workspaces false")
    run_command("gsettings set org.gnome.desktop.wm.preferences num-workspaces 9")
    for i in range(1, 10):
        run_command(f"gsettings set \"org.gnome.shell.keybindings\" \"switch-to-application-{i}\" \"[]\"")
        run_command(f"gsettings set \"org.gnome.desktop.wm.keybindings\" \"switch-to-workspace-{i}\" \"['<Super>{i}']\"")
        run_command(f"gsettings set \"org.gnome.desktop.wm.keybindings\" \"move-to-workspace-{i}\" \"['<Super><Shift>{i}']\"")


def setup_shortcuts():
    """Setup keyboard shortcuts"""
    # Super+q for close window instead of alt+f4
    run_command("gsettings set org.gnome.desktop.wm.keybindings close \"['<Super>q']\"")

    # Setup slots for custom shortcuts
    run_command("gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings \"[ '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/', '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/' ]\"")

    # super+return for opening ghostty
    run_command("gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ name 'Ghostty'")
    run_command("gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ command 'ghostty'")
    run_command("gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ binding '<Super>Return'")

    # super+shift+return for opening ~ in the file explorer
    run_command("gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/ name 'Home Folder'")
    run_command("gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/ command 'xdg-open /home/russ'")
    run_command("gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/ binding '<Super><Shift>Return'")


def disable_key_binding_that_fucks_up_my_monitors():
    # Normally, super+p allows you to change if you mirror or join your displays
    # however, if you hit it by accident, it resets your monitor join settings,
    # so my vertical monitor is now horizontal.
    print("Disabling the key binding that fucks up my monitors")
    run_command("gsettings set org.gnome.mutter.keybindings switch-monitor \"['']\"")


def setup_tpm():
    tpm_dir = os.path.expanduser('~/.tmux/plugins/tpm')
    if not os.path.isdir(tpm_dir):
        run_command("git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm")


def setup_docker_desktop():
    if os.path.exists(docker_desktop_install_path):
        print("Docker desktop is already installed!")
        return

    run_command("sudo dnf -y install dnf-plugins-core")
    run_command("sudo dnf config-manager addrepo --overwrite --from-repofile=https://download.docker.com/linux/fedora/docker-ce.repo")
    run_command("sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")
    run_command("wget --output-document /tmp/docker-desktop-x86_64.rpm https://desktop.docker.com/linux/main/amd64/docker-desktop-x86_64.rpm")
    # sleep for 10 seconds to allow wget to finish the download.
    # I can't figure out why this isn't synchronous, but I have things to do.
    time.sleep(10)
    run_command("sudo dnf install -y /tmp/docker-desktop-x86_64.rpm")
    run_command(" rm -rf /tmp/docker-desktop-x86_64.rpm")


def rm_docker_desktop():
    print("Removing Docker Desktop and related packages...")
    run_command_no_check("sudo systemctl stop docker-desktop")
    run_command_no_check("sudo dnf remove -y docker-desktop")
    run_command_no_check("sudo dnf remove -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")
    run_command_no_check("sudo rm -f /etc/yum.repos.d/docker-ce.repo")
    run_command_no_check(f"sudo rm -rf {docker_desktop_install_path}")
    print("Docker Desktop removed.")


def reinstall_docker_desktop():
    rm_docker_desktop()
    setup_docker_desktop()


def install_k8s_lens():
    if os.path.exists("/usr/bin/lens-desktop"):
        print("Lens desktop is already installed")
        return
    print("Installing Lens desktop")
    run_command("sudo dnf config-manager addrepo --from-repofile=https://downloads.k8slens.dev/rpm/lens.repo")
    run_command("sudo dnf install -y lens")


# TODO: THIS IS BEING OVERWRITTEN BY INSTALLING KUBELOGIN
# WITH THE COMMAND
# `az aks install-cli`
def install_kubectl():
    if (subprocess.run('which kubectl', shell=True, check=False) == 0):
        print("kubectl is already installed")
        return
    print("Installing kubectl")
    run_command("""
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.31/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.31/rpm/repodata/repomd.xml.key
EOF""")
    run_command("sudo yum install -y kubectl")


def install_az_cli():
    if (run_command_no_check('which az') == 0):
        print("az cli is already installed")
        return
    run_command('sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc')
    run_command('sudo dnf install -y https://packages.microsoft.com/config/rhel/9.0/packages-microsoft-prod.rpm')
    run_command('sudo dnf install -y azure-cli')


def setup_homerow_mods():
    if (run_command_no_check('which kanata') == 0):
        print("Home Row Mods with Kanata are already set up")
        return

    # Pre-release required: tap-hold-opposite-hand and defhands (timeless opposite-hand
    # homerow mods) shipped in v1.12; latest stable (v1.11.0) does not include them.
    kanata_version = "v1.12.0-prerelease-2"

    print("Installing Home Row Mods with Kanata")
    run_command('mkdir -p /tmp/kanata-install')
    run_command(
        f'sudo wget -O /tmp/kanata-install/kanata.zip '
        f'https://github.com/jtroo/kanata/releases/download/{kanata_version}/linux-binaries-x64.zip'
    )
    run_command('sudo unzip -o /tmp/kanata-install/kanata.zip -d /tmp/kanata-install')
    run_command('sudo install -m 755 /tmp/kanata-install/kanata_linux_x64 /usr/local/bin/kanata')
    run_command('rm -rf /tmp/kanata-install')
    run_command('mkdir -p /home/russ/.config/kanata')
    run_command('cp kanata_configs/config.kbd /home/russ/.config/kanata/config.kbd')

    print("Setting up Kanata to run in the background")
    run_command('sudo touch /etc/udev/rules.d/99-input.rules')
    run_command('sudo cp kanata_configs/99-input.rules /etc/udev/rules.d/99-input.rules')
    # TODO: I can't get this kernel mod stuff to load on boot or on login, so I'm
    # just going to hack around this for now with a script.
    # TODO: spend some time and find a permanent solution.
    run_command('sudo cp kanata_configs/99-input.rules /etc/udev/rules.d/99-uinput.rules')  # Is this needed?
    run_command("echo uinput | sudo tee /etc/modules-load.d/uinput.conf")
    run_command('sudo udevadm control --reload-rules && sudo udevadm trigger')
    run_command('sudo modprobe uinput')
    run_command('test -r /dev/uinput')
    run_command('test -w /dev/uinput')
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
    run_command('sudo dnf copr enable scottames/ghostty')
    run_command('sudo dnf install ghostty -y')


def install_minikube():
    if (run_command_no_check('which minikube') == 0):
        print("Minikube is already installed")
        return
    print("Installing minikube")
    run_command("curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-latest.x86_64.rpm")
    run_command("sudo rpm -Uvh minikube-latest.x86_64.rpm")
    run_command("rm minikube-latest.x86_64.rpm")


def install_terraform():
    if (run_command_no_check('which terraform') == 0):
        print('terraform is already installed')
        return
    print("Installing terraform")
    run_command("sudo dnf install -y dnf-plugins-core")
    run_command("sudo dnf config-manager addrepo --from-repofile=https://rpm.releases.hashicorp.com/fedora/hashicorp.repo")
    run_command("sudo dnf -y install terraform")


def install_rust():
    if (run_command_no_check('which rustc') == 0):
        print('rust is alreay installed')
        return
    print('installing rust')
    run_command("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")


def install_treesitter_dependency():
    # Required for treesitter to work properly in neovim
    run_command("cargo install --locked tree-sitter-cli")


# TODO: Finish this next time I'm setting up a new machine.
def install_cursor():
    run_command("curl -LO https://api2.cursor.sh/updates/download/golden/linux-x64-rpm/cursor/")
    print("I never finished the install cursor script. Guess you (future Russell) needs to finish that now")
    # run_command("rm cursor-*.rpm")


def install_opencode():
    run_command("curl -fsSL https://opencode.ai/install | bash")


# Main function to execute the steps
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--install", help="Install DNF Packages", action="store_true")
    parser.add_argument("-a", "--all", help="Run full setup", action="store_true")
    parser.add_argument("-f", "--force-update", help="Force of apps that do not update themeselves", action="store_true")

    args = parser.parse_args()
    # copy files must be run first because other commands will try to modify
    # .bashrc such as installing fd
    sync_files()

    if args.force_update:
        reinstall_docker_desktop()

    if args.install or args.all:
        install_dnf_and_flatpak_packages()

    if args.all:
        set_environment_variables()
        configure_git()
        setup_groups()
        set_up_workspaces()
        disable_key_binding_that_fucks_up_my_monitors()
        setup_tpm()
        setup_docker_desktop()
        install_kubectl()
        install_k8s_lens()
        install_az_cli()
        install_minikube()
        setup_homerow_mods()
        install_terraform()
        install_rust()
        install_treesitter_dependency()
        install_ghostty()
        setup_shortcuts()
        install_cursor()
        install_opencode()

    print("\nSetup completed successfully!")


# Run the script
if __name__ == "__main__":
    main()

