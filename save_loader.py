import argparse
import base64
import gzip
import io
import json
import os.path as op
import shutil
import struct


SAVEFILE_NAME = 'SaveData'
SAVEDATA_BAK = 'SaveData.bak'
EXPORT_NAME = 'SaveData.json'


def load(fname):
    """ Load a Kamiko save file. """
    _fname = fname or SAVEFILE_NAME
    with open(_fname, 'rb') as fobj:
        decoded = base64.b64decode(fobj.read())
    # Strip the first 4 bytes as they are just the size of the decompressed
    # data.
    decoded = decoded[4:]
    # decompress to get the raw data
    data = gzip.decompress(decoded).decode()
    # now load
    savedata = {}
    _savedata = json.loads(data)
    # The keys are also serialized so need to be loaded using .loads again.
    for key, value in _savedata.items():
        savedata[key] = json.loads(value)
    with open(EXPORT_NAME, 'w') as fout:
        json.dump(savedata, fout, indent=4)
    print('Decompiling: {0} -> {1}'.format(_fname, EXPORT_NAME))


def save(fname):
    """ Convert a json-format Kamiko save file into the file that can be read
    by the game. """
    _fname = fname or EXPORT_NAME
    # Load the file into a dictionary
    with open(_fname, 'r') as fobj:
        _savedata = json.load(fobj)
    # Serialize the values
    savedata = {}
    for key, value in _savedata.items():
        savedata[key] = json.dumps(value, separators=(',', ':'))
    # Then write the data into a bytes object
    data = json.dumps(savedata, separators=(',', ':')).encode()
    # Create buffers for the gzip data and the actual final
    gzipbuf = io.BytesIO()
    gzipbuf.write(struct.pack('<I', len(data)))
    with gzip.GzipFile(compresslevel=6, mtime=0, mode='wb',
                       fileobj=gzipbuf) as gzipobj:
        gzipobj.write(data)
    gzipbuf.seek(0xD)
    gzipbuf.write(b'\x0A')

    # Encode the data in base64
    encoded = base64.b64encode(gzipbuf.getvalue())

    # If there is no save data backup, create one
    if not op.exists(SAVEDATA_BAK):
        shutil.copy(SAVEFILE_NAME, SAVEDATA_BAK)
    with open(SAVEFILE_NAME, 'wb') as fout:
        fout.write(encoded)
    print('Recompiling: {0} -> {1}'.format(_fname, SAVEFILE_NAME))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--load",
                       help="Loads SaveData and saves it as SaveData.json",
                       action="store_true")
    group.add_argument("-s", "--save",
                       help="Loads SaveData.json and recompiles it into "
                            "a format the game can read. This will override "
                            "the savefile and create a backup unless a "
                            "backup exists, in which case it will just "
                            "override the current save file.",
                       action="store_true")
    parser.add_argument("-p", "--path",
                        help="A path to specifically decompile or recompile.",
                        default=None)
    args = parser.parse_args()
    if 'path' in args:
        fpath = args.path
    else:
        fpath = None
    if args.load:
        load(fpath)
    elif args.save:
        save(fpath)
