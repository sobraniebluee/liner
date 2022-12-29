import os
import json
import sys


class Error:
    dir = ": No such file or directory"
    parse = "Error parse params!"


class Config:
    TOTAL_FILES = 0
    TOTAL_LINES = 0
    TOTAL_SIZE = 0
    EXTENSIONS = []
    EXCLUDE: str = []
    IS_RECURSIVE = False
    IS_NORMALIZE_SIZE = False


def is_exclude(entity_path):
    abs_entity_path = os.path.abspath(entity_path)
    for exclude in Config.EXCLUDE:
        if exclude.strip("/") in abs_entity_path.split("/"):
            return True
        if os.path.abspath(exclude) == abs_entity_path:
            return True

    return False


def match_filename(filepath, extensions: list[str] = None) -> bool:
    if not extensions:
        return True

    file_extension = filepath.split('.')[-1]
    for ext in extensions:
        ext = ext.strip('.')
        if ext == file_extension:
            return True

    return False


def normalize_size_format(size: int):
    if not Config.IS_NORMALIZE_SIZE:
        return size
    sizes = ['B', 'K', 'M', 'G']

    for i in range(0, len(sizes) - 1):
        prev = size

        size = size / 1024
        if size < 0.9:
            return str(round(prev, 1)).replace('.0', '') + sizes[i]

    return str(round(size, 1)).replace('.0', '') + sizes[-1]


def count_lines(filepath) -> None:
    if not match_filename(filepath, extensions=Config.EXTENSIONS):
        return

    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            lines = data.split(b'\n')
            print("size:", normalize_size_format(len(data)), "lines:", len(lines), filepath)
            Config.TOTAL_LINES += len(lines)
            Config.TOTAL_SIZE += len(data)
            Config.TOTAL_FILES += 1
    except Exception as e:
        print("Error", e)


def line_reader(dir_entity):
    if not os.path.isdir(dir_entity) and not os.path.isfile(dir_entity):
        print("liner:", dir_entity, Error.dir)
    try:
        if os.path.isdir(dir_entity):

            for directory in os.scandir(dir_entity):
                entity_path = os.path.join(dir_entity, directory.name)
                if is_exclude(entity_path):
                    continue
                if Config.IS_RECURSIVE and directory.is_dir():
                    line_reader(entity_path)
                elif not directory.is_dir():
                    count_lines(entity_path)
        else:
            count_lines(dir_entity)
    except Exception as e:
        print(e)


def main(params: str):
    try:
        parse_params = json.loads(params)
    except Exception as e:
        exit(Error.parse)
    else:
        entry = parse_params.get('entry')
        extensions = parse_params.get('extensions', "")
        Config.IS_RECURSIVE = parse_params.get('is_recursive')
        Config.IS_NORMALIZE_SIZE = parse_params.get('is_normalize_size')
        exclude = parse_params.get("exclude", "")

        if len(exclude) > 0:
            Config.EXCLUDE = exclude.split(" ")
        if len(extensions) > 0:
            Config.EXTENSIONS = extensions.split(" ")

        try:
            line_reader(dir_entity=entry)
        except KeyboardInterrupt:
            print("\nStop...")
        finally:
            print("\ntotal lines:", Config.TOTAL_LINES,
                  "\ntotal size:", normalize_size_format(Config.TOTAL_SIZE),
                  "\ntotal files:", Config.TOTAL_FILES)


if __name__ == "__main__":
    try:
        args, *rest = sys.argv[1:]
    except ValueError:
        exit(Error.parse)
    else:
        # Start parse params and run line_reader
        main(params=args)
