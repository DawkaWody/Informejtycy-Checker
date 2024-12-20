import os
import zipfile


class PackLoader:
    """
    A class that loads test packs from a compressed archive.
    """
    def __init__(self, pack_dir: str, pack_extension: str, in_name: str, out_name: str):
        """
        :param pack_dir: Directory in which to search for packs.
        :param pack_extension: File extension for a pack file
        :param in_name: Name of the file with input data that sits in the pack file.
        :param out_name: Name of the file with output data that sits in the pack file.
        """
        self.pack_dir = pack_dir
        self.pack_extension = pack_extension
        self.in_name = in_name
        self.out_name = out_name

        self.pack_dir_path = os.path.abspath(self.pack_dir)
        self.pack_files = []
        self.get_all()

    def get_all(self) -> None:
        """
        Adds all pack files in the pack directory to the list.
        :return:
        """
        for element in os.listdir(self.pack_dir_path):
            if (os.path.isfile(os.path.join(self.pack_dir, element)) and
                    os.path.splitext(element)[-1] == self.pack_extension):
                self.pack_files.append(element)
        sorted(self.pack_files)

    def load_bytes(self, index: int) -> tuple[bytes, bytes]:
        """
        Loads the pack file from the list at specified index.
        :param index: index of the pack file in the list (starting from 0)
        :return: tuple with the inputs at index 0 and with the outputs at index 1
        """
        with zipfile.ZipFile(os.path.join(self.pack_dir_path, self.pack_files[index])) as pack:
            in_tests = pack.read(self.in_name)
            out_tests = pack.read(self.out_name)

        return in_tests, out_tests
