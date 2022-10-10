# Takes 2 arguments.
# 1. The input csv file
# 2. The encryption key file

from constant import *
from load import SqliteLoader
import rewriter
import transform
from Crypto.Random import get_random_bytes
import csv
import os.path
import sys


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
    with open(key_file, "rb") as f:
        key = f.read()
    if len(key) != KEY_SIZE:
        return generate_encryption_key(key_file)
    return key


def generate_encryption_key(key_file):
    with open(key_file, "wb") as f:
        key = get_random_bytes(KEY_SIZE)
        f.write(key)
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
    reader = csv.DictReader(open(sys.argv[1], newline=''))
    loader = SqliteLoader()
    for row in reader:
        transformed_row = transform.transform_row(env, row)
        loader.insert([transformed_row])
    env.metric.print()
