################################################################################
#                                                                              #
#                      This is the module for the models.                      #
#                                                                              #
#                    @author Jack <jack@thinkingcloud.info>                    #
#                                 @version 1.0                                 #
#                          @date 2021-05-31 14:15:26                           #
#                                                                              #
################################################################################

import os
from os import path
import logging
from .exceptions import *
from .helpers import load_class
import toml
from benedict import benedict
import dpath.util
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)


class Configurator:
    name: str = None
    directory: str = None
    config_data: dict = None
    template: any = None
    env: Environment = None
    plugins: list = ['.plugins.EnvExtension',
                     '.plugins.UUIDExtension', '.plugins.SeqExtension']
    """
    This is the model for the configurator
    """

    def __init__(self,
                 name: str = 'config.toml',
                 directory: str = None,
                 plugins: list = None, load=True):
        self.name = name
        if plugins:
            self.plugins += plugins
        if not directory or not path.exists(directory):
            # If no directory is set, or it is not exists, will use current directory
            self.directory = os.getcwd()
            logger.info(
                'Directory %s is not set or not exists, will use current directory %s instead',
                directory, self.directory)
        else:
            self.directory = directory

        if not path.exists(self.filename):
            raise ConfigNotExistsException(
                f'Configuration file {self.filename} not exists!')
        if load:
            self.load()

    def __getitem__(self, name):
        return self.get(name)

    def get(self, name, default=None):
        if not self.config_data:
            raise ConfigNotLoadException(
                f'Configuration file {self.filename} is not loaded!')

        if '/' in name or '*' in name:
            vs = dpath.util.values(self.config_data, name)
            if len(vs) == 1:
                return vs[0]
            return vs
        return self.config_data.get(name, default)

    def sub(self, name):
        c = Configurator(self.name, directory=self.directory, load=False)
        c.config_data = benedict(self[name])
        return c

    def search(self, query, **kwargs):
        return dpath.util.search(self.config_data, query, **kwargs)

    @property
    def filename(self):
        return path.join(self.directory, self.name)

    def to_dict(self):
        return self.config_data

    def load(self):
        # Let's load all plugins
        context = {}

        extensions = []
        if not self.env:
            for plugin in self.plugins:
                p = load_class(plugin)
                if p:
                    extensions.append(p)
            self.env = Environment(loader=FileSystemLoader(
                self.directory), extensions=extensions)

        if not self.template:
            self.template = self.env.get_template(self.name)
        self.config_data = benedict(toml.loads(self.template.render()))
