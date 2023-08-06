import importlib
import importlib.resources
import importlib.util
import inspect
import pathlib
import sys
import types
import typing as t
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List

import attr
import pkg_resources
import toml

from mario import asynch
from mario import config
from mario import declarative
from mario import interpret
from mario import utils


@attr.dataclass
class PluginObject:
    name: str
    traversal_function: types.FunctionType
    required_parameters: List[str]
    calculate_more_params: types.FunctionType = attr.ib(default=lambda x: {})


@attr.dataclass
class CommandStage:
    name: str

    options: List[str]
    arguments: List[str]
    remap_params: Dict


@attr.dataclass
class CommandCommand:
    name: str
    components: List[CommandStage]
    short_help: str
    options: t.Dict = attr.ib(factory=dict)
    arguments: t.Dict = attr.ib(factory=dict)


NO_DEFAULT = attr.make_class("NO_DEFAULT", [])()


@attr.dataclass
class GlobalOption:
    name: str
    type: type
    default: type(NO_DEFAULT)


@attr.s
class Registry:
    traversals: Dict[str, PluginObject] = attr.ib(factory=dict)
    global_options: Dict[str, GlobalOption] = attr.ib(factory=dict)
    cli_functions: Dict[str, Any] = attr.ib(factory=dict)
    commands: Dict[str, CommandCommand] = attr.ib(factory=dict)

    def register(self, name=None, params=None):
        def wrap(function):
            if name is None:
                registered_name = function.__name__
            else:
                registered_name = name

            self.traversals[registered_name] = PluginObject(
                registered_name, function, params
            )
            return function

        return wrap

    def add_traversal(self, name=None, calculate_more_params=lambda x: {}):
        def wrap(function):

            if name is None:
                registered_name = function.__name__
            else:
                registered_name = name

            params = [param for param in inspect.signature(function).parameters.keys()]
            self.traversals[registered_name] = PluginObject(
                registered_name, function, params, calculate_more_params
            )
            return function

        return wrap

    def add_cli(self, name=None):
        def wrap(function):
            if name is None:
                registered_name = function.__name__
            else:
                registered_name = name

            self.cli_functions[registered_name] = function

            return function

        return wrap


# Currently, mario reserves `function`, `command`, `stack`, `items`, `global_namespace`.
# These could all be provided in a namespace object.


def plugin_module_paths() -> List[str]:
    return [
        entry_point.module_name + "." + entry_point.name
        for entry_point in pkg_resources.iter_entry_points(f"{utils.NAME}_plugins")
    ]


def collect_modules(import_paths: Iterable[str]) -> List[types.ModuleType]:
    modules = []
    for path in import_paths:
        modules.append(importlib.import_module(path))
    return modules


def combine_registries(registries):
    global_options = {}
    traversals = {}
    cli_functions = {}
    commands = {}
    for registry in registries:
        traversals.update(registry.traversals)
        global_options.update(registry.global_options)
        cli_functions.update(registry.cli_functions)
        commands.update(registry.commands)
    return Registry(traversals, global_options, cli_functions, commands)


def make_plugin_registry():
    plugin_modules = collect_modules(plugin_module_paths())
    plugin_registries = [module.registry for module in plugin_modules]

    return combine_registries(plugin_registries)


def make_config_registry():
    modules = import_config_dir_modules()
    return combine_registries(module.registry for module in modules)


def load_module(path):
    module_name = "user_config." + path.with_suffix("").name
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def import_config_dir_modules(user_config_dir=None):
    if user_config_dir is None:
        user_config_dir = config.get_config_dir()

    modules = []
    for path in (pathlib.Path(user_config_dir) / "modules").rglob("*.py"):
        module = load_module(path)
        modules.append(module)

    return modules


def make_global_registry():
    return combine_registries(
        [
            make_plugin_registry(),
            make_config_registry(),
            make_config_commands_registry(),
            make_plugin_commands_registry(),
        ]
    )


def make_synthetic_command(cmd,):
    declarative.CommandSchema()
    components = [
        CommandStage(
            d["command"],
            d.get("options", []),
            d.get("arguments", []),
            remap_params=d.get("remap_params", []),
        )
        for d in cmd["stage"]
    ]
    return CommandCommand(
        cmd["name"],
        components,
        cmd["short_help"],
        options=cmd.get("options", {}),
        arguments=cmd.get("arguments", []),
    )


def make_commands(conf):
    synth_commands = []

    commands = declarative.CommandSchema(many=True).load(conf.get("command", []))

    return commands


def make_config_commands_registry():
    conf = config.load_config()

    commands = make_commands(conf)
    return Registry(commands={c.name: c for c in commands})


def make_plugin_commands_registry(package="mario.plugins"):
    plugin_tomls = [
        filename
        for filename in importlib.resources.contents(package)
        if filename.endswith(".toml")
    ]
    confs = [
        toml.loads(importlib.resources.read_text(package, filename))
        for filename in plugin_tomls
    ]

    conf_command_groups = [make_commands(conf) for conf in confs]
    registries = [
        Registry(commands={c.name: c for c in commands})
        for commands in conf_command_groups
    ]
    return combine_registries(registries)
