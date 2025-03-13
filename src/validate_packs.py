import os

from code_checking.pack_loader import PackLoader
from logger import Logger

pack_loader: PackLoader

def check(from_: int, to: int, all_tests: list[str]) -> None:
    global pack_loader

    for i in range(from_, to):
        print(f"Test: {all_tests[i]}")
        print(str(pack_loader.load_bytes(i))[:50])
        print(pack_loader.load_config(i))

def main() -> int:
    global pack_loader
    pack_loader = PackLoader(Logger(), "../tests", ".test", "in", "out", "CONFIG")

    try:
        print("Przykładowo, chcąc sprawdzić testy do zadania pierwszego")
        print("Początkowy plik: 1-01-1.test")
        print("Końcowy plik: 1-01-5.test\n")

        all_tests = sorted(os.listdir("../tests"))

        test_all = input("Czy chcesz sprawdzić wszystkie testy? [t/n] ")
        if not test_all in 'tn':
            print("Toż Ci mówie ~~idioto~~, że 't' lub 'n' co mie tu jakieś głupoty wypisujesz")
            print("Czytać nie umiesz czy z premedytacją testujesz mój kod, hę?")
            return -2
        
        if test_all == 't':
            check(0, len(all_tests), all_tests)
            return 0

        file_min_name = input("Podaj nazwę pliku, od którego należy zacząć sprawdzanie poprawności: ")
        file_max_name = input("Podaj nazwę pliku, na którym nalezy skończyć sprawdzanie poprawności: ")

        check(all_tests.index(file_min_name), all_tests.index(file_max_name)+1, all_tests)
    except ValueError:
        print("Podany/podane plik(i) nie istnieją")
        return -1

    return 0

if __name__ == "__main__":
    exit(main())