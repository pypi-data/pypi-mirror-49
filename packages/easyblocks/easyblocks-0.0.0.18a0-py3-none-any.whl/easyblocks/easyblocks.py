#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rocksdb
from . import utils
import logging


class Blockchain:

    # meta_ -> labels ro by the user
    # labels_ -> labels rw by the user
    # block_ -> blocks ro
    # hash_ -> blocks ro
    # height_ -> blocks ro

    @staticmethod
    def _get_block_key(height, prev_hash):
        return f'{utils.get_padded_int(height)}_{prev_hash}'

    def __init__(self, chain_dir='./chaindata', signature_checker=None):
        self._db = rocksdb.DB(f'{chain_dir}', rocksdb.Options(create_if_missing=True))
        if signature_checker:
            self.signature_checker = signature_checker
        self._write_batch = None

    def put(self, key, value):
        self._put(f'label_{key}', value)

    def get(self, key):
        return self._get(f'label_{key}')

    def add_block(self, block_dict):
        self.begin_write_batch()
        height = self._increment_height()
        if self.get_block_by_hash(block_dict['hash']):
            raise PermissionError
        if not self._prev_hash_is_correct(height, block_dict['prev_hash']):
            raise PermissionError
        if not self._signature_is_valid(block_dict):
            raise PermissionError
        key = self._get_block_key(height, block_dict['hash'])
        self._put(key, block_dict, prefix='block_')  # height, block_hash -> block_dict
        self._put(height, block_dict['hash'], prefix='height_')  # height -> block_hash
        self._put(block_dict['hash'], height, prefix='hash_')  # block_hash -> height
        self.commit_write_batch()

    def get_block_by_height(self, height):
        block_hash = utils.bytes_to_str(self._get(height, prefix='height_'))
        return self._get_block(height, block_hash)

    def get_block_by_hash(self, block_hash):
        height = utils.bytes_to_int(self._get(block_hash, prefix='hash_'))
        return self._get_block(height, block_hash)

    def get_block_hash_by_height(self, height):
        return utils.bytes_to_str(self._get(height, prefix='height_'))

    def get_block_height_by_hash(self, block_hash):
        return utils.bytes_to_int(self._get(block_hash, prefix='hash_'))

    def get_height(self):
        height = utils.bytes_to_int(self.get_meta('height'))
        return height

    def get_meta(self, key):
        return self._get(key, prefix='meta_')

    def print_chain(self):
        for key, value in self._db.iterator(prefix=b'block_'):
            height = key.decode('utf-8').split('_')[1]
            block_dict = utils.dump_pretty_dict(utils.load_dict(utils.bytes_to_str(value)))
            print(f'Height: {height}')
            print(block_dict)
            print()

    def print_meta(self):
        for key, value in self._db.iterator(prefix=b'label_'):
            print(f'key: {key}, value: {value}')

    def begin_write_batch(self):
        if self._write_batch is None:
            self._write_batch = rocksdb.WriteBatch()

    def commit_write_batch(self):
        if self._write_batch is not None:
            self._db.write(self._write_batch, sync=True)
            self._write_batch = None

    def _get_block(self, height, block_hash):
        block_key = self._get_block_key(height, block_hash)
        return utils.bytes_to_dict(self._get(block_key, prefix='block_'))

    def _get(self, key, prefix=''):
        key_bytes = utils.to_bytes(f'{prefix}{key}')
        value = self._db.get(key_bytes)
        if value != b'':
            return value

    def _can_put(self, key):
        if self._db.get(key) is None \
        or key[:6] == b'label_' \
        or key[:5] == b'meta_':
            return True
        else:
            return False

    def _put(self, key, value, prefix=''):
        key = utils.to_bytes(f'{prefix}{key}')
        value_bytes = utils.to_bytes(value)
        if not self._can_put(key):
            raise PermissionError
        if self._write_batch is not None:
            self._write_batch.put(key, value_bytes)
        else:
            self._db.put(key, value_bytes, sync=True)

    def _increment_height(self):
        height = self.get_height()
        if height is None:
            height = 0
        else:
            height += 1
        self._put('height', height, prefix='meta_')
        return height

    def _prev_hash_is_correct(self, current_height, prev_hash):
        if self.get_height() is None:
            return True

        prev_height = self.get_block_height_by_hash(prev_hash)
        if prev_height != current_height - 1:
            return False

        block_dict = self.get_block_by_hash(prev_hash)
        if not block_dict:
            return False

        if block_dict['hash'] == prev_hash:
            return True

        return False

    def _signature_is_valid(self, block_dict):
        if not hasattr(self, 'signature_checker'):
            return True

        if not 'signature' in block_dict:
            return False
        return self.signature_checker(block_dict['signature'])