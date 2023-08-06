SvcD class and "svcd" command to run persistent service programmes.


Release 20190729:
Get DEVNULL via cs.py3 instead of directly from subprocess.

SvcD class and "svcd" command to run persistent service programmes.

This provides the features one wants from a daemon
for arbitrary commands providing a service:

* process id (pid) files for both svcd and the service command
* filesystem visible status (command running, service enabled)
  via `cs.app.flag <https://pypi.org/project/cs.app.flag/>`_
* command restart if the command exits
* command control (stop, restart, disable)
  via `cs.app.flag <https://pypi.org/project/cs.app.flag/>`_
* test function to monitor for service viability;
  if the test function fails, do not run the service.
  This typically monitors something like
  network routing (suspend service while laptop offline)
  or a ping (suspend ssh tunnel while target does not answer pings).
* signature function to monitor for service restart;
  if the signature changes, restart the service.
  This typically monitors something like
  file contents (restart service on configuration change)
  or network routing (restart ssh tunnel on network change)
* callbacks for service command start and end,
  for example to display desktop notifications

I use this to run persistent ssh port forwards
and a small collection of other personal services.
I have convenient shell commands to look up service status
and to start/stop/restart services.

See `cs.app.portfwd <https://pypi.org/project/cs.app.portfwd/>`_
which I use to manage my ssh tunnels;
it is a single Python programme
running multiple ssh commands, each via its own SvcD instance.

## Function `main(argv=None)`

Command line main programme.

## Class `SvcD`

MRO: `cs.app.flag.FlaggedMixin`  
A process based service.

### Method `SvcD.__init__(self, argv, name=None, environ=None, flags=None, group_name=None, pidfile=None, sig_func=None, test_flags=None, test_func=None, test_rate=None, restart_delay=None, once=False, quiet=False, trace=False, on_spawn=None, on_reap=None)`

Initialise the SvcD.

Parameters:
* `argv`: command to run as a subprocess.
* `flags`: a cs.app.flag.Flags -like object, default None;
  if None the default flags will be used.
* `group_name`: alert group name, default "SVCD " + `name`.
* `pidfile`: path to pid file, default $VARRUN/{name}.pid.
* `sig_func`: signature function to compute a string which
  causes a restart if it changes
* `test_flags`: map of {flagname: truthiness} which should
  be monitored at test time; truthy flags must be true and
  untruthy flags must be false
* `test_func`: test function with must return true if the comannd can run
* `test_rate`: frequency of tests, default TEST_RATE
* `restart_delay`: delay before start of an exiting command,
  default RESTART_DELAY
* `once`: if true, run the command only once
* `quiet`: if true, do not issue alerts
* `trace`: trace actions, default False
* `on_spawn`: to be called after a new subprocess is spawned
* `on_reap`: to be called after a subprocess is reaped



#Release Log#

Release 20190729:
Get DEVNULL via cs.py3 instead of directly from subprocess.

Release 20190602.2:
Another doc tweak.

Release 20190602.1:
Improve module documentation formatting.

Release 20190602:
Support alert groups.
Catch and report exceptions from the monitor signature function.
Python 2 port fix for DEVNULL.

Release 20171118:
Bugfix for su invocation in setuid mode. Improved signature command tracing with -x option.

Release 20171026:
Improved logic around signature changes.

Release 20171025:
New "-F flag,..." option for svcd. Improve stop logic. Other small fixes.

Release 20170906:
Initial PyPI release.
