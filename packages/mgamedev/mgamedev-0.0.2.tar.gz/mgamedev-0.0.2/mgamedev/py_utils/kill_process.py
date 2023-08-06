import os
import sys
import subprocess
import logging
import re


def __suc(procename):
    logging.warning("[kill_process] kill process <%s>  suc!", procename)


def __not():
    logging.warning("[kill_process] nothing to kill")


def kill_process(procename):
    cmd_killall = "killall %s" % procename
    ret = subprocess.Popen(cmd_killall, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sout, serr = ret.communicate()
    if ret.returncode == 0:
        __suc()
    else:
        cmd_findone = "ps -ef | grep %s" % procename
        ret = subprocess.Popen(cmd_findone, shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sout, serr = ret.communicate()
        proce_list = re.split(r"\n+", sout)
        if len(proce_list) > 4:
            for proce in proce_list:
                infos = re.split(r"\s+", proce)
                if procename in infos:
                    ret = os.system("kill -9 %s" % str(infos[2]))
                    if (ret == 0):
                        __suc("PID:%s  " % str(infos[2]))
        else:
            __not()


if __name__ == "__main__":
    proc_name = sys.argv[1]
    kill_process(proc_name)
