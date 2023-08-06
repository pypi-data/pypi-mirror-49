import os
import sys

import attr
import click

import mario
import mario.doc

from . import app
from . import config
from . import utils


config.DEFAULTS.update(
    config.load_config(
        dir_path=os.environ.get(f"{utils.NAME}_CONFIG_DIR".upper(), None)
    )
)


class ReSTCommand(click.Command):
    """Parse help as rst."""

    def format_help_text(self, ctx, formatter):

        if self.help:
            self.help = mario.doc.rst2text(self.help)
            original_wrap_text = click.formatting.wrap_text
            click.formatting.wrap_text = lambda x, *a, **kw: x
            super().format_help_text(ctx, formatter)
            click.formatting.wrap_text = original_wrap_text
            return

        if self.short_help:
            original_help = self.help
            self.help = self.short_help
            super().format_help_text(ctx, formatter)
            self.help = original_help
            return


class SectionedFormatter(click.formatting.HelpFormatter):
    def __init__(self, *args, sections, **kwargs):
        self.sections = sections
        super().__init__(*args, **kwargs)

    # pylint: disable=arguments-differ
    def write_dl(self, rows, *args, **kwargs):

        cmd_to_section = {}
        for section_name, help_section in self.sections.items():

            for command in help_section.entries:
                cmd_to_section[command] = section_name

        sections = {}

        # pylint: disable=redefined-builtin
        for subcommand, help in rows:
            sections.setdefault(
                cmd_to_section.get(subcommand, "Custom commands"), []
            ).append((subcommand, help))

        for section_name, section_rows in sections.items():
            if section_rows[0][0][0] == "-":
                super().write_dl(section_rows)
            else:
                with super().section(section_name):
                    super().write_dl(section_rows, *args, **kwargs)


class SectionedContext(click.Context):
    def __init__(self, *args, sections, **kwargs):
        self.sections = sections
        super().__init__(*args, **kwargs)

    def make_formatter(self):
        """Creates the formatter for the help and usage output."""
        return SectionedFormatter(
            sections=self.sections,
            width=self.terminal_width,
            max_width=self.max_content_width,
        )


class SectionedGroup(click.Group):
    def __init__(self, *args, sections, **kwargs):
        self.sections = sections
        super().__init__(self, *args, **kwargs)

    def make_context(self, info_name, args, parent=None, **extra):
        """This function when given an info name and arguments will kick
        off the parsing and create a new :class:`Context`.  It does not
        invoke the actual command callback though.

        :param info_name: the info name for this invokation.  Generally this
                          is the most descriptive name for the script or
                          command.  For the toplevel script it's usually
                          the name of the script, for commands below it it's
                          the name of the script.
        :param args: the arguments to parse as list of strings.
        :param parent: the parent context if available.
        :param extra: extra keyword arguments forwarded to the context
                      constructor.
        """
        # pylint: disable=protected-access
        for key, value in click._compat.iteritems(self.context_settings):
            if key not in extra:
                extra[key] = value
        ctx = SectionedContext(
            self, info_name=info_name, parent=parent, sections=self.sections, **extra
        )
        with ctx.scope(cleanup=False):
            self.parse_args(ctx, args)
        return ctx

    def format_commands(self, ctx, formatter):
        """Extra format methods for multi methods that adds all the commands
        after the options.
        """
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                # pylint: disable=redefined-builtin
                help = cmd.get_short_help_str(limit)
                rows.append((subcommand, help))

            if rows:
                formatter.write_dl(rows)


CONTEXT_SETTINGS = {"default_map": config.DEFAULTS}

doc = f"""\
Mario: Python pipelines for your shell.

GitHub: https://github.com/python-mario/mario

\b
Configuration:
  Declarative config: {config.get_config_dir() / 'config.toml'}
  Python modules: {config.get_config_dir() / 'modules/*.py'}

"""


SECTIONS = {
    "Traversals": mario.doc.HelpSection(
        0,
        ["map", "filter", "apply", "eval", "reduce", "chain"],
        doc="Basic commands for calling functions on data.",
        name="Traversals",
    ),
    "Async traversals": mario.doc.HelpSection(
        1,
        [
            "async-map",
            "async-apply",
            "async-filter",
            "async-chain",
            "async-map-unordered",
        ],
        doc="Commands for asynchronously calling functions on data.",
        name="Async traversals",
    ),
}

ALIASES = app.global_registry.commands


def show(x):
    if hasattr(x, "__dict__"):
        return attr.make_class(type(x).__name__, list(vars(x).keys()))(
            **{k: show(v) for k, v in vars(x).items()}
        )
    if isinstance(x, list):
        return [show(v) for v in x]
    if isinstance(x, dict):
        return {k: show(v) for k, v in x.items()}
    return repr(x)


def cli_main(pairs, **kwargs):
    app.main(pairs, **kwargs)


def version_option(ctx, param, value):  # pylint: disable=unused-argument
    if not value:
        return
    click.echo("mario, version " + mario.__version__)
    sys.exit()


def build_stages(command):
    def run(ctx, **cli_params):
        out = []

        for stage in command.stages:

            mapped_stage_params = {
                remap.old.lstrip("-"): cli_params[remap.new.lstrip("-")]
                for remap in stage.remap_params
            }
            mapped_stage_params.update(stage.params)
            inject_namespace = {
                k: v for k, v in cli_params.items() if k in command.inject_values
            }
            cmd = cli.get_command(ctx, stage.command)
            out.extend(
                ctx.invoke(cmd, **mapped_stage_params, inject_values=inject_namespace)
            )
        return out

    params = command.arguments + command.options

    sections = {}
    if command.section:
        sections.setdefault(command.section, []).append(command.name)
    for key, entries in sections.items():
        if key in SECTIONS.keys():
            existing = SECTIONS[key]
            SECTIONS[key] = attr.evolve(existing, entries=existing.entries + entries)
        else:
            SECTIONS[key] = mario.doc.HelpSection(100, entries, name=command.section)

    return ReSTCommand(
        name=command.name,
        params=params,
        callback=click.pass_context(run),
        short_help=command.short_help,
        help=command.help,
    )


# pylint: disable=unsupported-assignment-operation
COMMANDS = app.global_registry.cli_functions

# pylint: disable=no-member
for k, v in ALIASES.items():

    COMMANDS[k] = build_stages(v)


cli = SectionedGroup(
    result_callback=cli_main,
    chain=True,
    context_settings=CONTEXT_SETTINGS,
    params=[
        click.Option(
            ["--max-concurrent"], type=int, default=config.DEFAULTS["max_concurrent"]
        ),
        click.Option(
            ["--exec-before"],
            help="Python source code to be executed before any stage.",
            default=config.DEFAULTS["exec_before"],
        ),
        click.Option(
            ["--base-exec-before"],
            help="Python source code to be executed before any stage; typically set in the user config file. Combined with --exec-before value. ",
            default=config.DEFAULTS["base_exec_before"],
        ),
        click.Option(
            ["--version"],
            callback=version_option,
            is_flag=True,
            help="Show the version and exit.",
        ),
    ],
    help=doc,
    commands=COMMANDS,
    sections=SECTIONS,
)
