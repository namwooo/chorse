import paramiko


class Config:
    HOST_IP = 'bluewhale.kr'
    PORT = 40022
    USERNAME = 'bluewhale'
    PKEY = paramiko.RSAKey.from_private_key_file('/Users/lucakim/.ssh/jenkins_id_rsa')
