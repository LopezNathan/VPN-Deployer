#!/usr/bin/env python3
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

# from digitalocean import SSHKey
# user_ssh_key = open('/home/<$USER>/.ssh/id_rsa.pub').read()
# key = SSHKey(token='secretspecialuniquesnowflake',
#              name='uniquehostname',
#              public_key=user_ssh_key)
# key.create()


def sshkey_gen_private():
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption())

    private_key = private_key.decode('utf-8')

    return private_key


def sshkey_gen_public():
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    public_key = public_key.decode('utf-8')

    return public_key
