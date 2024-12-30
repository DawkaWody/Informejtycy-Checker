from os.path import join

def write_file(path: str, filename: str, content: str) -> None:
    with open(join(path, filename), 'w') as f:
        f.write(content)
