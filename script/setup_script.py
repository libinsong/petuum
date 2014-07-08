#!/usr/bin/env python
# coding=utf-8

'''
Set up petuum project, including preliminaries and compilation

Usage:
    setup_script.py --lib
    setup_script.py --archive
    setup_script.py --petuum
    setup_script.py --make
    setup_scripy.py --setup

Options:
    -h --help   Print Help Information
    --lib       Copy Third Party Lib
    --archive   Copy Archives
    --petuum    Copy Petuum Project
    --make      Compile Petuum Project
    --setup    Setup

'''


import pexpect
import threading
from docopt import docopt
from script_config import FILE_COPY, SSH_INFO, PETUUM_PROJECT, SETUP_CMD, SOURCE_LIST


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


def copy_ownfile(ip, src, back):
    ip_str = ip.replace('.', '-')
    cpy = pexpect.spawn('ssh {ip}'.format(ip=ip))
    try:
        i = cpy.expect([ip_str, pexpect.TIMEOUT, pexpect.EOF],
                        timeout=100)
        if i == 0:
            cpy.sendline('cp {src} {back}\n'.format(src=src, back=back))
            print '\tcp {src} {back}'.format(src=src, back=back)
        elif i == 1:
            print '\tBackup failed, TIMEOUT'
        elif i == 2:
            print '\tBackup failed, EOF'
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
    ip_str = ip.replace('.', '-')
    make = pexpect.spawn('ssh {ip}'.format(ip=ip))
    try:
        i = make.expect([ip_str, pexpect.TIMEOUT, pexpect.EOF],
                        timeout=100)
        if i == 0:
            make.sendline('sudo apt-get update\n')
            for cmd in SETUP_CMD:
                make.sendline('{cmd}\n'.format(cmd=cmd))
                j = make.expect(['Install these packages without verification',
                                 pexpect.TIMEOUT, pexpect.EOF], timeout=100)
                if j == 0:
                    make.sendline('y\n')
            make.sendline(
                'sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 50\n')
            make.sendline(
                'sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.8 50\n')
    finally:
        make.close()


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
    newsrc_file = SOURCE_LIST['newsrc']
    src_file = SOURCE_LIST['src']
    back_file = SOURCE_LIST['backsrc']
    for info in SSH_INFO:
        print '\tSetup for {ip}'.format(ip=info['ip'])
        copy_file(info['ip'], newsrc_file, newsrc_file)
        copy_ownfile(info['ip'], src_file, back_file)
        install(info['ip'])
        copy_ownfile(info['ip'], back_file, src_file)


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
