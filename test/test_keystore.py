# Copyright 2018 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import tempfile
import unittest

from keymint_cli.cli import main

SUCCSESS = None


class TestExample(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        # Remember previous working directory
        self.pwd = os.getcwd()
        # Change to the temporary directory
        os.environ.unsetenv('PWD')
        os.chdir(self.test_dir)

    def tearDown(self):
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)
        # Change to the previous working directory
        os.chdir(self.pwd)
        os.environ['PWD'] = self.pwd

    def test_keystore_cli(self):

        package_nodes = [
            'listener',
            'talker',
        ]
        package_namespaces = [
            [''],
            ['foo'],
            ['foo', 'bar'],
        ]
        package_names = []
        for package_node in package_nodes:
            for package_namespace in package_namespaces:
                package_names.append(
                    os.path.join(
                        os.path.join(*package_namespace),
                        package_node).rstrip('/'))

        # Initialize keystore
        self.assertEqual(main(argv=['keystore', 'init', '--bootstrap',
                                    'keymint_ros']), SUCCSESS)

        # Create keystore packages
        for package_name in package_names:
            self.assertEqual(main(argv=['keystore', 'create_pkg',
                                        package_name]), SUCCSESS)

        # Build keystore packages
        for package_name in package_names:
            self.assertEqual(main(argv=['keystore', 'build_pkg',
                                        os.path.join('src', package_name),
                                        '--skip-install']), SUCCSESS)

        # Install keystore packages
        for package_name in package_names:
            self.assertEqual(main(argv=['keystore', 'build_pkg',
                                        os.path.join('src', package_name),
                                        '--skip-build']), SUCCSESS)


if __name__ == '__main__':
    unittest.main
