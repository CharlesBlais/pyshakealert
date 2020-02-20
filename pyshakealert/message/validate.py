'''
..  codeauthor:: Charles Blais
'''
import logging
import io
from pkg_resources import resource_filename

# Third-party module
from lxml import etree

# Constants
DEFAULT_DM_SCHEMA = resource_filename(
    'pyshakealert',
    'files/schemas/ShakeAlert_Message_v10_20191004.xsd')


def is_xml(content: bytes) -> bool:
    '''
    Is it an XML message

    :param bytes content: XML message
    :rtype: bool
    '''
    # First, try to parse the content
    try:
        etree.parse(io.BytesIO(content))
    # check for file IO error
    except IOError as err:
        logging.error("Invalid file sent to XML parser: %s", err)
        return False
    # check for XML syntax errors
    except etree.XMLSyntaxError as err:
        logging.error("Invalid XML syntax: %s", err)
        return False
    return True


def __validate_with_schema(
    content: bytes,
    schema: str
) -> bool:
    '''
    Is it an XML message according to a schema

    :param bytes content: XML message
    :param str schema: schema file
    :rtype: bool
    '''
    if not is_xml(content):
        return False
    # validate against schema
    try:
        xmlschema = etree.XMLSchema(etree.parse(open(schema)))
        doc = etree.parse(io.BytesIO(content))
        xmlschema.assertValid(doc)
    except etree.DocumentInvalid as err:
        logging.info("XML document does not match schema: %s", err)
        return False
    return True


def is_decision_module(
    content: bytes,
    schema: str = DEFAULT_DM_SCHEMA
) -> bool:
    '''
    Validate using schema for DM

    :param bytes content: XML message
    :param str schema: schema file
    :rtype: bool
    '''
    return __validate_with_schema(content, schema)
