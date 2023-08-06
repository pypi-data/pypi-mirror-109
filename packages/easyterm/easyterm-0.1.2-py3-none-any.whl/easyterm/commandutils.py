import os, hashlib, subprocess
from .commandlineopt import NoTracebackError
__all__ = ["md5sum_of_file", "check_file_presence"]

def md5sum_of_file(filename, chunksize=4096):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(chunksize), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def check_file_presence(input_file, descriptor='input_file', exception_raised=NoTracebackError):
    """ Check if file exists. If it doesn't, raises a IOError exception

    Args:
     input_file (str):   string of file to check, any relative or absolute path
     descriptor (str):   used for meaningful error message if file is present
     exception_raised (class): Exception class to be raised
    """
    if not input_file or not os.path.isfile(input_file):
        raise(exception_raised(f"ERROR {descriptor}: {input_file} not defined or not found. Run with option -h for help."))
