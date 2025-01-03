import os
import zipfile


class PackLoader:
	"""
	A class that loads test packs from a compressed archive.
	"""
	def __init__(self, pack_dir: str, pack_extension: str, in_name: str, out_name: str):
		"""
		:param pack_dir: Directory in which to search for packs.
		:param pack_extension: File extension for a pack file.
		:param in_name: Name of the file with input data that sits in the pack file.
		:param out_name: Name of the file with output data that sits in the pack file.
		"""
		self.pack_dir = pack_dir
		self.pack_extension = pack_extension
		self.in_name = in_name
		self.out_name = out_name

		self.pack_dir_path = os.path.abspath(self.pack_dir)
		self.pack_files = self.get_all()

	def get_all(self) -> list:
		"""
		Returns a list of all pack files in the pack directory.
		:return:
		"""
		pack_files = []
		for element in os.listdir(self.pack_dir_path):
			if (os.path.isfile(os.path.join(self.pack_dir, element)) and
					os.path.splitext(element)[-1] == self.pack_extension):
				pack_files.append(element)
		sorted(pack_files)
		return pack_files
	
	def get_pack_count(self) -> int:
		"""
		Returns the number of pack files in the pack directory.
		:return: Number of pack files in the pack directory.
		"""
		return len(self.pack_files)

	def load_bytes(self, index: int) -> tuple[bool, list[tuple[bytes, bytes]]]:
		"""
		Loads the pack file from the list at specified index.
		:param index: index of the pack file in the list (starting from 0)
		:return: List of tuples with the inputs at index 0 and with the outputs at index 1
		"""
		
		tests = []
		with zipfile.ZipFile(os.path.join(self.pack_dir_path, self.pack_files[index])) as pack:
			for i in range(int(len(pack.filelist) / 2)):
				in_test = pack.read(self.in_name + str(i + 1))
				out_test = pack.read(self.out_name + str(i + 1))
				tests.append((in_test, out_test))

		return tests
