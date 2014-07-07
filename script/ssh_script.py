#!/usr/bin/env python
# coding=utf-8

'''
ssh_script: test, close and free ssh

Usage:
    ssh_script.py --test
    ssh_script.py --close
    ssh_script.py --free

Options:
    -h --help   Print Help Information
    --test      Test Ssh
    --close     Close Ssh
    --free      Free Ssh
'''




import pexpect
from docopt import docopt
from script_config import SSH_INFO

def key_gen():
    print 'Generating SSH Key...'
    gen = pexpect.spawn('ssh-keygen -t rsa')
    gen.sendline()
    try:
        i = gen.expect(['Overwrite', pexpect.TIMEOUT, pexpect.EOF],
                       timeout=1)
        if i == 0:
            gen.sendline('y\n')         #overwrite old ssh key
            gen.sendline('\n')
            gen.sendline('\n')
            print 'SSH Key Success'
        elif i == 1:
            print 'KeyGen TIMEOUT'
        elif i == 2:
            print 'KeyGen EOF'
    finally:
        gen.close()


def key_copy(ip, password):
    cpy = pexpect.spawn('ssh-copy-id -i {ip}'.format(ip=ip))
    try:
        i = cpy.expect(['password', 'yes/no', pexpect.TIMEOUT,
                        pexpect.EOF], timeout=1)
        if i == 0:
            cpy.sendline(password + '\n')
            print '\t{ip} Success'.format(ip = ip)
        elif i == 1:
            cpy.sendline('yes\n')
            cpy.sendline(password + '\n')
            print '\t{ip} Success'.format(ip=ip)
        elif i == 2:
            print '\t{ip} TIMEOUT'.format(ip=ip)
        elif i == 3:
            print '\t{ip} EOF'.format(ip=ip)
    finally:
        cpy.close()


def test_ip(ip):
    test = pexpect.spawn('ssh {ip}'.format(ip=ip))
    try:
        i = test.expect(['password', 'yes/no', pexpect.TIMEOUT,
                         pexpect.EOF], timeout=1)
        if i == 0:
            print '{ip} Failed'.format(ip=ip)
        elif i == 1:
            test.sendline('yes\n')
            j = test.expect(['password', pexpect.TIMEOUT,
                            pexpect.EOF], timeout=1)
            if j == 0:
                print '{ip} Failed'.format(ip=ip)
            elif j == 1:
                print '{ip} Success'.format(ip=ip)
            elif j == 2:
                print '{ip} Failed, EOF'.format(ip=ip)
        elif i == 2:
            print '{ip} Success'.format(ip=ip)
        elif i == 3:
            print '{ip} Failed, EOF'.format(ip=ip)
    finally:
        test.close()


def close_ip(ip):
    cls = pexpect.spawn('ssh {ip}'.format(ip=ip))
    try:
        i = cls.expect(['password', 'yes/no', pexpect.TIMEOUT,
                        pexpect.EOF], timeout=1)
        if i == 0:
            print '{ip} Already Closed'.format(ip=ip)
        elif i == 1:
            cls.sendline('yes\n')
            j = cls.expect(['password', pexpect.TIMEOUT,
                            pexpect.EOF], timeout=1)
            if j == 0:
                print '{ip} ALready Closed'
            elif j == 1:
                cls.sendline('rm -r ~/.ssh\n')
                print '{ip} Closed'.format(ip=ip)
            elif j == 2:
                print '{ip} Failed, EOF'.format(ip=ip)
        elif i == 2:
            cls.sendline('rm -r ~/.ssh\n'.format(ip=ip))
            print '{ip} Closed'.format(ip=ip)
        elif i == 3:
            print '{ip} Failed, EOF'.format(ip=ip)
    finally:
        cls.close()


def test_ssh():
    for info in SSH_INFO:
        test_ip(info['ip'])


def free_ssh():
    key_gen()
    print 'Copy SSH Key to slaves...'
    for info in SSH_INFO:
        key_copy(info['ip'], info['password'])
    print 'Copy Complete'

def close_ssh():
    for info in SSH_INFO:
        close_ip(info['ip'])


def main(args):
    if args['--test']:
        test_ssh()
    if args['--free']:
        free_ssh()
    if args['--close']:
        close_ssh()




if __name__ == '__main__':
    args = docopt(__doc__, version='1.0.0')
    main(args)
