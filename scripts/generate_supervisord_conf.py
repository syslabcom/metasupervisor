# Find all the folders in the parent directory that contain a bin/supervisord file
# and generate a supervisord.conf file that includes all of them.
import pathlib
import os
import sys

SUPERVISORD_PORT = sys.argv[1]
SUPERVISORD_PASSWORD = sys.argv[2]

SUPERVISORD_CONF_PREAMBLE = f"""\
[supervisord]
logfile=var/log/supervisord.log
pidfile=var/run/supervisord.pid
logfile_maxbytes=50MB
logfile_backups=10
loglevel=info
pidfile=var/run/supervisord.pid
childlogdir=var/log
directory=.

[inet_http_server]
port={SUPERVISORD_PORT}
username=admin
password={SUPERVISORD_PASSWORD}

[supervisorctl]
serverurl=http://localhost:{SUPERVISORD_PORT}
username=admin
password={SUPERVISORD_PASSWORD}

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface
"""

parent = pathlib.Path("..")
executables = [
    executable.resolve()
    for executable in parent.glob(os.path.sep.join(["*", "bin", "supervisord"]))
]

# Ensure that the supervisord.conf file is written with 600 permissions.
os.umask(0o177)

with open("etc/supervisord.conf", "w") as conf:
    conf.write(SUPERVISORD_CONF_PREAMBLE)
    for executable in executables:
        program = executable.parent.parent.name
        conf.write(f"\n[program:{program}]\n")
        conf.write(f"command={executable} --nodaemon\n")
        conf.write("autostart=false\n")
        conf.write("autorestart=false\n")
        conf.write("startretries=0\n")
        conf.write("redirect_stderr=true\n")
