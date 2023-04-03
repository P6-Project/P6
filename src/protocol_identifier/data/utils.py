import os

def list_files(dirPath: str, ext: list[str]):
    for path in os.listdir(dirPath):
        absPath = os.path.join(dirPath, path)
        if os.path.isfile(absPath) and os.path.splitext(path)[1] in ext:
            yield absPath
        elif os.path.isdir(absPath):
            yield from list_files(absPath, ext)
        else:
            continue