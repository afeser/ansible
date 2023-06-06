from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import collections
import os
import sys
import tempfile
import unittest as main_unittest

from units.compat.mock import Mock
from units.compat import unittest
import ansible.modules.apt as apt

try:
    from ansible.modules.apt import (
        expand_pkgspec_from_fnmatches,
    )
except Exception:
    # Need some more module_utils work (porting urls.py) before we can test
    # modules.  So don't error out in this case.
    if sys.version_info[0] >= 3:
        pass


class AptExpandPkgspecTestCase(unittest.TestCase):

    def setUp(self):
        FakePackage = collections.namedtuple("Package", ("name",))
        self.fake_cache = [
            FakePackage("apt"),
            FakePackage("apt-utils"),
            FakePackage("not-selected"),
        ]

    def test_trivial(self):
        foo = ["apt"]
        self.assertEqual(
            expand_pkgspec_from_fnmatches(None, foo, self.fake_cache), foo)

    def test_version_wildcard(self):
        foo = ["apt=1.0*"]
        self.assertEqual(
            expand_pkgspec_from_fnmatches(None, foo, self.fake_cache), foo)

    def test_pkgname_wildcard_version_wildcard(self):
        foo = ["apt*=1.0*"]
        m_mock = Mock()
        self.assertEqual(
            expand_pkgspec_from_fnmatches(m_mock, foo, self.fake_cache),
            ['apt', 'apt-utils'])

    def test_pkgname_expands(self):
        foo = ["apt*"]
        m_mock = Mock()
        self.assertEqual(
            expand_pkgspec_from_fnmatches(m_mock, foo, self.fake_cache),
            ["apt", "apt-utils"])

    
    def test_get_cache_mtime(self):
        """
        Cover all the branches and try to blow up the implementation.
        """
        if sys.version_info.major == 2:
            self.skipTest("Skipping test for Python 2.x")
            return
        
        
        file_a = tempfile.NamedTemporaryFile()
        file_b = tempfile.NamedTemporaryFile()
        # Step 1, two branches False
        apt.APT_UPDATE_SUCCESS_STAMP_PATH = '/tmp/does-not-exist'
        apt.APT_LISTS_PATH = file_b.name = '/tmp/does-not-exist'

        self.assertEqual(apt.get_cache_mtime(), 0)
        
        # Step 2, first branch True, and should return some output
        apt.APT_UPDATE_SUCCESS_STAMP_PATH = file_a.name

        try:
            apt.get_cache_mtime()
        except Exception:
            self.fail("Should not have thrown an exception")
        
        # Step 3, second branch True, and should return some output
        apt.APT_LISTS_PATH = file_b.name

        try:
            apt.get_cache_mtime()
        except Exception:
            self.fail("Should not have thrown an exception")
        
        # Step 4, branch is true, but a broken symbolic link
        temp_dir = tempfile.TemporaryDirectory()
        
        cmd = 'cd ' + str(temp_dir.name) + ' && ln -s non_existing_broken_link'
        os.system(cmd)
        apt.APT_UPDATE_SUCCESS_STAMP_PATH = os.path.join(temp_dir.name, 'non_existing_broken_link')
        apt.APT_LISTS_PATH = os.path.join(temp_dir.name, 'non_existing_broken_link')
        
        try:
            apt.get_cache_mtime()
        except Exception:
            self.fail("Should not have thrown an exception")






