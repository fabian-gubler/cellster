{
  description = "Basic Python Configuration Flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-23.05";
  };

  outputs = inputs@{ self, nixpkgs, flake-utils, ... }:

    flake-utils.lib.eachDefaultSystem (system:
      let
        python = "python310"; # <--- change here
        pythonPackages = pkgs.python310Packages;# <--- change here
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      {
        devShell = pkgs.mkShell {
          name = "python";
          venvDir = "./.venv";
          buildInputs = [
            # A Python interpreter including the 'venv' module is required to bootstrap
            # the environment.
            pythonPackages.python

            # This executes some shell code to initialize a venv in $venvDir before
            # dropping into the shell
            pythonPackages.venvShellHook

            # Dependencies that we would like to use from nixpkgs, which will
            # add them to PYTHONPATH and thus make them accessible from within the venv.
            pythonPackages.pytest
            pythonPackages.flake8
            pythonPackages.isort
			pythonPackages.debugpy
			pythonPackages.tkinter
            pkgs.black
            pkgs.nodePackages.pyright
          ];

        };
      }
    );
}
