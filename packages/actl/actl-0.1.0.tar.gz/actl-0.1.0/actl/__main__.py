import actl
from pathlib import Path


def main():
    app_dir = Path(__file__).parent.joinpath("actl-cli")
    actl.main(__name__, app_dir=app_dir)


main()
