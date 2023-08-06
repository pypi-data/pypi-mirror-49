#!/usr/bin/env python3

import sys
import os
import hashlib
from docopt import docopt
import random
import json
import io
import csv

DEFAULT_ROOT = os.path.abspath(".")
OUTPUT_FORMATS = ["just-filename", "plain", "json", "char30-delimited"]
OUTPUT_FORMATS_LIST = ", ".join(["'" + x + "'" for x in OUTPUT_FORMATS])

__doc__ = """
Usage: {0} [options] [-e <ext>]... [<DIR>]

Options:
  -h, --help                        Show this help
  <DIR>                             Directory to start descending from
                                    [DEFAULT: {1}]
  -s, --sha384-blacklist=<filename> File full of sha384s to be skipped
  -p, --path-blacklist=<filename>   File full of paths to be skipped
  -o, --output-format=<style>       {2}
                                    [DEFAULT: just-filename]
  -v, --version                     Show version
  -e, --extension=<.txt>            Only yield files with this extension
                                    (case insensitive)
  -n, --numfiles=<number>           How many random files to yield
                                    [DEFAULT: 1]
""".format(sys.argv[0], DEFAULT_ROOT, OUTPUT_FORMATS_LIST)


def sha384(filename):
  BLOCKSIZE = 65536
  hasher = hashlib.sha384()
  with open(filename, "rb") as f:
    buf = f.read(BLOCKSIZE)
    while len(buf) > 0:
      hasher.update(buf)
      buf = f.read(BLOCKSIZE)
  return hasher.hexdigest()


def random_non_repeating_filenames(root, *, blacklist=None,
    conditions=None):
  if conditions == None:
    conditions = []
  if blacklist != None:
    conditions.append(lambda x: x not in blacklist)

  # TODO Consider how large this gets and do write
  # to disk if it gets too big or do some other intelligent
  # optimizations
  already_yielded = []
  new_filename = random_file(root,
      file_condition = lambda x:
        x not in already_yielded and
        all([condition(x) for condition in conditions])
  )
  while new_filename != None:
    already_yielded.append(new_filename)
    yield new_filename
    new_filename = random_file(root,
        file_condition = lambda x:
          x not in already_yielded and
          all([condition(x) for condition in conditions])
    )


def random_file(root, *, file_condition=None, dir_condition=None):
  """
  To be returned, file_condition must be True and dir_condition must be True
  for all directories containing a file
  """
  if file_condition == None:
    file_condition = lambda x: True
  if dir_condition == None:
    dir_condition = lambda x: True
  if not dir_condition(root):
    return None
  if os.path.isfile(root):
    if file_condition(root):
      return root
    else:
      return None
  if not os.path.isdir(root):
    return None

  # Now it's a directory for sure
  all_items = os.listdir(root)
  all_items = random.sample(all_items, len(all_items))
  for dir_or_file in all_items:
    dir_or_file = os.path.join(root, dir_or_file)
    if os.path.isfile(dir_or_file) and file_condition(dir_or_file):
      return dir_or_file
    if os.path.isdir(dir_or_file) and dir_condition(dir_or_file):
      maybe = random_file(dir_or_file, file_condition=file_condition,
          dir_condition=dir_condition)
      if maybe is not None:
        return maybe
  return None



def main():
  args = docopt(__doc__, version="1.1.0")
  root = args["<DIR>"]
  _format = args["--output-format"]
  if _format not in OUTPUT_FORMATS:
    print("Only allowed formats are:\n  {}\nreceived '{}'".format(
        OUTPUT_FORMATS_LIST, _format))
    exit(1)
  if root == None:
    root = DEFAULT_ROOT
  try:
    num_to_yield = int(args["--numfiles"])
  except ValueError as e:
    print("--numfiles argument must be an integer")
    exit(1)

  conditions = []
  blacklist = []
  if args["--sha384-blacklist"] != None:
    with open(args["--sha384-blacklist"]) as f:
      sha384_blacklist = f.read().split()
      conditions.append(lambda x: sha384(x) not in sha384_blacklist)
  if args["--path-blacklist"] != None:
    with open(args["--path-blacklist"]) as g:
      blacklist = g.read().split()
  if args["--extension"] != []:
    for extension in args["--extension"]:
      conditions.append(lambda x: x.lower().endswith(extension.lower()))

  filename_generator = random_non_repeating_filenames(root,
      blacklist=blacklist, conditions=conditions)

  for file_number in range(num_to_yield):
    try:
      _next = next(filename_generator)
    except StopIteration as e:
      print("Only {} files were available".format(file_number), file=sys.stderr)
      exit(1)

    if _format == "just-filename":
      print(_next)
    else:
      info = {"path": _next, "sha384": sha384(_next)}
      if _format == "json":
        print(json.dumps(info))
      elif _format == "char30-delimited":
        print(chr(30).join(["path", _next, "sha384", sha384(_next)]))
      elif _format == "plain":
        print("path: {}".format(_next))
        print("sha384: {}".format(sha384(_next)))
      else:
        print(_next)


if __name__ == "__main__":
  main()
