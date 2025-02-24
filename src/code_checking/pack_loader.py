import os
import zipfile

from logger import Logger


class PackLoader:
	"""
	A class that loads test packs from a compressed archive.
	"""
	def __init__(self, logger: Logger, pack_dir: str, pack_extension: str, in_name: str, out_name: str, config_name: str):
		"""
		:param logger: Used for logging about invalid packs.
		:param pack_dir: Directory in which to search for packs.
		:param pack_extension: File extension for a pack file.
		:param in_name: Name of the file with input data that sits in the pack file.
		:param out_name: Name of the file with output data that sits in the pack file.
		"""
		self.logger = logger
		
		self.pack_dir = pack_dir
		self.pack_extension = pack_extension
		self.in_name = in_name
		self.out_name = out_name
		self.config_name = config_name

		self.pack_dir_path = os.path.abspath(self.pack_dir)
		self.pack_files = self.get_all()

	def get_all(self) -> list:
		"""
		Returns a list of all pack files in the pack directory.
		:return:
		"""
		pack_files = []
		for element in os.listdir(self.pack_dir_path):
			if (os.path.isfile(os.path.join(self.pack_dir, element)) and os.path.splitext(element)[-1] == self.pack_extension):
				pack_files.append(element)
		pack_files.sort()
		return pack_files
	
	def get_pack_count(self) -> int:
		"""
		Returns the number of pack files in the pack directory.
		:return: Number of pack files in the pack directory.
		"""
		return len(self.pack_files)

	def load_bytes(self, index: int) -> list[tuple[bytes, bytes]]:
		"""
		Loads the pack file from the list at specified index.
		:param index: index of the pack file in the list (starting from 0)
		:return: List of tuples with the inputs at index 0 and with the outputs at index 1
		"""
		
		tests = []
		if index >= self.get_pack_count():
			self.logger.alert(f"Given pack index {index} doesn't exists", self.load_bytes)
			return [(b"", b"")]

		with zipfile.ZipFile(os.path.join(self.pack_dir_path, self.pack_files[index])) as pack:
			for i in range(len(pack.filelist) // 2):
				try:
					in_test = pack.read(self.in_name + str(i + 1))
					out_test = pack.read(self.out_name + str(i + 1))
					tests.append((in_test, out_test))
				except KeyError:
					self.logger.alert("Number of input files must match the number of output files.", self.load_bytes)
					tests.append((b"", b""))
				except Exception as e:
					self.logger.error(f"Challenge Complete! How Did We Get Here? | {e.__class__.__name}: {e}", self.load_bytes)
					tests.append((b"", b""))

		return tests

	def load_config(self, index: int) -> dict[str, int]:
		"""
		Loads the pack file settings from the list at specified index.
		:param index: index of the pack file in the list (starting from 0)
		:return: Dictionary with time limit and memory limit
		"""
		conf = {"time_limit": 3, "memory_limit": 60}

		with zipfile.ZipFile(os.path.join(self.pack_dir_path, self.pack_files[index])) as pack:
			try:
				settings = pack.read(self.config_name).split()
				
				conf["time_limit"] = int(settings[0])
				conf["memory_limit"] = int(settings[1])
			except KeyError:
				self.logger.alert("Config file is not present.", self.load_config)
			except ValueError:
				self.logger.alert("Time or memory limit is not an integer.", self.load_config)
			except Exception as e:
				self.logger.error(f"Challenge Complete! How Did We Get Here? | {e.__class__.__name}: {e}", self.load_config)

		return conf