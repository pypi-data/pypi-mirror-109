from actl.application import Application
from pathlib import Path


def main(name, file=None, app_name=None, appvesion=None, app_dir=None):

    # When called fromt he Windows script the name is module.__name__
    if "." in name:
        name = name.split(".")[-1]

    if name != "__main__":
        return
    if file:
        app_dir = Path(file).parent
    application = Application(app_dir)
    application.run_commands()
