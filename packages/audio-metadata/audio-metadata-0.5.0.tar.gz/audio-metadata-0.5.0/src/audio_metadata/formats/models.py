__all__ = [
	'Format',
	'Picture',
	'StreamInfo',
	'Tags'
]

import os

from bidict import frozenbidict

from ..structures import DictMixin
from ..utils import (
	DataReader,
	humanize_bitrate,
	humanize_duration,
	humanize_filesize,
	humanize_sample_rate
)


class Tags(DictMixin):
	FIELD_MAP = frozenbidict()

	def __getitem__(self, key):
		k = self.FIELD_MAP.get(key, key)

		return super().__getitem__(k)

	def __setitem__(self, key, value):
		k = self.FIELD_MAP.get(key, key)

		return super().__setitem__(k, value)

	def __delitem__(self, key):
		k = self.FIELD_MAP.get(key, key)

		return super().__delitem__(k)

	def __iter__(self):
		return iter(
			self.FIELD_MAP.inv.get(k, k)
			for k in self.__dict__
			if not k.startswith('_') and not k == 'FIELD_MAP'
		)

	def __repr__(self, repr_dict=None):
		repr_dict = {
			self.FIELD_MAP.inv.get(k, k): v
			for k, v in self.__dict__.items()
			if not k.startswith('_') and not k == 'FIELD_MAP'
		}

		return super().__repr__(repr_dict=repr_dict)


class Format(DictMixin):
	"""Base class for audio format objects.

	Attributes:
		filepath (str): Path to audio file, if applicable.
		filesize (int): Size of audio file.
		pictures (list): A list of :class:`Picture` objects.
		tags (Tags): A :class:`Tags` object.
	"""

	tags_type = Tags

	def __init__(self):
		self.filepath = None
		self.filesize = None
		self.pictures = []
		self.tags = self.tags_type()

	def __repr__(self):
		repr_dict = {}

		for k, v in sorted(self.items()):
			if k == 'filesize':
				repr_dict[k] = humanize_filesize(v, precision=2)
			elif not k.startswith('_'):
				repr_dict[k] = v

		return super().__repr__(repr_dict=repr_dict)

	@classmethod
	def _load(cls, data):
		self = cls()

		if hasattr(data, 'name'):
			self.filepath = os.path.abspath(data.name)
			self.filesize = os.path.getsize(data.name)
		elif isinstance(data, DataReader):
			if hasattr(data.data, 'name'):
				self.filepath = os.path.abspath(data.data.name)
				self.filesize = os.path.getsize(data.data.name)
			else:
				self.filepath = None
				self.filesize = len(data.data.getbuffer())
		else:
			self.filepath = None
			self.filesize = len(data)

		if not isinstance(data, DataReader):
			self._obj = DataReader(data)
		else:
			self._obj = data

		return self


class Picture(DictMixin):
	def __repr__(self):
		repr_dict = {}

		for k, v in sorted(self.items()):
			if k == 'data':
				repr_dict[k] = humanize_filesize(len(v), precision=2)
			elif not k.startswith('_'):
				repr_dict[k] = v

		return super().__repr__(repr_dict=repr_dict)


class StreamInfo(DictMixin):
	def __repr__(self):
		repr_dict = {}

		for k, v in sorted(self.items()):
			if k == 'bitrate':
				repr_dict[k] = humanize_bitrate(v)
			elif k == 'duration':
				repr_dict[k] = humanize_duration(v)
			elif k == 'sample_rate':
				repr_dict[k] = humanize_sample_rate(v)
			elif not k.startswith('_'):
				repr_dict[k] = v

		return super().__repr__(repr_dict=repr_dict)
