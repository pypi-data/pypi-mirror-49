# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm.utils.cmd import call, call_check
from _sadm.utils.sh import mktmp

__all__ = ['deploy']

def deploy(env):
	_autoconf(env)
	call_check('service munin-node stop')
	call_check('service munin-node start')
	call_check('service munin-node status')

def _autoconf(env):
	env.log('autoconf')
	tmpfh = mktmp(prefix = __name__)
	tmpfh.write('exit 128')
	tmpfh.close()
	tmpfn = tmpfh.name()
	env.debug("tmpfn %s" % tmpfn)
	try:
		call("munin-node-configure --shell >%s 2>&1" % tmpfn)
		call_check("/bin/sh -eu %s" % tmpfn)
	finally:
		tmpfh.unlink()
