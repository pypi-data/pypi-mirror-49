#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 1/23/19 by Pat Blair
"""
.. currentmodule:: elastalk.seed
.. moduleauthor:: Pat Daburu <pat@daburu.net>

Prepare your Elasticsearch store with seed data!
"""
import json
import logging
from pathlib import Path
import uuid
from .connect import ElastalkConnection
from .config import ElastalkConf

_logger: logging.Logger = logging.Logger(__file__)  #: the module logger


def seed(root: str or Path,
         config: str or Path = 'config.toml',
         force: bool = False):
    """
    Populate an Elasticsearch instance with seed data.

    :param root: the root directory that contains the seed data
    :param config: the path to the configuration
    :param force: delete existing indexes and replace them with seed data
    :raises FileNotFoundError: if the path does not exist
    :raises NotADirectoryError: if the path is not a directory
    """
    # Determine the root path.
    _root: Path = Path(root).resolve() if isinstance(root, str) else root

    # Let's figure out where the configuration file is supposed to be.
    _config: Path = config if isinstance(config, Path) else Path(config)
    # If we didn't get an absolute path...
    if not _config.is_absolute():
        _config = _root / _config  # ...assume the config path is in the root.
    _config = _config.resolve()

    # If the configuration file doesn't exist (or isn't a file), we have a
    # problem.
    if not _config.exists():
        raise FileNotFoundError(f"{_config} does not exist.")
    if not _config.is_file():
        raise FileNotFoundError(f"{_config} is a directory.")

    # Create the Elastalk configuration from the config file.
    etconf = ElastalkConf().from_toml(toml_=_config)
    # Create the Elastalk connection.
    etconn = ElastalkConnection(etconf)
    # Retrieve the client.
    es = etconn.client

    for idxdir in [d for d in _root.iterdir() if d.is_dir()]:
        # The name of the index directory is the name of the Elasticsearch
        # index.
        _index: str = idxdir.stem
        # If we've been instructed to *force* the seed data into the database...
        if force:  # ...drop the index.
            es.indices.delete(index=_index, ignore=[400, 404])
        elif es.indices.exists(index=_index):
            _logger.warning(
                f"Index '{_index}' already exists. Skipping."
            )
            continue
        # Each directory within the index directory indicates a "document type"
        # and contains files that will be converted to Elasticsearch documents.
        for docdir in [d for d in idxdir.iterdir() if d.is_dir()]:
            # The name of the document directory is the name of the
            # Elasticsearch document type.
            _doctype: str = docdir.stem
            # Now let's look at the files...
            for docfile in [f for f in docdir.iterdir() if f.is_file()]:
                # What do we thing the document ID should be?
                _id = docfile.name
                # If it is convertible to a UUID, it's a UUID...
                try:
                    _id = uuid.UUID(_id)
                except ValueError:  # pragma: no cover
                    pass  # ...but maybe not.  That's all right.
                # Prepare a document to index in Elasticsearch.
                doc = json.loads(docfile.read_text())
                # Index the document.
                es.index(
                    index=_index,
                    doc_type=_doctype,
                    id=_id,
                    body=etconn.pack(doc=doc, index=_index)
                )
