import os
import subprocess
from itertools import chain, imap


def _escape_parameter(parameter):
    parameter = str(parameter)
    if parameter.startswith('-'):
        return parameter
    return '"%s"' % parameter.replace('\\', '\\\\').replace('"', '\\"')


def run(command, *arguments, **kwargs):
    command = ' '.join(chain([command], imap(_escape_parameter, arguments)))

    print "RUNNING:", command
    pipe = subprocess.PIPE if kwargs.get('return_stdout') else None
    proc = subprocess.Popen(command, shell=True, stdout=pipe)
    stdout = proc.communicate()[0]
    if proc.returncode != 0:
        raise Exception("suprocess interrupted with error: %d" % proc.returncode)
    return stdout


def remove_file(filename):
    print "Removing file", filename
    os.remove(filename)
