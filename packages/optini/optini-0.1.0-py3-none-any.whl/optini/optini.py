import argparse
import configparser
import copy
import logging
import os
import typing

import attr
from dotmap import DotMap

opt = DotMap()

LOGGINGSPEC = {
    # verbose corresponds to INFO log level
    'verbose': {
        'help': 'report performed actions',
    },
    'debug': {
        'help': 'report planned actions and diagnostics',
    },
    'quiet': {
        'help': 'avoid all non-error console output',
    },
    'Log': {
        'help': 'log output to logfile (see File4log option)',
    },
    'File4log': {
        'type': str,
        'help': 'log file',
        'default': 'optini.log',
    },
}

########################################################################

@attr.s(auto_attribs=True)
class Config:
    '''
    Class to get options from command line and config file

    - The hierarchy is: command line args > config file > defaults
    - Based on those inputs, Config constructs a DotMap object
        - Interface is a module-level variable: optini.opt
        - Access specific config options using DotMap attributes
        - Example: optini.opt.verbose
    - Config derives command line options from option names
        - Example: "verbose" => -v and --verbose
    - Most method operations occur during construction (consider "private")

    Examples
    --------

    .. code-block:: python

      import optini
      spec = {
          'someopt': {
              'help': 'set a flag',
          },
      }
      # implies -s and --someopt command line options
      confobj = optini.Config(spec=spec, file=True)
      if optini.opt.someopt:
          print("someopt flag is set")

    This defines one boolean option, someopt, which defaults to false;
    users can specify -s at the command line, or put someopt = true in
    the config file.

    Attributes
    ----------

    description : str
        if not None, optini will use this in argparse usage message
    file : str
        if not None, optini will use this file as config file
    logging : bool (default: False)
        incorporate logging config, with (mostly) conventional options
            (-v, -d, -q, -L, -F LOGFILE)
    skeleton : bool (default: True)
        whether to create a default config file or not
    spec : dict of dicts
        a nested dictionary specifying option configuration

    Option Specification Format
    ---------------------------

    - Specify options by passing a dict of dicts (the spec attribute)
    - The top level key is the option name
    - optini recognizes the following second-level keys:
        - help : str
            - for argparse usage message, default config file comments
        - type : type
            - type hint for parsers (default is bool)
        - default
            - the default value for the option
        - configfile : bool
            - Specify False for command line only options
        - short : str
            - Short form command line option (example: -v)
        - long : str
            - Long form command line option (example: --verbose)

    Logging
    -------

    Config has special support for configuring the standard logging
    module using several (mostly) conventional options controlling
    logs and verbosity (-v, -d, -q, -L and -F). Note: 'verbose' (-v)
    corresponds to the INFO log level. If you set the appname attribute,
    optini will derive the default log file name from appname (by
    appending .log).

    .. code-block:: python

      import optini
      confobj = optini.Config(logging=True)

    In this example, -L will enable logging to file for the application.
    The user can override the default logfile using -F newfile.

    Example way to use the logging support:

    .. code-block:: python

        import os
        myself = os.path.basename(__FILE__)
        import optini
        # ...
        confobj = optini.Config(logging=True, appname=myself)

    '''
    appname: str
    description: str = None
    file: bool = False
    filename: str = None
    logging: bool = False
    skeleton: bool = True
    spec: typing.Dict = attr.Factory(dict)

    def __attrs_post_init__(self):
        self.merge_spec()
        self.set_default_config()
        self.parse_config_file()
        self.parse_args()
        self.merge()
        self.configure_logging()

    def configure_logging(self):
        if not self.logging:
            return

        # numeric log levels, according to logging module:
        # CRITICAL 50, ERROR 40, WARNING 30, INFO 20, DEBUG 10, NOTSET 0

        # by default, only show warning and higher messages
        loglevel = logging.WARNING
        if opt.verbose:
            loglevel = min(loglevel, logging.INFO)
        if opt.debug:
            loglevel = min(loglevel, logging.DEBUG)

        handlers = []
        if not opt.quiet:
            handlers.append(logging.StreamHandler())
        if opt.Log:
            handlers.append(logging.FileHandler(opt.File4log))

        if self.appname is not None:
            format = f"{self.appname}: %(levelname)s: %(message)s"
        else:
            format = f"%(levelname)s: %(message)s"

        logging.basicConfig(
            level=loglevel,
            handlers=handlers,
            format=format,
        )

        if opt.Log:
            logging.info(f"logging to {opt.File4log}")

    def configfile(self):
        'generate sample config file showing default values'
        contents = []
        contents.append(f"# configuration file\n")
        for option in self.optspec:
            # ignore options marked as not for config file
            if 'configfile' in self.optspec[option]:
                if not self.optspec[option].configfile:
                    continue
            lhs = option
            if 'default' in self.optspec[option]:
                if type(self.optspec[option].default) is bool:
                    rhs = str(self.optspec[option].default).lower()
                else:
                    rhs = self.optspec[option].default
            else:
                if self.optspec[option].type is bool:
                    rhs = 'false'
                else:
                    rhs = "''"
            if 'help' in self.optspec[option]:
                contents.append(f"# {self.optspec[option].help}")
            contents.append(f"#{lhs} = {rhs}\n")
        return('\n'.join(contents))

    def merge_spec(self):
        'determine and augment option specification'
        # option specification, DotMap form
        # we will iterate over self.spec to create this
        self.optspec = DotMap()

        if self.appname is not None:
            # update option specification for logfile
            logfile = f"{self.appname}.log"
            LOGGINGSPEC['File4log'] = {
                'type': str,
                'help': f"log file (default: {logfile})",
                'default': f"{logfile}",
            }
        if self.logging:
            self.spec = {**self.spec, **LOGGINGSPEC}

        # running example: {'someopt': {'help': 'some help info'}}
        for name, spec in DotMap(self.spec).items():
            # example: name = 'someopt', spec = {'help': 'some help info'}
            if 'type' not in spec:
                # no type specified, default to bool
                spec.type = bool
            if spec.type is bool:
                if 'action' not in spec:
                    spec.action = 'store_true'
                    # 'count' would be another reasonable possibility
                if 'default' not in spec:
                    spec.default = False
            else:
                if 'default' not in spec:
                    spec.default = None
            self.optspec[name] = spec

    def set_default_config(self):
        'derive default config from option specification'
        # self.opt will be the final options specified by user
        self.opt = DotMap()
        for name, spec in self.optspec.items():
            # after merge_spec(), all items should have a default
            self.opt[name] = spec.default

    def parse_config_file(self):
        'parse config file, if config files are enabled'
        # support options without an ini section header
        # that is, prepend an implicit default [optini] section
        config_file_content = '[optini]\n'

        self.configparser = configparser.ConfigParser(allow_no_value=True)

        # if config files are enabled
        if self.file:
            if self.filename is None:
                # default config file = $HOME/.<appname>.ini
                home = os.environ['HOME']
                self.filename = f"{home}/.{self.appname}.ini"
            if self.skeleton:
                if not os.path.exists(self.filename):
                    # create a skeleton config file
                    open(self.filename, 'w').write(self.configfile())
            with open(self.filename) as f:
                config_file_content += f.read()
            self.configparser.read_string(config_file_content)

    def parse_args(self):
        'parse command line arguments'
        parser = argparse.ArgumentParser(description=self.description)

        # derive add_argument kwargs from option specification
        for name, spec in self.optspec.items():
            kwargs = copy.deepcopy(spec)
            # ignore invalid argparse keys
            # (added optini functionality)
            kwargs.pop('configfile')
            kwargs.pop('type')

            # short and long need to be here, because:
            # - they are not argpase keys like 'action' or 'help'
            # - instead, they are passed as separate initial arguments

            # short option form defaults to first character of option name
            if 'short' in kwargs:
                short = kwargs.pop('short')
            else:
                short = f"-{name[0:1]}"

            # long option form defaults to --option name
            if 'long' in kwargs:
                long = kwargs.pop('long')
            else:
                long = f"--{name}"

            parser.add_argument(long, short, **kwargs.toDict())

        self.argparser = parser
        self.parsed_args, self.unparsed_args = self.argparser.parse_known_args()
        # save the Namespace as a DotMap as well
        self.args_vars = DotMap(vars(self.parsed_args))

    def merge(self):
        'merge command line, config file, and default options'
        for name, spec in self.optspec.items():
            # if one of the options was set in the config file
            # 'optini' is the default implicit section name
            section = self.configparser['optini']
            if name in section:
                # ignore options marked as not for config file
                if 'configfile' in spec and not spec.configfile:
                    continue

                if spec.type is str:
                    self.opt[name] = section.get(name)
                    #self.configparser['optini'].get(name)
                elif spec.type is int:
                    self.opt[name] = section.getint(name)
                elif spec.type is float:
                    self.opt[name] = section.getfloat(name)
                elif spec.type is bool:
                    self.opt[name] = section.getboolean(option)
                else:
                    raise Exception(f"error processing {name}")

            # command line argument override
            if name in self.args_vars and self.args_vars[name] is not None:
                if self.optspec[name].type is int:
                    # attempt to convert value to int
                    try:
                        self.opt[name] = int(self.args_vars[name])
                    except Exception as e:
                        raise(e) # yyy improve this
                if self.optspec[name].type is float:
                    # attempt to convert value to float
                    try:
                        self.opt[name] = float(self.args_vars[name])
                    except Exception as e:
                        raise(e) # yyy improve this
                else:
                    # argparse can handle string and boolean
                    self.opt[name] = self.args_vars[name]
        global opt
        opt = self.opt

    def __str__(self):
        ret = [f"options from config file ({self.file}):"]
        for section in self.configparser.sections():
            ret.append(f"config file section: {section}")
            for option in self.configparser.options(section):
                optval = self.configparser.get(section, option)
                ret.append(f"  {option} = {optval}")
        ret.append("\noptions from command line:")
        ret.append(str(self.args_vars))
        ret.append("\nconfigured options:")
        ret.append(str(self.opt))
        return("\n".join(ret))

# task: argparse help hint for non configfile options (asterisks?)
# task: support option group aliases (so -a could be -TyhG)
# task: incorporate type=argparse.FileType("r")
# task: maybe support yaml spec input (what about embedded python objects?)
