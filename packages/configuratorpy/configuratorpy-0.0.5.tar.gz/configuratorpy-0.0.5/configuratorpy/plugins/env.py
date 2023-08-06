################################################################################
#                                                                              #
#                 This is the plugin for environment variables                 #
#                                                                              #
#                    @author Jack <jack@thinkingcloud.info>                    #
#                                 @version 1.0                                 #
#                          @date 2021-05-31 15:33:20                           #
#                                                                              #
################################################################################

import os
from dotenv import load_dotenv
from contextlib import suppress
import jinja2
from jinja2 import nodes, TemplateSyntaxError
from jinja2.ext import Extension
from jinja2.nodes import Const
import logging

logger = logging.getLogger(__name__)


def load_env(path=None):
    load_dotenv(verbose=True, dotenv_path=path)


def env(key, default=''):
    return os.getenv(key, default=default)


jinja2.filters.FILTERS['env'] = env


class EnvExtension(Extension):
    tags = {'loadenv'}

    def __init__(self, environment):
        super(EnvExtension, self).__init__(environment)

    def parse(self, parser):
        line_number = next(parser.stream).lineno
        file = [Const('')]
        body = ''
        try:
            file = [parser.parse_expression()]
        except TemplateSyntaxError:
            file = parser.parse_statements(
                ['name:endloadenv'], drop_needle=True)
        load_env(file[0].value)
        return nodes.CallBlock(self.call_method('_load_env', file), [], [], body).set_lineno(line_number)

    def _load_env(self, file, caller):
        return ''
