import json
import datetime
import random
import string
import numpy as np
import subprocess
import os

def system(command):
    os.system(command)

def list_folders(root):
    commands = ["find", os.path.realpath(root), "-type","d"]
    results = subprocess.check_output(commands)
    return results.decode().split("\n")[1:]


def parent(path, level=1, sep="/", realpath=False):
    """
    Get the parent of a file or a directory

    :param path:
    :param level:
    :param sep:
    :return list:
    """
    path = os.path.realpath(path) if realpath else path
    def dir_parent(path, level=1):
        return sep.join(path.split(sep)[:-level])

    return [dir_parent(_path) for _path in path] if type(path) == list else dir_parent(path, level)


def replace_dir(dir_path):
    """
    Create a folder if it doesnt exist and remove its content

    :param dir_path:
    :return:
    """
    os.makedirs(dir_path, exist_ok=True)
    os.system("rm -r {}".format(dir_path))
    os.makedirs(dir_path, exist_ok=True)


def read_txt(filename_path, sep="\n"):
    """
    Read a text file and split by

    :param file:
    :return list:
    """
    lines = open(filename_path, "r").read().split(sep)
    return lines


def read_csv(filename_path, sep=","):
    """

    :param filename_path:
    :param sep:
    :return:
    """
    return [tuple(line.split("\n")[0].split(sep)) for line in open(filename_path, "r").readlines()]


def read_json(filename_path):
    """
    Read a json file

    :param filename_path:
    :return str:
    """
    with open(os.path.realpath(filename_path)) as label_file:
        return json.load(label_file)


def json_labels(labels_path, normalizer=None):
    """
    Read a json file to extract the labels in it

    :param labels_path:
    :param normalizer:
    :return list:
    """
    # Load the labels
    with open(os.path.realpath(labels_path)) as label_file:
        labels = str(' '.join(json.load(label_file)))
        labels = normalizer(labels) if normalizer is not None else labels
        labels = labels.split(" ")
        labels = [l for l in labels if len(l) > 0]
        labels.append(" ")
        return labels


def name(file, level=-1):
    """
    Get the name of a file and remove the extension
    :param file:
    :return string:
    """
    if file.split("/")[-1].__contains__("."):
        output = file.split("/")[-1]
        output = ".".join(output.split(".")[:level])
    else:
        output = file.split("/")[-1]
    return output


def check_files(dir, ext):
    """
    Check if files exist and have a non null size

    :param dir:
    :param ext:
    :return list:
    """
    files_audio_ids = [name(file) for file in os.listdir(dir) if ".{}".format(ext) in file]
    files_audio_ids = [name(file) for file in files_audio_ids
                       if os.path.getsize("{}/{}.{}".format(dir, file, ext)) > 0]
    return ["{}/{}.{}".format(dir, file, ext) for file in files_audio_ids]


def name_it(id, start, stop):
    """
    Automatically name a sound file with respect to (start, stop) slice audio

    :param id:
    :param start:
    :param stop:
    :return string:
    """
    return "{}_{}_{}_{}".format(id,
                                int(start * pow(10, 6)),
                                int(stop * pow(10, 6)),
                                int(stop - start))


def contain_filter(file, filters=None):
    """
    Check if a file contains one or many of the substrings specified in filters

    :param file:
    :param filters:
    :return bool:
    """
    if filters is None:
        return True
    for filter in filters:
        if len(file.split(filter)) >= 2:
            return True
    return False


def contain_ext(file, exts=None):
    """
    Check if a file contains a specific extension in a list of extensions

    :param file: file to scan
    :param exts: list of extensions
    :return bool:
    """
    if exts is None:
        return True
    return extension(file) in exts


def listfiles(root, patterns=[], excludes=[], exlude_hidden=False):
    """
    Similar to os.listdir but with more options in the search and a specific pattern

    :param root:
    :param patterns:
    :return:
    """
    def string_contains(text, patterns):
        for pattern in patterns:
            if text.__contains__(pattern):
                return True
        return False

    def fitler(file):
        try:
            assert len(file) > 0
            assert not file.__contains__("/.") if exlude_hidden else True
            assert not string_contains(file, excludes) if len(excludes)>0 else True
            assert string_contains(file, patterns) if len(patterns)>0 else True
            return True
        except AssertionError:
            return False

    commands = ["find", "-L", os.path.realpath(root)]
    results = subprocess.check_output(commands)
    files = results.decode().split("\n")[1:]
    files = [file for file in files if fitler(file)]
    return files


def inverse_dict(root=None, filters=None, array=None, exclude=None):
    """
    Inverse a dictionary of files

    :param root: directory to scan
    :param filters: filters or keywords to include in the search
    :param array:
    :param exclude: filterss or keywords to exclude in the search
    :return dict:
    """
    assert ((root is not None) | (array is not None))
    _idict = {}
    if array is not None:
        for f in array:
            _idict[name(f)] = parent(f)
    else:
        for dir, _, files in os.walk(root):
            condition = True
            if exclude is not None:
                if contain_filter(dir, exclude):
                    condition = False
            if condition:
                for file in files:
                    if ((contain_filter(file, filters)) | (filters is None)):
                        if exclude is None:
                            _idict[file] = dir
                        elif not contain_filter(file, exclude):
                            _idict[file] = dir
    return _idict


def ext(f):
    """
        Return the extension of a file

        :param f:
        :return string:
        """
    splits = f.split("/")[-1].split(".")
    return splits[1] if len(splits)==2 else ""


def extension(f):
    """
    Return the extension of a file

    :param f:
    :return string:
    """
    return ext(f)


def regroup(entries, index=0):
    """
    Convert an array into a dictionary by specifying a column index

    :param files:
    :param index:
    :return dictionary:
    """
    d = {}
    for f in entries:
        f = list(f)
        key = f[index]
        del f[index]
        try:
            d[key].append(f[:])
        except:
            d[key] = [f[:]]
    for key, values in d.items():
        d[key] = list(np.array(values).reshape(-1, ))
    return d


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Generate a random id

    :param size:
    :param chars:
    :return string:
    """
    return ''.join(random.choice(chars) for _ in range(size))


# Gather all files together
def regroup_by_parent(dir_data, patterns=["*"]):
    """
    Look for files with pattern in directoryu and regroup by parent directory

    :param dir_data:
    :param patterns:
    :return dictionary:
    """
    files = []
    for pattern in patterns:
        files = files + listfiles(root=dir_data, patterns=[pattern])
    data = {}
    for file in files:
        try:
            data[parent(file)].append(file)
        except:
            data[parent(file)] = [file]
    return data


def read(filename):
    """
    Generic reader.

    :param filename:
    :return:
    """
    if ext(filename) == "json":
        return read_json(filename)
    elif ext(filename) == "csv":
        return read_csv(filename)
    elif ext(filename) == "txt":
        return read_txt(filename, sep="\n")
    elif ext(filename) == "cfg":
        from iyo.utils import ConfigParser
        config = ConfigParser()
        config.read(filename)
        return config.convert_types("DEFAULT")


def download(url, filename):
    """
    Download and read a filename

    :param filename:
    :return:
    """
    output_dir = parent(filename)
    os.makedirs(output_dir, exist_ok=True)
    os.system("wget {} -P {}".format(url, output_dir))
    return read(filename)



def timedelta(string):
    """

    :param string:
    :return:
    """
    splits = np.array(string.split(":"), dtype=int)
    return datetime.timedelta(hours=int(splits[0]), minutes=int(splits[1]), seconds=int(splits[2]))


def find_in_file(file, text):
    try:
        matches=[]
        for k, line in enumerate(open(file, "r").readlines()):
            if len(line.split(text))>1:
                matches.append(k)
        return (matches, file) if len(matches)>0 else None
    except:
        pass
