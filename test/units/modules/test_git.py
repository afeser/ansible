from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys
import tempfile
import traceback

import unittest
from units.compat.mock import patch, MagicMock, mock_open
from units.modules.utils import ModuleTestCase
from ansible.modules.git import relocate_repo, head_splitter, create_archive

import os



@unittest.skipIf(sys.version_info.major == 2, "Skipping test for Python 2.x")
class AptExpandPkgspecTestCase(ModuleTestCase):
    def test_relocate_repo(self):
        """
        Create different types of files and directories to test if relocation will work.
        """
        file_a = tempfile.NamedTemporaryFile()
        file_b = tempfile.NamedTemporaryFile()

        source_repo_dir = tempfile.TemporaryDirectory()
        new_repo_dir = tempfile.TemporaryDirectory()

        relocate_repo(MagicMock(), [], new_repo_dir.name, source_repo_dir.name, False)
        relocate_repo(MagicMock(), [], new_repo_dir.name, source_repo_dir.name, source_repo_dir.name)

        # Create broken link
        temp_dir = tempfile.TemporaryDirectory()
        
        cmd = 'cd ' + str(temp_dir.name) + ' && ln -s non_existing_broken_link'
        os.system(cmd)
        
        relocate_repo(MagicMock(), [], temp_dir.name, new_repo_dir.name, new_repo_dir.name)


    def test_head_splitter(self):
        """
        Try rational and non-sense strings.
        """
        temp_file = tempfile.NamedTemporaryFile()

        with open(temp_file.name, 'w') as f:
            f.write('mock_1/mock_2/abc/s')
        
        res = head_splitter(temp_file.name, remote = '')
        self.assertEqual(res, 'abc/s')

        temp_file = tempfile.NamedTemporaryFile()


        res = head_splitter('/non_existing_file', remote = '')
        self.assertEqual(res, None)


        temp_file_2 = tempfile.NamedTemporaryFile()

        with open(temp_file_2.name, 'w') as f:
            f.write('none')
        res = head_splitter(temp_file_2.name, remote = '')


    def test_create_archive(self):
        """
        Try to crash program here.
        """
        
        temp_dir = tempfile.TemporaryDirectory()
        
        cmd = 'cd ' + str(temp_dir.name) + ' && ln -s non_existing_broken_link'
        os.system(cmd)
        
        class MyMockClass:
            def run_command(*args, **kwargs):
                return('', '', '')
            def fail_json(*args, **kwargs):
                pass
            
        git_path = ''
        # module = MagicMock(return_value=('', '', '')) # this does not work for some reason
        module = MyMockClass()
        dest = ''
        archive = os.path.join(temp_dir.name, 'non_existing_broken_link')
        archive_prefix = ''
        version = ''
        repo = 'a/b/c/d'
        result = MagicMock()
        
        try:
            create_archive(git_path, module, dest, archive, archive_prefix, version, repo, result)
        except Exception as e:
            self.fail("Should not have thrown an exception " + str(e) + traceback.format_exc())
