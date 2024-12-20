import subprocess

def check(filename: str, index: int):
    pass

if __name__ == "__main__":
    from pack_loader import PackLoader
    pl = PackLoader('../tests', '.test', 'in', 'out')
    print(pl.load_bytes(0))
    print(pl.load_bytes(1))
