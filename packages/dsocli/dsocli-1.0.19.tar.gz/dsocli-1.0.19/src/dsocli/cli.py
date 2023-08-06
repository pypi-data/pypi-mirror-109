import sys
import os
import platform
import click
import re
import yaml
import json
import subprocess
import tempfile
from stdiomask import getpass
from .version import __version__
from .constants import *
from .exceptions import DSOException
from .config import Config
from .logger import Logger, log_levels
from .contexts import Contexts
from .parameters import Parameters
from .secrets import Secrets
from .templates import Templates
from .packages import Packages
from .releases import Releases
from .click_extend import *
from click_params import RangeParamType
from .utils import flatten_dict

DEFAULT_CONTEXT = dict(help_option_names=['-h', '--help'])

###--------------------------------------------------------------------------------------------

@click.group(context_settings=DEFAULT_CONTEXT)
def cli():
    """DevSecOps CLI"""
    pass

###--------------------------------------------------------------------------------------------

@cli.group(context_settings=DEFAULT_CONTEXT)
def config():
    """
    Manage DSO application configuration.
    """
    pass

###--------------------------------------------------------------------------------------------

@cli.group(context_settings=DEFAULT_CONTEXT)
def parameter():
    """
    Manage parameters.
    """
    pass

###--------------------------------------------------------------------------------------------

@cli.group(context_settings=DEFAULT_CONTEXT)
def secret():
    """
    Manage secrets.
    """
    pass

###--------------------------------------------------------------------------------------------

@cli.group(context_settings=DEFAULT_CONTEXT)
def template():
    """
    Manage templates.
    """
    pass

###--------------------------------------------------------------------------------------------

@cli.group(context_settings=DEFAULT_CONTEXT)
def package():
    """
    Manage build packages.
    """
    pass

###--------------------------------------------------------------------------------------------

@cli.group(context_settings=DEFAULT_CONTEXT)
def release():
    """
    Manage deployment releases.
    """
    pass

###--------------------------------------------------------------------------------------------

@cli.group(context_settings=DEFAULT_CONTEXT)
def provision():
    """
    Provision resources.
    """
    pass

###--------------------------------------------------------------------------------------------

@cli.group(context_settings=DEFAULT_CONTEXT)
def deploy():
    """
    Deploy releases.
    """
    pass

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

@cli.command('version', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['version']}")
def version():
    """
    Display versions.
    """
    click.echo(f"DevSecOps Tool CLI: {__version__}\nPython: {platform.sys.version}")


###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

@parameter.command('add', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['parameter']['add']}")
@click.option('-c', '--context', metavar='<stage>[/env]', default='default', help=f"{CLI_PARAMETERS_HELP['common']['context']}")
@click.argument('key', required=False)
# @click.option('-k', '--key', metavar='<key>', help=f"{CLI_PARAMETERS_HELP['parameter']['key']}")
@click.option('-k', '--key', 'key_option', required=False, metavar='<key>', help=f"{CLI_PARAMETERS_HELP['parameter']['key']}")
@click.option('-v', '--value', metavar='<value>', required=False, help=f"{CLI_PARAMETERS_HELP['parameter']['value']}")
@click.option('-i', '--input', metavar='<path>', required=False, type=click.File('r'), help=f"{CLI_PARAMETERS_HELP['common']['input']}")
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml', 'shell']), default='shell', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def add_parameter(context, key, key_option, value, input, format, working_dir, config, verbosity):
    """
    Adds a parameter to the application, or updates its value if already existing.\n
    \tMultiple parmeters may be added at once from an input file using '-i' / '--input' option.
    """

    parameters = []

    def check_command_usage():
        nonlocal context, parameters
        context = Contexts.normalize(context)
        if input:
            if key or key_option:
                Logger.error(MESSAGES['ArgumentsMutualExclusive'].format("'-k' / '--key'","'-i' / '--input'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)
            if format == 'json':
                try:
                    _params = json.load(input)
                    parameters = _params['Parameters']
                # except json.JSONDecodeError as e:
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'yaml':
                try:
                    _params = yaml.load(input, yaml.SafeLoader)
                    parameters = _params['Parameters']
                # except yaml.YAMLError as e:
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'csv':
                _params = input.readlines()
                try:
                    for param in _params:
                        _key = param.split(',')[0].strip()
                        _value = param.split(',')[1].strip()
                        parameters.append({'Key': _key, 'Value': _value})
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'shell':
                _params = input.readlines()
                try:
                    for param in _params:
                        _key = param.split('=', 1)[0].strip()
                        _value = param.split('=', 1)[1].strip()
                        ### eat possible enclosing quotes and double quotes when source is file, stdin has already eaten them!
                        if re.match(r'^".*"$', _value):
                            _value = re.sub(r'^"|"$', '', _value)
                        elif re.match(r"^'.*'$", _value):
                            _value = re.sub(r"^'|'$", '', _value)
                        parameters.append({'Key': _key, 'Value': _value})
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)

        ### not input
        else:
            if key and key_option:
                Logger.error(MESSAGES['ArgumentsMutualExclusive'].format("'key'", "'--key'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)
    
            key = key or key_option

            if not key:
                Logger.error(MESSAGES['AtleastOneofTwoNeeded'].format("'-k' / '--key'","'-i' / '--input'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)
    
            if not value:
                Logger.error(MESSAGES['MissingOption'].format("'-v' / '--value'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)

            parameters.append({'Key': key, 'Value': value})


        invalid = False
        for param in parameters:
            invalid = not Parameters.validate_key(param['Key']) or invalid

        if invalid:
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)

    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()

        for param in parameters:
            key = param['Key']
            value = param['Value']
            Parameters.add(context, key, value)

    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise

###--------------------------------------------------------------------------------------------

@parameter.command('list', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['parameter']['list']}")
@click.option('-c', '--context', metavar='<stage>[/env]', default='default', help=f"{CLI_PARAMETERS_HELP['common']['context']}")
@click.option('-u','--uninherited', 'uninherited', is_flag=True, default=False, help=f"{CLI_PARAMETERS_HELP['parameter']['uninherited']}")
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml', 'shell']), default='shell', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-v', '--show-values', required=False, is_flag=True, default=False, show_default=True, help=f"{CLI_PARAMETERS_HELP['parameter']['show_values']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def list_parameter(show_values, uninherited, context, format, working_dir, config, verbosity):
    """
    Return the list of parameters added to an application.\n
    """

    def check_command_usage():
        nonlocal context
        context = Contexts.normalize(context)

    def print_output(parameters):
        if not len(parameters): return
        flattened = flatten_dict(parameters)
        if format == 'csv':
            if show_values:
                for key, value in flattened.items():
                    print(f"{key},{value}", flush=True)
            else:
                for key in flattened:
                    print(key, flush=True)
        elif format == 'shell':
            if show_values:
                for key, value in flattened.items():
                    # ### preserve enclosing double quotes if part of the value
                    # if re.match(r'^".*"$', value):
                    #     print(f"{key}='{value}'", flush=True)
                    # ### preserve enclosing single quotes if part of the value
                    # elif re.match(r"^'.*'$", value):
                    #     print(f'{key}="{value}"', flush=True)
                    ### No quoting for integer numbers
                    if re.match(r"^[1-9][0-9]*$", value):
                        print(f'{key}={value}', flush=True)
                    ### No quoting for float numbers
                    elif re.match(r"^[0-9]*\.[0-9]*$", value):
                        print(f'{key}={value}', flush=True)
                    ### Double quote if there is single quote
                    elif re.match(r"^.*[']+.*$", value):
                        print(f'{key}="{value}"', flush=True)
                    ### sinlge quote by default
                    else:
                        print(f"{key}='{value}'", flush=True)

            else:
                for key in flattened:
                    print(key, flush=True)
        elif format in ['json', 'yaml']:
            items = []
            if show_values:
                for key, value in flattened.items():
                    items.append({'Key': key, 'Value': value})
            else:
                for key, value in flattened.items():
                    items.append({'Key': key})
            if format == 'json':
                print(json.dumps({'Parameters' : items}, indent=2), flush=True)
            else:
                print(yaml.dump({'Parameters' : items}, indent=2), flush=True)

    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()
        print_output(Parameters.list(context, uninherited))
        # if len(duplicates) > 0:
        #     Logger.warn('Duplicate parameters found:', force=True)
        #     print(*duplicates, sep="\n")
    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise

###--------------------------------------------------------------------------------------------

@parameter.command('get', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['parameter']['get']}")
@click.option('-c', '--context', metavar='<stage>[/env]', default='default', help=f"{CLI_PARAMETERS_HELP['common']['context']}")
@click.argument('key', required=False)
@click.option('-k', '--key', 'key_option', required=False, metavar='<key>', help=f"{CLI_PARAMETERS_HELP['parameter']['key']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def get_parameter(context, key, key_option, working_dir, config, verbosity):
    """
    Return the value of a parameter in the application.\n
    \tKEY: The key of the parameter. It may also be provided via '-k' / '--key' option.
    """

    def check_command_usage():
        nonlocal context, key, key_option
        context = Contexts.normalize(context)        
        if key and key_option:
            Logger.error(MESSAGES['ArgumentsMutualExclusive'].format("'key'", "'--key'"))
            # Logger.info(MESSAGES['TryHelpWithCommand'].format('get parameter'), force=True, stress = False)
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)

        key = key or key_option

        if not key:
            Logger.error(MESSAGES['MissingArgument'].format("'KEY'"))
            # Logger.info(MESSAGES['TryHelpWithCommand'].format('get parameter'), force=True, stress = False)
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)


    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()
        print(Parameters.get(context, key), flush=True)
    
    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise

###--------------------------------------------------------------------------------------------

@parameter.command('delete', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['parameter']['delete']}")
@click.option('-c', '--context', default='', metavar='<stage>[/env]', help=f"{CLI_PARAMETERS_HELP['common']['context']}")
@click.argument('key', required=False)
@click.option('-k', '--key', 'key_option', metavar='<key>', required=False, help=f"{CLI_PARAMETERS_HELP['parameter']['key']}")
@click.option('-i', '--input', metavar='<path>', required=False, type=click.File('r'), help=f"{CLI_PARAMETERS_HELP['common']['input']}")
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml','shell']), default='shell', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def delete_parameter(key, key_option, input, format, context, working_dir, config, verbosity):
    """
    Delete a parameter from the application.\n
    \tKEY: The key of the parameter. It may also be provided via '-k' / '--key' option.\n
    \tMultiple parmeters may be added at once from an input file using '-i' / '--input' option.
    """

    parameters = []

    def check_command_usage():
        nonlocal context, parameters
        context = Contexts.normalize(context)
        if input:
            if key or key_option:
                Logger.error(MESSAGES['ArgumentsMutualExclusive'].format("'-k' / '--key'","'-i' / '--input'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)
            if format == 'json':
                try:
                    parameters = json.load(input)['Parameters']
                # except json.JSONDecodeError as e:
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'yaml':
                try:
                    parameters = yaml.load(input, yaml.SafeLoader)['Parameters']
                # except yaml.YAMLError as e:
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'shell':
                try:
                    for param in input.readlines():
                        _key = param.split('=', 1)[0].strip()
                        # _value = param.split('=', 1)[1].strip()
                        parameters.append({'Key': _key})

                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'csv':
                try:
                    for param in input.readlines():
                        _key = param.split(',')[0].strip()
                        # _value = param.split('=', 1)[1].strip()
                        parameters.append({'Key': _key})
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
        ### not input
        else:
            if key and key_option:
                Logger.error(MESSAGES['ArgumentsMutualExclusive'].format("'key'", "'--key'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)
    
            key = key or key_option

            if not key:
                Logger.error(MESSAGES['AtleastOneofTwoNeeded'].format("'-k' / '--key'","'-i' / '--input'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)


            parameters.append({'Key': key})

        invalid = False
        for param in parameters:
            invalid = not Parameters.validate_key(param['Key']) or invalid

        if invalid:
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)


    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()

        for param in parameters:
            Parameters.delete(context, param['Key'])

    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise

###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

@secret.command('list', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['secret']['list']}")
@click.option('-c', '--context', metavar='<stage>[/env]', default='default', help=f"{CLI_PARAMETERS_HELP['common']['context']}")
@click.option('-u','--uninherited', 'uninherited', is_flag=True, default=False, help=f"{CLI_PARAMETERS_HELP['secret']['uninherited']}")
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml', 'shell']), default='shell', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-v', '--show-values', required=False, is_flag=True, default=False, show_default=True, help=f"{CLI_PARAMETERS_HELP['parameter']['show_values']}")
@click.option('-d', '--decrypt', required=False, is_flag=True, default=False, show_default=True, help=f"{CLI_PARAMETERS_HELP['parameter']['show_values']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def list_secret(decrypt, show_values, uninherited, context, format, working_dir, config, verbosity):
    """
    Return the list of secrets added to the application.\n
    """
    def check_command_usage():
        nonlocal context
        context = Contexts.normalize(context)
        if decrypt:
            if not show_values:
                raise DSOException(MESSAGES['OptionMutualInclusive'].format("'-s' / '--show-values'","'-d' / '--decrypt'"))

    def print_output(secrets):
        if not len(secrets): return
        flattened = flatten_dict(secrets)
        if format == 'shell':
            if show_values:
                f = tempfile.NamedTemporaryFile("w") if decrypt else sys.stdout
                for key, value in flattened.items():
                    # ### preserve enclosing double quotes if part of the value
                    # if re.match(r'^".*"$', value):
                    #     f.write(f"{key}='{value}'\n")
                    # ### preserve enclosing single quotes if part of the value
                    # elif re.match(r"^'.*'$", value):
                    #     f.write(f'{key}="{value}"\n')
                    ### No quoting for integer numbers
                    if re.match(r"^[1-9][0-9]*$", value):
                        f.write(f'{key}={value}\n')
                    ### No quoting for float numbers
                    elif re.match(r"^[0-9]*\.[0-9]*$", value):
                        f.write(f'{key}={value}\n')
                    ### Double quote if there is single quote
                    elif re.match(r"^.*[']+.*$", value):
                        f.write(f'{key}="{value}"\n')
                    ### sinlge quote by default
                    else:
                        f.write(f"{key}='{value}'\n")
                f.flush()
                if decrypt: 
                    p = subprocess.Popen(["less", f.name])  ### TO-DO: make it platform agnostic
                    p.wait()
                if not f == sys.stdout: f.close()
            else:
                for key in flattened:
                    print(key, flush=True)
        elif format == 'csv':
            if show_values:
                f = tempfile.NamedTemporaryFile("w") if decrypt else sys.stdout
                for key, value in flattened.items():
                    f.write(f"{key},{value}\n")
                f.flush()
                if decrypt: 
                    p = subprocess.Popen(["less", f.name])  ### TO-DO: make it platform agnostic
                    p.wait()
                if not f == sys.stdout: f.close()
            else:
                for key in flattened:
                    print(key, flush=True)
        elif format in ['json', 'yaml'] :
            items = []
            if show_values:
                for key, value in flattened.items():
                    items.append({'Key': key, 'Value': value})
            else:
                for key, value in flattened.items():
                    items.append({'Key': key})
            f = tempfile.NamedTemporaryFile("w") if decrypt else sys.stdout
            if format == 'json':
                f.write(json.dumps({'Secrets' : items}, indent=2))
            else:
                f.write(yaml.dump({'Secrets' : items}, indent=2))
            f.flush()
            if decrypt: 
                p = subprocess.Popen(["less", f.name])  ### TO-DO: make it platform agnostic
                p.wait()
            if not f == sys.stdout: f.close()
    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()
        print_output(Secrets.list(context, uninherited, decrypt))

    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise


###--------------------------------------------------------------------------------------------

@secret.command('get', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['secret']['get']}")
@click.option('-c', '--context', metavar='<stage>[/env]', default='default', help=f"{CLI_PARAMETERS_HELP['common']['context']}")
@click.argument('key', required=False)
@click.option('-k', '--key', 'key_option', required=False, metavar='<key>', help=f"{CLI_PARAMETERS_HELP['parameter']['key']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def get_secret(context, key, key_option, working_dir, config, verbosity):
    """
    Return the value of a secret in the application.\n
    """

    def check_command_usage():
        nonlocal context, key, key_option
        context = Contexts.normalize(context)
        if key and key_option:
            Logger.error(MESSAGES['ArgumentsMutualExclusive'].format("'key'", "'--key'"))
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)

        key = key or key_option

        if not key:
            Logger.error(MESSAGES['MissingArgument'].format("'KEY'"))
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)

    def print_output(output):
        with tempfile.NamedTemporaryFile("w") as f:
            f.write(str(output))
            f.flush()
            p = subprocess.Popen(["less", f.name])  ### TO-DO: make it platform agnostic
            p.wait()

    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()
        output = Secrets.get(context, key) 
        print_output(output)

    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise


###--------------------------------------------------------------------------------------------

@secret.command('add', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['secret']['add']}")
@click.option('-c', '--context', metavar='<stage>[/env]', default='default', help=f"{CLI_PARAMETERS_HELP['common']['context']}")
@click.argument('key', required=False)
@click.option('-k', '--key', 'key_option', required=False, metavar='<key>', help=f"{CLI_PARAMETERS_HELP['secret']['key']}")
# @click.option('-v', '--value', metavar='<value>', required=False, help=f"{CLI_PARAMETERS_HELP['secret']['value']}")
@click.option('-i', '--input', metavar='<path>', required=False, type=click.File('r'), help=f"{CLI_PARAMETERS_HELP['common']['input']}")
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml', 'shell']), default='shell', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def add_secret(context, key, key_option, input, format, working_dir, config, verbosity):
    """
    Adds a secret to the application, or updates its value if already existing.\n
    \tMultiple parmeters may be added at once from an input file using '-i' / '--input' option.
    """

    secrets = []

    def check_command_usage():
        nonlocal context, secrets, key, key_option
        context = Contexts.normalize(context)
        if input:
            if key or key_option:
                Logger.error(MESSAGES['ArgumentsMutualExclusive'].format("'-k' / '--key'","'-i' / '--input'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)
            if format == 'json':
                try:
                    secrets = json.load(input)['Secrets']
                # except json.JSONDecodeError as e:
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'yaml':
                try:
                    secrets = yaml.load(input, yaml.SafeLoader)
                # except yaml.YAMLError as e:
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'csv':
                try:
                    for secret in input.readlines():
                        _key = secret.split(',')[0]
                        _value = secret.split(',')[1]
                        secrets.append({'Key': _key, 'Value': _value})
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'shell':
                try:
                    for secret in input.readlines():
                        _key = secret.split('=', 1)[0].strip()
                        _value = secret.split('=', 1)[1].strip()
                        ### eat possible enclosing quotes and double quotes when source is file, stdin has already eaten them!
                        if re.match(r'^".*"$', _value):
                            _value = re.sub(r'^"|"$', '', _value)
                        elif re.match(r"^'.*'$", _value):
                            _value = re.sub(r"^'|'$", '', _value)
                        secrets.append({'Key': _key, 'Value': _value})
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
        ### not input
        else:
            if key and key_option:
                Logger.error(MESSAGES['ArgumentsMutualExclusive'].format("'key'", "'--key'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)
    
            key = key or key_option

            if not key:
                Logger.error(MESSAGES['AtleastOneofTwoNeeded'].format("'-k' / '--key'","'-i' / '--input'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)

            # if not value:
            #     Logger.error(MESSAGES['MissingOption'].format("'-v' / '--value'"))
            #     Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            #     exit(1)

            value = getpass("Enter secret value: ")
            value2 = getpass("Verify secret value: ")
            if not value == value2:
                Logger.error(MESSAGES['EnteredSecretValuesNotMatched'].format(f"'{format}'"))
                exit(1)

            secrets.append({'Key': key, 'Value': value})

        invalid = False
        for secret in secrets:
            invalid = not Secrets.validate_key(secret['Key']) or invalid

        if invalid:
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)

    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()

        for secret in secrets:
            key = secret['Key']
            value = secret['Value']
            Secrets.add(context, key, value)

    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise


###--------------------------------------------------------------------------------------------

@secret.command('delete', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['secret']['delete']}")
@click.option('-c', '--context', metavar='<stage>[/env]', default='default', help=f"{CLI_PARAMETERS_HELP['common']['context']}")
@click.argument('key', required=False)
@click.option('-k', '--key', 'key_option', metavar='<key>', required=False, help=f"{CLI_PARAMETERS_HELP['secret']['key']}")
@click.option('-i', '--input', metavar='<path>', required=False, type=click.File('r'), help=f"{CLI_PARAMETERS_HELP['common']['input']}")
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml', 'shell']), default='shell', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def delete_secret(key, key_option, input, format, context, working_dir, config, verbosity):
    """
    Delete a secret from the application.\n
    \tKEY: The key of the secret. It may also be provided via '-k' / '--key' option.\n
    \tMultiple secrets may be added at once from an input file using '-i' / '--input' option.
    """

    secrets = []

    def check_command_usage():
        nonlocal context, secrets, key, key_option
        context = Contexts.normalize(context)
        if input:
            if key or key_option:
                Logger.error(MESSAGES['ArgumentsMutualExclusive'].format("'-k' / '--key'","'-i' / '--input'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)
            if format == 'json':
                try:
                    secrets = json.load(input)['Secrets']
                # except json.JSONDecodeError as e:
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'yaml':
                try:
                    secrets = yaml.load(input, yaml.SafeLoader)['Secrets']
                # except yaml.YAMLError as e:
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'shell':
                try:
                    for secret in input.readlines():
                        _key = secret.split('=', 1)[0].strip()
                        # _value = secret.split('=', 1)[1].strip()
                        secrets.append({'Key': _key})
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'csv':
                try:
                    for param in input.readlines():
                        _key = param.split(',')[0].strip()
                        # _value = param.split('=', 1)[1].strip()
                        parameters.append({'Key': _key})
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
        ### not input
        else:
            if key and key_option:
                Logger.error(MESSAGES['ArgumentsMutualExclusive'].format("'key'", "'--key'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)
    
            key = key or key_option

            if not key:
                Logger.error(MESSAGES['AtleastOneofTwoNeeded'].format("'-k' / '--key'","'-i' / '--input'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)

            secrets.append({'Key': key})

        invalid = False
        for param in secrets:
            invalid = not Secrets.validate_key(param['Key']) or invalid

        if invalid:
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)

    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()

        for secret in secrets:
            Secrets.delete(context, secret['Key'])

    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise


###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

@template.command('list', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['template']['list']}")
@click.option('-r', '--render-path', 'show_render_path', required=False, is_flag=True, default=False, show_default=True, help=f"{CLI_PARAMETERS_HELP['template']['show_render_path']}")
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml']), default='csv', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def list_template(show_render_path, format, working_dir, config, verbosity):
    """
    Return the list of templates added to the application.\n
    """

    def check_command_usage():
        pass

    def print_output(templates):
        if show_render_path:
            if format == 'csv':
                for template in templates:
                    print(f"{template['Key']},{template['Render']}", flush=True)
            elif format == 'json':
                print(json.dumps({'Templates' : templates}, indent=2), flush=True)
            elif format == 'yaml':
                print(yaml.dump({'Templates' : templates}), flush=True)
        else:
            if format == 'shell':
                for item in templates:
                    print(f"{item['Key']}", flush=True)
            elif format == 'csv':
                for item in templates:
                    print(f"{item['Key']}", flush=True)
            elif format == 'json':
                print(json.dumps({'Templates' : [x['Key'] for x in templates]}, indent=2), flush=True)
            elif format == 'yaml':
                print(yaml.dump({'Templates' : [x['Key'] for x in templates]}), flush=True)

    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()
        templates = Templates.list()
        print_output(templates)
    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise


###--------------------------------------------------------------------------------------------

@template.command('get', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['template']['get']}")
@click.argument('key', required=False)
@click.option('-k', '--key', 'key_option', metavar='<key>', required=False, help=f"{CLI_PARAMETERS_HELP['template']['key']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def get_template(key, key_option, working_dir, config, verbosity):
    """
    Return the content of a template.\n
    \tKEY: The key of the template. It may also be provided via '-k' / '--key' option.\n
    """

    def check_command_usage():
        nonlocal key, key_option
        if key and key_option:
            Logger.error(MESSAGES['ArgumentsOrOption'].format("Template key", "'KEY'", "'--key'"))
            # Logger.info(MESSAGES['TryHelpWithCommand'].format('get parameter'), force=True, stress = False)
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)

        key = key or key_option

        if not key:
            Logger.error(MESSAGES['MissingOption'].format("'KEY"))
            # Logger.info(MESSAGES['TryHelpWithCommand'].format('get parameter'), force=True, stress = False)
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)


        if not Templates.validate_key(key):
            # Logger.info(MESSAGES['TryHelpWithCommand'].format('delete template'), force=True, stress = False)
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)


    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()
        print(Templates.get(key), flush=True)
    
    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise

###--------------------------------------------------------------------------------------------

@template.command('add', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['template']['add']}")
@click.argument('key', required=False)
@click.option('-k', '--key', 'key_option', metavar='<key>', required=False, help=f"{CLI_PARAMETERS_HELP['template']['key']}")
@click.option('-r', '--render-path', default='.', show_default=True, metavar='<path>', required=False, help=f"{CLI_PARAMETERS_HELP['template']['render_path']}")
@click.option('-i', '--input', metavar='<path>', required=True, type=click.File('r'), help=f"{CLI_PARAMETERS_HELP['common']['input']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def add_template(key, key_option, render_path, input, working_dir, config, verbosity):
    """
    Adds a template to the application, or updates the content if it is already existing.\n
    \tKEY: The key of the template. It may also be provided via '-k' / '--key' option.\n
    """

    content = ''

    def check_command_usage():
        nonlocal content, render_path
        if key and key_option:
            Logger.error(MESSAGES['ArgumentsOrOption'].format("'key'", "'--key'"))
            # Logger.info(MESSAGES['TryHelpWithCommand'].format('get parameter'), force=True, stress = False)
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)

        _key = key or key_option

        if not _key:
            Logger.error(MESSAGES['MissingArgument'].format("'KEY'"))
            # Logger.info(MESSAGES['TryHelpWithCommand'].format('get parameter'), force=True, stress = False)
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)

        if not Templates.validate_key(_key):
            # Logger.info(MESSAGES['TryHelpWithCommand'].format('delete template'), force=True, stress = False)
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)

        content = input.read()

    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()
        Templates.add(key, content, render_path)
    
    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise

###--------------------------------------------------------------------------------------------

@template.command('delete', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['template']['delete']}")
@click.argument('key', required=False)
@click.option('-k', '--key', 'key_option', metavar='<key>', required=False, help=f"{CLI_PARAMETERS_HELP['template']['key']}")
@click.option('-i', '--input', metavar='<path>', required=False, type=click.File('r'), help=f"{CLI_PARAMETERS_HELP['common']['input']}")
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml']), default='csv', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def delete_template(key, key_option, input, format, working_dir, config, verbosity):
    """
    Delete a template from the application.\n
    \tKEY: The key of the template. It may also be provided via '-k' / '--key' option.\n
    \tMultiple templates may be deleted at once from an input file using '-i' / '--input' option.
    """

    templates = []

    def check_command_usage():
        nonlocal templates
        if input:
            if key or key_option:
                Logger.error(MESSAGES['ArgumentsMutualExclusive'].format("'-k' / '--key'","'-i' / '--input'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)

            if format == 'json':
                try:
                    templates = json.load(input)['Templates']
                # except json.JSONDecodeError as e:
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'yaml':
                try:
                    templates = yaml.load(input, yaml.SafeLoader)['Parameters']
                # except yaml.YAMLError as e:
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
            elif format == 'csv':
                try:
                    for template in input.readlines():
                        _key = template.split(',')[0].strip()
                        # _value = param.split('=', 1)[1].strip()
                        templates.append({'Key': _key})
                except:
                    Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                    exit(1)
        ### not input
        else:
            if key and key_option:
                Logger.error(MESSAGES['ArgumentsMutualExclusive'].format("'key'", "'--key'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)
    
            _key = key or key_option

            if not _key:
                Logger.error(MESSAGES['AtleastOneofTwoNeeded'].format("'-k' / '--key'","'-i' / '--input'"))
                Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
                exit(1)

            templates.append({'Key': _key})

        invalid = False
        for template in templates:
            invalid = not Templates.validate_key(template['Key']) or invalid

        if invalid:
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)

    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()

        for template in templates:
            Templates.delete(template['Key'])
    
    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise

###--------------------------------------------------------------------------------------------

@template.command('render', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['template']['render']}")
@click.option('-c', '--context', metavar='<stage>[/env]', default='default', help=f"{CLI_PARAMETERS_HELP['common']['context']}")
@click.option('-l', '--limit', required=False, default='', help=f"{CLI_PARAMETERS_HELP['template']['limit']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def render_template(context, limit, working_dir, config, verbosity):
    """
    Render templates using parameters in a context.\n
    """

    def check_command_usage():
        pass

    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()

        rendered = Templates.render(context, limit)
        print(*rendered, sep='\n')

    
    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise


###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------
###--------------------------------------------------------------------------------------------

@package.command('list', context_settings=DEFAULT_CONTEXT, short_help="List available packages")
@click.argument('env')
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml']), default='csv', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def list_package(context, format, working_dir, config, verbosity):
    """
    Return the list of all available packages generated for a context.\n
    \tENV: Name of the environment
    """
    
    print(Packages.list(context))

###--------------------------------------------------------------------------------------------

@package.command('download', context_settings=DEFAULT_CONTEXT, short_help="Download a package")
@click.argument('env')
@click.argument('package')
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml']), default='csv', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def download_package(context, package, format, working_dir, config, verbosity):
    """
    Downlaod a package generated for a context.\n
    \tENV: Name of the environment\n
    \tPACKAGE: Version of the package to download
    """

    Packages.download(context, name)

###--------------------------------------------------------------------------------------------

@package.command('create', context_settings=DEFAULT_CONTEXT, short_help="Create a package")
@click.argument('env')
@click.argument('description', required=False)
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml']), default='csv', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def generate_package(context, verbosity, format, description=''):
    """
    Create a new build package for the application.\n
    \tENV: Name of the environment\n
    \tDESCRIPTION (optional): Description of the package
    """





###--------------------------------------------------------------------------------------------

@package.command('delete', context_settings=DEFAULT_CONTEXT, short_help="Delete a package")
@click.argument('env')
@click.argument('package')
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml']), default='csv', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def delete_package(context, package, format, working_dir, config, verbosity):
    """
    Delete a package from a context.\n
    \tENV: Name of the environment\n
    \tPACKAGE: Version of the package to be deleted
    """

    Packages.delete(context, name)


###--------------------------------------------------------------------------------------------

@release.command('list', context_settings=DEFAULT_CONTEXT, short_help="List available releases")
@click.argument('env')
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml']), default='csv', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def list_release(context, format, working_dir, config, verbosity):
    """
    Return the list of all available releases generated for a context.\n
    \tENV: Name of the environment
    """

    print(Releases.list(context))


###--------------------------------------------------------------------------------------------

@release.command('download', context_settings=DEFAULT_CONTEXT, short_help="Download a release")
@click.argument('env')
@click.argument('release')
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml']), default='csv', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def download_release(context, release, format, working_dir, config, verbosity):
    """
    Downlaod a release generated for a context.\n
    \tENV: Name of the environment\n
    \tRELEASE: Version of the release
    """

    Releases.download(context, release)

###--------------------------------------------------------------------------------------------

@release.command('create', context_settings=DEFAULT_CONTEXT, short_help="Create a release")
@click.argument('env')
@click.argument('package')
@click.argument('description', required=False)
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml']), default='csv', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def generate_release(context, verbosity, format, package, description=''):
    """
    Create a new release for a context.\n
    \tENV: Name of the environment\n
    \tPACKAGE: Version of the package to be used for creating the release\n
    \tDESCRIPTION (optional): Description of the release
    """

    Releases.generate(context, package, description)


###--------------------------------------------------------------------------------------------

@release.command('delete', context_settings=DEFAULT_CONTEXT, short_help="Delete a release")
@click.argument('env')
@click.argument('release')
@click.option('-f', '--format', required=False, type=click.Choice(['csv','json', 'yaml']), default='csv', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['format']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def delete_release(context, release, format, working_dir, config, verbosity):
    """
    Delete a release from a context.\n
    \tENV: Name of the environment\n
    \tRELEASE: Version of the release to be deleted
    """

    Releases.delete(context, release)

###--------------------------------------------------------------------------------------------

@config.command('get', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['config']['get']}")
@click.argument('key', required=False)
@click.option('-u','--uninherited', 'uninherited', is_flag=True, default=False, help=f"{CLI_PARAMETERS_HELP['config']['uninherited']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def get_config(key, uninherited, working_dir, config, verbosity):
    """
    Get DSO application configuration.\n
    \tKEY: The key of the configuration
    """

    def check_command_usage():
        pass

    def print_output(output):
        if not output: return
        if isinstance(output, dict):
            print(yaml.dump(output, indent=2), flush=True)
        else:
            print(output, flush=True)

    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()
        print_output(Config.get(key, uninherited))

    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise

###--------------------------------------------------------------------------------------------

@config.command('set', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['config']['set']}")
@click.argument('key', required=True)
@click.option('-v', '--value', metavar='<value>', required=False, help=f"{CLI_PARAMETERS_HELP['config']['value']}")
@click.option('-i', '--input', metavar='<path>', required=False, type=click.File('r'), help=f"{CLI_PARAMETERS_HELP['config']['input']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def set_config(key, value, input, working_dir, config, verbosity):
    """
    Set DSO application configuration.\n
    \tKEY: The key of the configuration
    """

    def check_command_usage():
        nonlocal value
        if value and input:
            Logger.error(MESSAGES['ArgumentsMutualExclusive'].format("'-v' / '--value'","'-i' / '--input'"))
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)

        if not (value or input):
            Logger.error(MESSAGES['AtleastOneofTwoNeeded'].format("'-v' / '--value'","'-i' / '--input'"))
            Logger.info(MESSAGES['TryHelp'], stress = False, force=True)
            exit(1)

        if input:
            try:
                value = yaml.load(input, yaml.SafeLoader)
            # except yaml.YAMLError as e:
            except:
                Logger.error(MESSAGES['InvalidFileFormat'].format(f"'{format}'"))
                exit(1)            

    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()
        Config.set(key, value)

    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise

###--------------------------------------------------------------------------------------------

@config.command('delete', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['config']['delete']}")
@click.argument('key', required=False)
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def delete_config(key, working_dir, config, verbosity):
    """
    Dlete a DSO application configuration.\n
    \tKEY: The key of the configuration
    """

    def check_command_usage():
        pass

    def print_output(output):
        pass

    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()
        Config.delete(key)

    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise

###--------------------------------------------------------------------------------------------

@config.command('setup', context_settings=DEFAULT_CONTEXT, short_help=f"{CLI_COMMANDS_SHORT_HELP['config']['setup']}")
@click.option('-w','--working-dir', metavar='<path>', type=click.Path(), required=False, default='.', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['working_dir']}")
@click.option('--config', metavar='<key>:<value>, ...', required=False, help=f"{CLI_PARAMETERS_HELP['common']['config']}")
@click.option('-b', '--verbosity', metavar='<number>', required=False, type=RangeParamType(click.INT, minimum=0, maximum=5), default='2', show_default=True, help=f"{CLI_PARAMETERS_HELP['common']['verbosity']}")
def setup_config(working_dir, config, verbosity):
    """
    Run a setup wizard to configure a DSO application.\n
    """

    def check_command_usage():
        pass

    try:
        Logger.set_verbosity(verbosity)
        Config.load(working_dir if working_dir else os.getcwd(), config)
        check_command_usage()


    except DSOException as e:
        Logger.error(e.message)
    except Exception as e:
        msg = getattr(e, 'message', getattr(e, 'msg', str(e)))
        Logger.critical(msg)
        if verbosity >= log_levels['full']:
            raise

###--------------------------------------------------------------------------------------------


if __name__ == '__main__':
    cli()

### Zsh workaround: Zsh puts args not passed asd $@ and starting with --/- first when calling the function via alias
### does not work for flag options!
if len(sys.argv)>3 and ( sys.argv[1].startswith('-') or sys.argv[1] == '--' ):
    sys.argv.append(sys.argv[1])  ### add --<option> to last
    sys.argv.append(sys.argv[2]) ### add value of the option to last
    sys.argv.pop(1)  ### remove original --<option>
    sys.argv.pop(1)  ### remove original value of the option

modify_click_usage_error()
