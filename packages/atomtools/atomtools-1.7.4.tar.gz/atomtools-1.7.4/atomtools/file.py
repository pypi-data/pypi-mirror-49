"""

atomtools.file

process all file related



fileobj is frequently used
fileobj could be a StringIO, a string
extension is a string ".xxxx"
"""


import os
import shutil
import time
from io import StringIO
import chardet
from .name import randString


MAX_FILENAME_LENGTH = 200
MAX_DETECT_LENGTH = 300000
MAX_ACTIVE_TIME = 3600


def get_file_extension(filename):
    return os.path.splitext(get_absfilename(filename))[-1]

def get_file_basename(filename):
    return os.path.splitext(get_absfilename(filename))[0]

def get_file_content(fileobj):
    """
    get content of fileobj
    """
    if hasattr(fileobj, 'read'):
        fileobj.seek(0)
        return fileobj.read().replace('\r', '')
    elif isinstance(fileobj, str):
        if len(fileobj) < MAX_FILENAME_LENGTH and os.path.exists(fileobj): # a filename
            with open(fileobj, 'rb') as fd:
                data = fd.read()
            code = chardet.detect(data[:MAX_DETECT_LENGTH])['encoding']
            return data.decode(code).replace('\r', '')
        else:
            return fileobj
    else:
        raise ValueError('fileobj should be filename/filecontent/StringIO object')


def get_absfilename(fileobj):
    if hasattr(fileobj, 'read'):
        return os.path.realpath(fileobj.name) if hasattr(fileobj, 'name') else None
    elif isinstance(fileobj, str):
        if len(fileobj) < MAX_FILENAME_LENGTH:
            return os.path.realpath(fileobj)
        else:
            return None # a string has no filename
    else:
        import pdb; pdb.set_trace()
        raise ValueError('fileobj should be filename/filecontent/StringIO object')


def get_filename(fileobj):
    return os.path.basename(get_absfilename(fileobj))


def get_file_basename(fileobj):
    return os.path.splitext(get_filename(fileobj))[0]



def get_extension(fileobj):
    filename = get_absfilename(fileobj)
    if filename is None:
        return None
    return os.path.splitext(filename)[-1]



def get_time_since_lastmod(filename):
    filename = get_filename(filename)
    if not os.path.exists(filename):
        return 0
    return time.time() - os.stat(filename).st_mtime



def file_active(filename):
    filename = get_absfilename(filename)
    lastmod = get_time_since_lastmod(filename)
    if lastmod > MAX_ACTIVE_TIME:
        return False
    return True



def file_exist(filename):
    filename = get_filename(filename)
    if filename is None:
        return False
    return os.path.exists(filename)


TMP_DIR = '/tmp/atomtools_{0}'.format(randString())
compress_command = {
    '.xz' : 'xz -d -f',
    '.zip' : 'unzip',
    '.gz' : 'gzip -d ',
    '.Z' : 'uncompress',
    '.bz2' : 'bzip2 -d',
    '.bz' : 'bzip2 -d',
    '.rar' : 'rar x',
    '.lha' : 'lha -e',
}


def get_uncompressed_fileobj(filename):
    filename = get_absfilename(filename)
    extension = get_file_extension(filename)
    if not extension in compress_command:
        return filename

    cmd = compress_command[extension]
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
    tmpfilename = os.path.join(TMP_DIR, os.path.basename(filename))
    newfilename = os.path.splitext(tmpfilename)[0]
    shutil.copyfile(os.path.abspath(filename), tmpfilename)
    cmd += ' ' + tmpfilename + '; dos2unix {0} > /dev/null 2>&1 '.format(newfilename)
    os.system(cmd)
    with open(newfilename) as fd:
        fileobj = StringIO(fd.read())
        fileobj.name = os.path.basename(newfilename)
    os.remove(newfilename)
    try:
        shutil.rmtree(TMP_DIR)
    except:
        pass
    return fileobj


def get_uncompressed_filename(filename):
    return get_file_basename(filename)



def is_compressed_file(filename):
    if os.path.exists(filename) and get_file_extension(filename) in compress_command:
        return True
    return False


