import paramiko


def get_ssh(host_ip, port, username, pkey):
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(host_ip, port=port, username=username, pkey=pkey)
    except Exception as e:
        print(e)
        raise e

    return ssh


def close_ssh(ssh):
    ssh.close()


def ssh_execute(ssh, command):
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
    except Exception as e:
        print(e)
        raise e

    return stdout
