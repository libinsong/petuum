#!/usr/bin/env python
# coding=utf-8

'''
Set up petuum project, including preliminaries and compilation

Usage:
    setup_script.py --lib
    setup_script.py --archive
    setup_script.py --petuum
    setup_script.py --make
    setup_script.py --setup

Options:
    -h --help   Print Help Information
    --lib       Copy Third Party Lib
    --archive   Copy Archives
    --petuum    Copy Petuum Project
    --make      Compile Petuum Project
    --setup     Setup

'''


import pexpect
import threading
from docopt import docopt
from script_config import FILE_COPY, SSH_INFO, PETUUM_PROJECT, SETUP_CMD


def copy_dir(ip, src, dest):
    cmd = 'scp -r {src} {ip}:{dest}'.format(src=src, ip=ip,
                                            dest=dest)
    cpy = pexpect.spawn(cmd)
    try:
        i = cpy.expect([pexpect.TIMEOUT, pexpect.EOF])
        if i == 0:
            print '\tCopy Dir Error, TIMEOUT'
    finally:
        cpy.close()


def copy_file(ip, src, dest):
    cmd = 'scp {src} {ip}:{dest}'.format(src=src, ip=ip,
                                         dest=dest)
    cpy = pexpect.spawn(cmd)
    try:
        i = cpy.expect([pexpect.TIMEOUT, pexpect.EOF])
        if i == 0:
            print '\tCopy File Error, TIMEOUT'
    finally:
        cpy.close()


def make_project(ip):
    ip_str = ip.replace('.', '-')
    make = pexpect.spawn('ssh {ip}'.format(ip))
    try:
        i = make.expect([ip_str, pexpect.TIMEOUT, pexpect.EOF],
                        timeout=1)
        if i == 0:
            make.sendline('cd petuum\n')
            make.sendline('make\n')
            j = make.expect([ip_str, pexpect.TIMEOUT, pexpect.EOF],
                            timeout=3600)
            if j == 0:
                print '\nMake Success'
            elif j == 1:
                print '\nMake Failed, TIMEOUT'
            elif j == 2:
                print '\nMake Failed, EOF'
        elif i == 1:
            print '\nSSH ERROR, TIMEOUT'
        elif i == 2:
            print '\nSSH ERROR, EOF'
    finally:
        make.close()


def install(ip):
    cmd_gcc = 'sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 50\n'
    cmd_gpp = 'sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 50\n'
    ip_str = ip.replace('.', '-')
    inst = pexpect.spawn('ssh {ip}'.format(ip=ip))
    try:
        i = inst.expect([ip_str, pexpect.TIMEOUT, pexpect.EOF], timeout=100)
        if i == 0:
            inst.sendline('cd /etc/apt/\n')
            inst.sendline('mv sources.list sources.list.backup\n')
            inst.sendline('mv sources.list.tmp sources.list\n')
            print '\tBackup sources.list'
            inst.sendline('sudo apt-get update\n')
            for cmd in SETUP_CMD:
                print '\tExecuting ' + cmd
                inst.sendline(cmd + '\n')
                j = inst.expect(['now taking place', 'Y/n', 'y/N', 'already the newest', pexpect.TIMEOUT, pexpect.EOF], timeout=100)
                while j == 1 or j == 2:
                    inst.sendline('y\n')
                    j = inst.expect(['now taking place', 'Y/n', 'y/N', 'already the newest', pexpect.TIMEOUT, pexpect.EOF], timeout=100)
                if j == 0:
                    print '\tInstall Success'
                elif j == 1 or j == 2:
                    print '\tERROR!!!'
                elif j == 3:
                    print '\tAlready Newest Version'
                elif j == 4:
                    print '\tInstall TIMEOUT'
                elif j == 5:
                    print '\tInstall EOF'
            inst.sendline(cmd_gcc)
            inst.sendline(cmd_gpp)
            inst.sendline('rm sources.list\n')
            inst.sendline('mv sources.list.backup sources.list\n')
            print '\tRestore sources.list'
        elif i == 1:
            print '\tSSH TIMEOUT'
        elif i == 2:
            print '\tSSH EOF'
    finally:
        inst.close()


def copy_third_party_lib():
    src_path = FILE_COPY['third_party_lib']['from']
    dest_path = FILE_COPY['third_party_lib']['to']
    print 'Copy third party lib'
    for info in SSH_INFO:
        print '\tcopy lib for {ip}'.format(ip=info['ip'])
        copy_dir(info['ip'], src_path, dest_path)


def copy_archives():
    src_path = FILE_COPY['archives']['from']
    dest_path = FILE_COPY['archives']['to']
    print 'Copy archives'
    for info in SSH_INFO:
        print '\tcopy archives for {ip}'.format(ip=info['ip'])
        copy_dir(info['ip'], src_path, dest_path)


def copy_petuum_project():
    src_path = PETUUM_PROJECT['from']
    dest_path = PETUUM_PROJECT['to']
    print 'Copy petuum project'
    for info in SSH_INFO:
        print '\tcopy petuum for {ip}'.format(ip=info['ip'])
        copy_dir(info['ip'], src_path, dest_path)


def compile_petuum():
    print 'Compile petuum project'
    for info in SSH_INFO:
        print '\tStarting to compile at {ip}'.format(ip=info['ip'])
        a = threading.Thread(target=make_project,
                             args=(info['ip']))
        a.start()


def setup_dependencies():
    print 'Setup dependencies'
    for info in SSH_INFO:
        print 'Setup for {ip}'.format(ip=info['ip'])
        copy_file(
            info['ip'], FILE_COPY['source']['from'], FILE_COPY['source']['to'])
        install(info['ip'])


def main(args):
    if args['--lib']:
        copy_third_party_lib()
    elif args['--archive']:
        copy_archives()
    elif args['--petuum']:
        copy_petuum_project()
    elif args['--make']:
        compile_petuum()
    elif args['--setup']:
        setup_dependencies()


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0.0')
    main(args)
