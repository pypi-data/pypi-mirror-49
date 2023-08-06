import subprocess
import psutil
from cnvrg.helpers.logger_helper import log_message
import shlex
import sys
import re
import sys
import os
ON_POSIX = 'posix' in sys.builtin_module_names


def __send_cmd(cmd, cwd=None):
    os.environ['PYTHONUNBUFFERED'] = "1"
    cmd = re.sub(r"^(python3?)",r"{exe} -u".format(exe=sys.executable), cmd)
    if not isinstance(cmd, list):
        cmd = shlex.split(cmd)
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, close_fds=False, bufsize=1, cwd=r"{}".format(cwd))

def run_sync(cmd, print_output=False, cwd=None):
    proc = __send_cmd(cmd, cwd=cwd)
    output = []
    for log in proc.stdout:
        log = log.decode("utf-8")
        output.append(log)
        if print_output:
            log_message(log)
    return output

def run_async(cmd):
    return __send_cmd(cmd)

def analyze_pid(proc):
    p = psutil.Process(proc.pid)
    with p.oneshot():
        return {"cpu": p.cpu_times(), "cpu_precent": p.cpu_percent(), "memory_info": p.memory_percent(), "threads": p.num_threads()}