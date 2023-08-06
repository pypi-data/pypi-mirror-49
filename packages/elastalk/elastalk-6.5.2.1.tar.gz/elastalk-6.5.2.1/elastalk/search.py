#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 7/24/19 by Pat Daburu
"""
.. currentmodule:: elastalk.search
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This module contains functions you can use when dealing with
`Elasticsearch documents <https://bit.ly/2YcMds5>`_ returned by searches.
"""
from typing import Any, Iterable, Mapping, Tuple
import uuid

ID_FIELD = '_id'  #: the standard name of the ID field


def extract_hit(
        hit: Mapping[str, Any],
        includes: Tuple[str] = (ID_FIELD,),
        source: str = '_source'
) -> Mapping[str, Any]:
    """
    Extract a document from a single search result hit.

    :param hit: the search hit document
    :param includes: the metadata keys to include in the return document
    :param source: the key that contains the source document
    :return:
    """
    doc = {
        **{
            k: hit.get(k) for k in includes
        },
        **hit.get(source)
    }
    # If the document ID is included...
    if ID_FIELD in doc:
        # ...convert it to a UUID.
        doc[ID_FIELD] = uuid.UUID(doc.get(ID_FIELD))
    return doc


def extract_hits(
        result: Mapping[str, Any],
        includes: Tuple[str] = (ID_FIELD,),
        source: str = '_source'
) -> Iterable[Mapping[str, Any]]:
    """
    Extract documents from a search result.

    :param result: the search result document
    :param includes: the metadata keys to include in the return document
    :param source: the key that contains the source document
    :return: an iteration of search result documents
    """
    hits = result.get('hits', {}).get('hits', [])
    for hit in hits:
        yield extract_hit(hit, includes=includes, source=source)
