
from pyglossary.core import rootDir
from os.path import join
import json
from typing import (
	List,
	Optional,
)

import logging
log = logging.getLogger("root")


class Lang(object):
	def __init__(self, codes: List[str], names: List[str]):
		self._codes = codes
		self._names = names

	def __repr__(self) -> str:
		return f"Lang(codes={self._codes!r}, names={self._names!r})"

	def __str__(self) -> str:
		return f"Lang({self._codes + self._names})"

	@property
	def codes(self):
		return self._codes

	@property
	def names(self):
		return self._names

	@property
	def name(self):
		return self._names[0]

	@property
	def code(self):
		return self._codes[0]


class LangDict(dict):
	def load(self):
		if len(self) > 0:
			return
		filename = join(rootDir, "pyglossary", "langs", "langs.json")
		with open(filename, "r", encoding="utf-8") as _file:
			data = json.load(_file)
			for row in data:
				lang = Lang(
					codes=row["codes"],
					names=[row["name"]] + row["alt_names"],
				)
				for key in lang.codes:
					if key in self:
						log.error(f"duplicate language code: {key}")
					self[key] = lang
				for name in lang.names:
					if name in self:
						log.error(f"duplicate language name: {name}")
					self[name.lower()] = lang
		print(f"LangDict: loaded, {len(self)} keys")

	def __getitem__(self, key: str) -> Optional[Lang]:
		self.load()
		return self.get(key.lower(), None)
