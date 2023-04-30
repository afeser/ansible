from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import collections
import sys
import tempfile

from units.compat.mock import Mock
from units.compat import unittest

import os
from os.path import dirname, basename

try:
    from ansible.modules.find import (
        main,
        contentfilter,
        sizefilter,
        pfilter
    )
    from ansible.module_utils.basic import FILE_COMMON_ARGUMENTS
except Exception:
    # Need some more module_utils work (porting urls.py) before we can test
    # modules.  So don't error out in this case.
    if sys.version_info[0] >= 3:
        pass


class AptExpandPkgspecTestCase(unittest.TestCase):
    def test_find_file(self):
        """
        This is very basic test.
        Just create a file and find it using Ansible find module.
        """
        my_file = tempfile.NamedTemporaryFile(prefix='test_find_file')
        file_name = my_file.name


        global FILE_COMMON_ARGUMENTS
        FILE_COMMON_ARGUMENTS['paths'] = dirname(file_name)
        
        # TODO: how do we test this function?
        # main()

    def test_contentfilter(self):
        """
        Create a temporary file and test if content filter works.
        """
        my_file = tempfile.NamedTemporaryFile(prefix='test_contentfilter')
        file_name = my_file.name
        with open(file_name, 'w') as f:
            # just add my_pattern substring
            f.write('hj98239f8hsj\n\n\3434erermy_pattern\nsf32ffd\n')

        self.assertTrue(contentfilter(file_name, 'my_pattern'))
        self.assertFalse(contentfilter(file_name, 'no_my_pattern'))
        self.assertTrue(contentfilter(file_name, 'my_pattern'), False)
        self.assertFalse(contentfilter(file_name, 'no_my_pattern'), False)

        
    def test_pfilter(self):
        """
        """
        file_name = 'test_pfilter_some_file_name.txt'
        self.assertTrue(pfilter(file_name, patterns=[file_name]))
        self.assertFalse(pfilter(file_name, patterns=[file_name], excludes=[file_name]))
        self.assertTrue(pfilter(file_name, patterns=['test_pfilter*'], use_regex=True))
        self.assertFalse(pfilter(file_name, patterns=['test_pfilter*'], excludes=[file_name], use_regex=True))

    
    def test_sizefilter(self):
        """
        """
        my_file = tempfile.NamedTemporaryFile(prefix='test_sizefilter')
        file_name = my_file.name
        with open(file_name, 'w') as f:
            # just add my_pattern substring
            f.write('x'*10000) # 10000 bytes..
        
        # file is greater than 9999 and 10001 bytes
        self.assertTrue(sizefilter(os.lstat(file_name), 9999))
        self.assertFalse(sizefilter(os.lstat(file_name), 10001))

        # file is less than 9999, 10001 bytes (other branch)
        self.assertTrue(sizefilter(os.lstat(file_name), -10001))
        self.assertFalse(sizefilter(os.lstat(file_name), -9999))
        