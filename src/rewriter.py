from constant import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from ipaddress import ip_address,ip_network


def rewrite_id(val, metric):
    if not val.isnumeric():
        return {}
    return {COLUMN_ID: int(val)}


def encryption_rewrite(column, key, data_annotation):
    def encrypt(val, metric):
        n = get_random_bytes(NONCE_SIZE)
        cipher = AES.new(key, AES.MODE_GCM, nonce=n)
        encrypted = n + cipher.encrypt(bytes(val, 'utf-8'))
        metric.increment(data_annotation)
        return {column: VALUE_REDACTED, column+"_raw": encrypted}
    return encrypt


def rewrite_ip(key, data_annotation):
    def rewrite(val, metric):
        try:
            ip_address(val)
        except ValueError:
            return {}
        n = get_random_bytes(NONCE_SIZE)
        cipher = AES.new(key, AES.MODE_GCM, nonce=n)
        encrypted = n + cipher.encrypt(bytes(val, 'utf-8'))
        masked = '.'.join(val.split('.')[:-1]) + '.' + VALUE_REDACTED
        metric.increment(data_annotation)
        return {COLUMN_IP_ADDRESS: masked, COLUMN_IP_ADDRESS+"_raw": encrypted}
    return rewrite

