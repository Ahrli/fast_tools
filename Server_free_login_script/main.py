#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' a test module '
import time

__author__ = 'Ahrli Tao'
import paramiko
# username = "ahrli"
# password = "123456"
'''需要免密码登录服务器列表'''
##################  修改这里 别的不要动  ##########################
# 用户 ip 密码
hostname_list=[
('root','192.168.0.108','123456'),
]
############################################
def ssh_pub(hostname,username,password):
    '''生成id_rsa.pub'''
    # 创建SSH对象
    ssh = paramiko.SSHClient()

    # 把要连接的机器添加到known_hosts文件中
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 连接服务器
    ssh.connect(hostname=hostname, port=22, username=username, password=password)

    cmd = 'ssh-keygen -t  rsa'

    # 相当于建立一个terminal 不过每条命令都要自己加\n
    chan = ssh.invoke_shell(cmd)
    chan.send(cmd + '\n')
    time.sleep(0.3)
    chan.send('\n')
    time.sleep(0.3)
    chan.send('\n')
    time.sleep(0.3)
    chan.send('\n')
    time.sleep(0.3)
    chan.send('\n')
    time.sleep(0.3)
    chan.send('\n')
    time.sleep(0.3)
    # print(chan.recv(1024))
    chan.close()
    ssh.close()

def ssh_red(hostname,username,password):
    '''生成id_rsa.pub'''
    # 创建SSH对象
    ssh = paramiko.SSHClient()

    # 把要连接的机器添加到known_hosts文件中
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 连接服务器
    ssh.connect(hostname=hostname, port=22, username=username, password=password)


    cmd2 = 'cd ~/.ssh/;cat id_rsa.pub '

    # cmd = 'ls -l;ifconfig'       #多个命令用;隔开
    # 第一可以写回车命令vim 等操作 错误信息 成功信息

    stdin, stdout, stderr = ssh.exec_command(cmd2)
    result = stdout.read()
    if not result:
        result = stderr.read()
    ssh.close()

    print(result.decode())
    return result.decode()


def sftp_file(hostname,username,password):
    # 创建SSH对象
    t = paramiko.Transport((hostname, 22))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put('authorized_keys', '/root/.ssh/authorized_keys')
    t.close()


def main():
    """记下秘钥 每台机器发送秘钥"""
    for i in hostname_list:
        username, hostname, password = i
        ssh_pub(hostname, username, password)
        a = ssh_red(hostname, username, password)
        with open('authorized_keys', 'a+') as f:
            f.write(a)
    for i in hostname_list:
        username, hostname, password = tuple(i.split("@"))
        if username not in 'ahrli':
            sftp_file(hostname, username, password)



if __name__ == '__main__':
    main()



