"""
analyze chemical input/output filetype 
"""


import os
import re
import configparser
import atomtools


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FILETYPE_REGEXP_CONF = 'default_filetype.conf'
DEFAULT_FILETYPE_REGEXP_CONF = os.path.join(BASE_DIR, DEFAULT_FILETYPE_REGEXP_CONF)
REG_ANYSTRING = r'[\s\S]*?'
FILETYPE_SECTION_NAME = 'filetype'
MULTIFRAME_NAME = 'multiframe'



global FORMATS_REGEXP, MULTIFRAME
FORMATS_REGEXP, MULTIFRAME = dict(), list()


def update_config(path=None):
    global FORMATS_REGEXP, MULTIFRAME
    path = path or DEFAULT_FILETYPE_REGEXP_CONF
    if os.path.exists(path):
        conf = configparser.ConfigParser(delimiters=('='))
        conf.optionxform=str
        conf.read(path)
        FORMATS_REGEXP.update(conf._sections[FILETYPE_SECTION_NAME])
        MULTIFRAME += conf._sections[MULTIFRAME_NAME][MULTIFRAME_NAME].split()


def filetype(fileobj=None, isfilename=False, debug=False):
    """
    >>> filetype("a.gjf")
    gaussian
    >>> filetype("1.gro")
    gromacs
    """
    filename = atomtools.file.get_absfilename(fileobj)
    if atomtools.file.is_compressed_file(filename):
        fileobj = atomtools.file.get_uncompressed_fileobj(filename)
        filename = atomtools.file.get_uncompressed_filename(filename)
    else:
        filename = atomtools.file.get_filename(fileobj)
    content = atomtools.file.get_file_content(fileobj)
    if filename is None and content is None:
        return None
    for fmt_regexp, fmt_filetype in FORMATS_REGEXP.items():
        name_regexp, content_regexp = (fmt_regexp.split('&&') + [None])[:2]
        if debug:
            print(name_regexp, content_regexp)
        if filename and re.match(re.compile(name_regexp.strip()), filename) or filename is None:
            if content and content_regexp:
                if not content_regexp.startswith('^'):
                    content_regexp = REG_ANYSTRING + content_regexp.strip() 
                if not content_regexp.endswith('$'):
                    content_regexp = content_regexp.strip() + REG_ANYSTRING
                if debug:
                    print(content_regexp)
                    import pdb; pdb.set_trace()
                if re.match(re.compile(content_regexp.strip()), content):
                    return fmt_filetype
            else:
                return fmt_filetype
    return None


def list_supported_formats():
    return list(FORMATS_REGEXP.values())


def support_multiframe(ftype):
    if ftype in MULTIFRAME:
        return True
    return False


update_config()



