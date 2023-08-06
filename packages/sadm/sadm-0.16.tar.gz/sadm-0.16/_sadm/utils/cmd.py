# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import subprocess

from os import environ

from _sadm.errors import PluginCommandError

__all__ = ['call', 'callCheck']

class _ProcMan(object):
	def __init__(self):
		self.call = subprocess.call
		self.check_call = subprocess.check_call

proc = _ProcMan()

def call(cmd):
	shell = False
	if isinstance(cmd, str):
		shell = True
	return proc.call(cmd, shell = shell)

def callCheck(cmd, env = None):
	if env is None:
		env = environ.copy()
	shell = False
	if isinstance(cmd, str):
		shell = True
	try:
		return proc.check_call(cmd, env = env, shell = shell)
	except subprocess.CalledProcessError as err:
		raise PluginCommandError(str(err))

call_check = callCheck # FIXME!!!
