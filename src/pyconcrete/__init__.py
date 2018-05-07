import sys
import importlib
import importlib.abc
import marshal
from os.path import join, exists, isdir
import os
import base64


from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


EXT_PY  = '.py'
EXT_PYC = '.pyc'
EXT_PYD = '.pyd'
EXT_PYE = '.pye'


__all__ = ["init"]


SALT_SIZE = 16
_KEY = None


def encrypt_file(pyc_file, pye_file, password):
    salt = os.urandom(SALT_SIZE)
    key = generate_key(password, salt)
    f = Fernet(key)
    with open(pyc_file, 'rb') as fin:
        data = fin.read()
    with open(pye_file, 'wb') as fout:
        encrypted = f.encrypt(data)
        fout.write(salt)
        fout.write(encrypted)


def decrypt_file(path):
    with open(path, 'rb') as f:
        encrypted_data = f.read()
        print(encrypted_data)
    return decrypt_buffer(encrypted_data)


def decrypt_buffer(data):
    assert _KEY
    salt, data = data[:SALT_SIZE], data[SALT_SIZE:]
    print(salt, data)
    key = generate_key(_KEY, salt)
    f = Fernet(key)
    return f.decrypt(data)


class PyeLoader(importlib.abc.SourceLoader):
    def __init__(self, is_pkg, pkg_path, full_path):
        self.is_pkg = is_pkg
        self.pkg_path = pkg_path
        self.full_path = full_path

    def get_data(self, path):
        with open(path, 'rb') as f:
            encrypted_data = f.read()
            print(encrypted_data)
        data = decrypt_buffer(encrypted_data)
        print(data)
        return data

    def get_filename(self, fullname):
        return self.full_path


class PyeMetaPathFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        print('Looking for {}:{}'.format(fullname, path))
        loader = self.get_loader(fullname, path)
        if loader:
            return importlib.util.spec_from_loader(fullname, loader)
        else:
            return None

    def get_loader(self, fullname, path):
        mod_name = fullname.split('.')[-1]
        paths = path if path else sys.path
        for trypath in paths:
            print('Looking for {} on {}'.format(fullname, trypath))
            mod_path = join(trypath, mod_name)
            is_pkg = isdir(mod_path)
            if is_pkg:
                full_path = join(mod_path, '__init__' + EXT_PYE)
                pkg_path = mod_path
            else:
                full_path = mod_path + EXT_PYE
                pkg_path = trypath
            if exists(full_path):
                return PyeLoader(is_pkg, pkg_path, full_path)


def generate_key(password, salt):
    password_as_bytes = password.encode('utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(password_as_bytes))


def init(password):
    global _KEY
    _KEY = password
    sys.meta_path.insert(0, PyeMetaPathFinder())
