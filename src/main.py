# Takes 3 arguments.
# 1. The input csv file
# 2. The encryption key file
# 3. The database address

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from constant import *
import extract
import os.path
import rewriter
import transform
import sys


class ColumnAnnotation:
    def __init__(self, data_tag, rewrite_func):
        self.data_tag = data_tag
        self.rewrite_func = rewrite_func


class Environment:
    def __init__(self, key):
        self.metric = Metric()
        self.key = key
        self.rewrite_fns = {
            COLUMN_ID: rewriter.rewrite_id,
            COLUMN_FIRST_NAME: rewriter.encryption_rewrite(COLUMN_FIRST_NAME, key, "NAME_PII"),
            COLUMN_LAST_NAME: rewriter.encryption_rewrite(COLUMN_LAST_NAME, key, "NAME_PII"),
            COLUMN_EMAIL: rewriter.encryption_rewrite(COLUMN_EMAIL, key, "EMAIL_PII"),
            COLUMN_PHONE: rewriter.encryption_rewrite(COLUMN_PHONE, key, "PHONE_NUMBER_PII"),
            COLUMN_IP_ADDRESS: rewriter.rewrite_ip(key, "IP_PSEUDO_PII"),
            COLUMN_CC_NUMBER: rewriter.encryption_rewrite(COLUMN_CC_NUMBER, key, "CC_NUMBER_PCI"),
        }


def init_env(key_file):
    return Environment(get_encryption_key(key_file))


def get_encryption_key(key_file):
    """Read the key from key_file. If the file does not exist, or if the file does not contain a valid key, generate the
     key and store it in the key file"""
    if not os.path.exists(key_file):
        return generate_encryption_key(key_file)
    f = open(key_file, "rb")
    key = f.read()
    f.close()
    if len(key) != KEY_SIZE:
        return generate_encryption_key(key_file)
    return key


def generate_encryption_key(key_file):
    f = open(key_file, "wb")
    key = get_random_bytes(KEY_SIZE)
    f.write(key)
    f.close()
    return key


class Metric:
    def __init__(self):
        self.success = 0
        self.failure = 0
        self.masked = {}

    def increment(self, data_annotation):
        if data_annotation in self.masked:
            self.masked[data_annotation] += 1
        else:
            self.masked[data_annotation] = 1

    def print(self):
        if self.success > 0:
            print("Process completed successfully for %d records" % self.success)
        if self.failure > 0:
            print("Process failed for %d records" % self.failure)
        for k, v in self.masked.items():
            print("Identified and masked %d %s" % (v, k))


if __name__ == "__main__":
    env = init_env(sys.argv[2])
    reader = extract.open_csv(sys.argv[1])
    count = 0
    for row in reader:
        print(row)
        print(transform.transform_row(env, row))
        print("\n")
        count += 1
        if count == 10:
            pass
            #break
    env.metric.print()
