{
  description = "Axiom Hive - C=0 AI System";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python312;
        pythonEnv = python.withPackages (ps: [
          ps.z3-solver ps.cryptography ps.fastapi ps.uvicorn ps.orjson ps.pynacl
        ]);
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [ pythonEnv pkgs.sqlite ];
          shellHook = ''
            export AXIOM_HIVE_HOME=$PWD
            export PYTHONPATH=$PWD:$PYTHONPATH
            echo "Axiom Hive dev env loaded"
          '';
        };
        packages.default = pkgs.stdenv.mkDerivation {
          pname = "axiom-hive";
          version = "1.0.0";
          src = ./.;
          buildInputs = [ pythonEnv ];
          builder = pkgs.writeScript "builder.sh" ''
            #!/bin/sh
            export PYTHONHASHSEED=0
            cp -r $src $out
            cd $out
            python scripts/verify_integrity.py
            python -m pytest tests/ --tb=short
          '';
          outputHashMode = "recursive";
          outputHashAlgo = "sha256";
          outputHash = "sha256:c0de1234c0de1234c0de1234c0de1234c0de1234c0de1234c0de1234c0de1234";
        };
      }
    );
}