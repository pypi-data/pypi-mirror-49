#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: elastalk
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Simple Conveniences for Talking to Elasticsearch
"""
from .version import __version__, __release__
from .config import ElastalkConf, ElastalkConfigException
from .connect import ElastalkMixin
from .seed import seed
from .search import extract_hit, extract_hits
