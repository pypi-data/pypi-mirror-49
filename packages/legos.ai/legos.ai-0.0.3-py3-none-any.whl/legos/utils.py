import os
import re
import gzip
from pathlib import Path
import tempfile
import tarfile
import zipfile

def num_cpus():
    cpus = os.cpu_count()
    if cpus is None:
        return 1
    return cpus

def camel2snake(name):
    """
    Convert Camel Case to Snake Case. Source: https://stackoverflow.com/a/1176023
    Example:
    LoggerCallback -> logger_callback
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def ifnone(a, b):
    return b if a is None else a

def get_temp_dir_path():
    return Path(tempfile.gettempdir())

def is_notebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook, Spyder or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

def _is_tar(filename):
    return filename.endswith(".tar")

def _is_targz(filename):
    return filename.endswith(".tar.gz")

def _is_gzip(filename):
    return filename.endswith(".gz") and not filename.endswith(".tar.gz")

def _is_zip(filename):
    return filename.endswith(".zip")

def extract_archive(from_path, to_path=None, remove_finished=False):
    if to_path is None:
        to_path = os.path.dirname(from_path)

    if _is_tar(from_path):
        with tarfile.open(from_path, 'r') as tar:
            tar.extractall(path=to_path)
    elif _is_targz(from_path):
        with tarfile.open(from_path, 'r:gz') as tar:
            tar.extractall(path=to_path)
    elif _is_gzip(from_path):
        to_path = os.path.join(to_path, os.path.splitext(os.path.basename(from_path))[0])
        with open(to_path, "wb") as out_f, gzip.GzipFile(from_path) as zip_f:
            out_f.write(zip_f.read())
    elif _is_zip(from_path):
        with zipfile.ZipFile(from_path, 'r') as z:
            z.extractall(to_path)
    else:
        raise ValueError("Extraction of {} not supported".format(from_path))

    if remove_finished:
        os.remove(from_path)

def to_path(path):
    if not isinstance(path, Path):
        path = Path(path)
    return path