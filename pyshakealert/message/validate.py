"""
..  codeauthor:: Charles Blais
"""
import logging
import io

# Third-party module
from lxml import etree

from pyshakealert.config import get_app_settings


def is_xml(content: bytes) -> bool:
    """
    Is it an XML message

    :param bytes content: XML message
    :rtype: bool
    """
    # First, try to parse the content
    try:
        etree.parse(io.BytesIO(content))
    # check for file IO error
    except IOError as err:
        logging.error(f'Invalid file sent to XML parser: {err}')
        return False
    # check for XML syntax errors
    except etree.XMLSyntaxError as err:
        logging.error(f'Invalid XML syntax: {err}')
        return False
    return True


def _validate_with_schema(
    content: bytes,
    schema: str
) -> bool:
    """
    Is it an XML message according to a schema

    :param bytes content: XML message
    :param str schema: schema file
    :rtype: bool
    """
    if not is_xml(content):
        return False
    # validate against schema
    try:
        xmlschema = etree.XMLSchema(etree.parse(open(schema)))
        doc = etree.parse(io.BytesIO(content))
        xmlschema.assertValid(doc)
    except etree.DocumentInvalid as err:
        logging.info(f'XML document does not match schema: {err}')
        return False
    return True


def is_decision_module(
    content: bytes,
) -> bool:
    """
    Validate using schema for DM

    :param bytes content: XML message
    :param str schema: schema file
    :rtype: bool
    """
    settings = get_app_settings()
    return _validate_with_schema(content, settings.dm_schema)
