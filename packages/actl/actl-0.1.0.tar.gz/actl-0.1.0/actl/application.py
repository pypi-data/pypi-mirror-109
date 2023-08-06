from pathlib import Path
from eprint import eprint
from eprint.str import info
import importlib
from .log import verbose
from .loader import load_modules
from . import singleton

import click


@click.group()
@click.option("-v", "--verbose", count=True)
def cli(verbose):
    singleton.verbosity = verbose


class Application:
    def __init__(self, *args, **kwargs):
        self.app_dir = args[0]
        self.args = args
        self.kwargs = kwargs
        self.feature_map = {}

    def _load_features(self):
        features_dir = Path(self.app_dir, "features").resolve()

        for file_path in Path(features_dir).glob("*.py"):
            feature_name = file_path.stem
            verbose(1, info("Loading feature from {}", file_path))
            #  feature_module = import_module()
            spec = importlib.util.spec_from_file_location(
                f"webplane.app_features.{feature_name}", file_path
            )
            feature_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(feature_module)
            self.feature_map[feature_name] = feature_module

    def _sort_features(self):
        # If there is an AFTER_FEATURE attribute, make sure that
        # feature will be activated first
        sorted_list = []
        for feature_name, feature_module in self.feature_map.items():
            after_feature = getattr(feature_module, "AFTER_FEATURE", None)
            if after_feature and after_feature not in sorted_list:
                sorted_list.insert(0, after_feature)
            if feature_name not in sorted_list:
                sorted_list.append(feature_name)
        new_feature_map = {}
        for feature_name in sorted_list:
            new_feature_map[feature_name] = self.feature_map[feature_name]
        self.feature_map = new_feature_map

    def _activate_features(self):
        for feature_module in self.feature_map.values():
            feature_module.activate(*self.args, **self.kwargs)

    def run(self, command):
        eprint.info("Starting application from {}", self.app_dir)
        app_path = Path(self.app_dir)

        if not app_path.exists():
            eprint.error("Directory '{}' not found!", self.app_dir)
            exit(-3)

        if not Path(self.app_dir).is_dir():
            eprint.error("'{}' is not a directory!", self.app_dir)
            exit(-3)

        self._load_features()
        self._sort_features()
        self._activate_features()

    def run_commands(self):

        # Load command classes found in the "commands" dir
        commands_dir = Path(self.app_dir, "commands")
        commands = load_modules("cmd_", commands_dir, click.core.Command)
        for cmd in commands:
            cli.add_command(cmd)
        cli()
