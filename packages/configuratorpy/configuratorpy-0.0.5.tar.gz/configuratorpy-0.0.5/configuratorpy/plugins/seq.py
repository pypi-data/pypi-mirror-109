################################################################################
#                                                                              #
#      This is the plugin which will provide the functions for sequences       #
#                                                                              #
#                    @author Jack <jack@thinkingcloud.info>                    #
#                                 @version 1.0                                 #
#                          @date 2021-06-02 11:41:53                           #
#                                                                              #
################################################################################

import uuid
import os
import jinja2
from jinja2 import nodes, TemplateSyntaxError
from jinja2.ext import Extension
from jinja2.nodes import Const
import logging

logger = logging.getLogger(__name__)

seqs = {}


def seq(name):
    global seqs
    if name not in seqs:
        seqs[name] = 0
    seqs[name] += 1
    return seqs[name]


class SeqExtension(Extension):
    tags = {'seq'}

    def __init__(self, environment):
        super(SeqExtension, self).__init__(environment)

    def parse(self, parser):
        line_number = next(parser.stream).lineno
        expr = [Const('')]
        body = ''
        try:
            expr = [parser.parse_expression()]
        except TemplateSyntaxError:
            expr = parser.parse_statements(
                ['name:endseq'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_get_seq', expr), [], [], body).set_lineno(line_number)

    def _get_seq(self, name, caller):
        return str(seq(name))


class UUIDExtension(Extension):
    tags = {'uuid'}

    def __init__(self, environment):
        super(UUIDExtension, self).__init__(environment)

    def parse(self, parser):
        line_number = next(parser.stream).lineno
        expr = [Const('')]
        body = ''
        try:
            expr = [parser.parse_expression()]
        except TemplateSyntaxError:
            expr = parser.parse_statements(
                ['name:enduuid'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_get_uuid', expr), [], [], body).set_lineno(line_number)

    def _get_uuid(self, body, caller):
        return str(uuid.uuid4())


jinja2.filters.FILTERS['seq'] = seq
