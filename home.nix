{ ... }: {
  home = {
    packages = with pkgs; [
      hello
      cowsay
      home-manager
    ];
    username = "russ";
    homeDirectory = "/home/russ";

    stateVersion = "24.05";
  };

  programs.home-manager.enable = true;
}
