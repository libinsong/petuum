#!/usr/bin/env python
# coding=utf-8


PC_GROUP = {
    'mytest_1': {
        'ip': '172.17.13.26',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'mytest_2': {
        'ip': '172.17.13.33',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'mytest': {
        'ip': '172.17.11.71',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'newtest': {
        'ip': '172.17.11.223',
        'out_ip': '118.244.224.8',
        'password': 'whywkl305'
    },
    'newtest2': {
        'ip': '172.17.11.22',
        'out_ip': 'None',
        'password': 'whywkl305'
    },
    'empty': {
        'ip': '172.17.11.61',
        'out_ip': 'None',
        'password': 'whywkl305'
    }
}

SETUP_CMD = [
    'sudo apt-get install gcc-4.8 g++-4.8\n',
    'sudo apt-get install autoconf libtool uuid-dev openssh-server\n',
    'sudo apt-get install libopenmpi-dev libssl-dev\n'
]

SSH_INFO = [
    PC_GROUP['newtest2']
]


SOURCE_COPY = {
    'newsrc': 'newsrc',
    'src': '/etc/apt/sources.list',
    'dest': '/etc/apt/sources.list.back'
}
FILE_COPY = {
    'third_party_lib': {
        'from': '/root/petuum_files/src/',
        'to': '/root/petuum/third_party/'
    },
    'archives': {
        'from': '/root/petuum_files/offlinePackage',
        'to': '/root/'
    }
}
SOURCE_LIST = {
    'newsrc': '/root/newsource',
    'src': '/etc/apt/sources.list',
    'backsrc': '/etc/apt/sources.list.back'

}

PETUUM_PROJECT = {
    'from': '/root/petuum/',
    'to': '/root/'
}









