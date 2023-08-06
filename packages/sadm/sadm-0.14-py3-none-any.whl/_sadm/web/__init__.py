# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm import log
from _sadm.web.app import wapp

# load views
import _sadm.web.errors
import _sadm.web.view.home
import _sadm.web.view.profile
import _sadm.web.view.syslog
import _sadm.web.view.about

def start(host, port, debug):
	wapp.run(host = host, port = port, reloader = debug,
		quiet = log._curlevel != 'debug', debug = debug)
