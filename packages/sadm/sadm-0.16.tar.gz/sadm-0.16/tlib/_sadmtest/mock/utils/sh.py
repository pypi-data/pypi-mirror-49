# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from os import path
from unittest.mock import Mock

class MockTmpFile(object):
	_fn = None

	def __init__(self, suffix = None, prefix = None, dir = None):
		if suffix is None:
			suffix = '.mock'
		if prefix is None:
			prefix = __name__
		if dir is None:
			dir = path.join(path.sep, 'tmp')
		self._fn = path.join(dir, prefix + suffix)

	def __enter__(self):
		return self

	def __exit__(self, *args):
		pass

	def close(self):
		pass

	def unlink(self):
		pass

	def write(self, data):
		pass

	def name(self):
		return self._fn

class MockShUtil(object):
	_mock = None
	_cfg = None
	makedirs = None
	chmod = None
	chown = None
	mktmp = None

	def __init__(self, cfg):
		self._mock = Mock()
		self.makedirs = self._mock.mock_makedirs
		self.chmod = self._mock.mock_chmod
		self.chown = self._mock.mock_chown
		self.mktmp = self._mock.mock_mktmp
		self._configure(cfg)

	def _configure(self, cfg):
		self.mktmp.side_effect = self._mktmp

	def _mktmp(self, suffix = None, prefix = None, dir = None):
		return MockTmpFile(suffix = suffix, prefix = prefix, dir = dir)

	def check(self):
		# ~ assert self._mock.mock_calls == [], str(self._mock.mock_calls)
		pass
