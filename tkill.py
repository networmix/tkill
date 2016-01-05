#!/usr/bin/env python
# This sript tracks VPN interface and allows to use uTorrent only if VPN interface is present. 

import time
import subprocess
import signal
import os
import sys


__version__ = "1.0.1"
__status__ = "First release"


IFNAME = 'ppp' # The name of the interface to track
APPNAME = 'uTorrent.app' # The name of the app to kill

# SIGTERM (15) - Termination signal. This is the default and safest way to kill process.
# SIGKILL (9) - Kill signal. This will not save data and no cleanup while killing the process.
SIG = signal.SIGTERM 


def main():
    get_pid_cmd = "ps -ax"
    get_ifaces_cmd = "ifconfig -lu"
    
    while True:
        proc_lst = subprocess.check_output(get_pid_cmd, shell=True).split('\n')
        ifaces = subprocess.check_output(get_ifaces_cmd, shell=True)
        
        pids = []
        # Getting all pids belonging to 'APPNAME'
        for string in proc_lst:
            if APPNAME in string:
                pids.append(string.split()[0]) 

        VPN_ACTIVE = True if IFNAME in ifaces else False
        UT_ACTIVE = True if pids else False

        if UT_ACTIVE and VPN_ACTIVE:
            time.sleep(1)

        # We don't allow to run 'APPNAME' if VPN ('IFNAME') is not there
        elif UT_ACTIVE:
            for pid in pids:
                try:
                    os.kill(int(pid), SIG)
                except:
                    formatstr = {'pid' : pid}
                    err_msg = "Warning! Couldn't kill {pid}.\n".format(**formatstr)
                    sys.stderr.write(err_msg)

            time.sleep(1)


def int_handler(signal, frame):
    sys.stdout.write('\nSIGINT captured. Exiting.\n')
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, int_handler)
    main()
