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

        self.private_space = os.path.join(self.test_dir, 'private')
        self.profile_space = os.path.join(self.test_dir, 'profile')
        self.public_space = os.path.join(self.test_dir, 'public')

    def tearDown(self):
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)

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
        self.assertEqual(main(argv=['keystore', 'init', '--bootstrap', 'keymint_ros',
                                    '--private-space', self.private_space,
                                    '--profile-space', self.profile_space,
                                    '--public-space', self.public_space,
                                    ]), SUCCSESS)

        for package_name in package_names:

            build_space = os.path.join(self.test_dir, 'build', package_name)
            install_space = os.path.join(self.test_dir, 'install', package_name)
            source_space = os.path.join(self.test_dir, 'src', package_name)

            # Create keystore packages
            self.assertEqual(main(argv=['keystore', 'create_pkg', package_name,
                                        '--source-space', source_space,
                                        '--private-space', self.private_space,
                                        '--profile-space', self.profile_space,
                                        '--public-space', self.public_space,
                                        ]), SUCCSESS)

            # Build keystore packages
            self.assertEqual(main(argv=['keystore', 'build_pkg',
                                        os.path.join(self.test_dir, 'src', package_name),
                                        '--build-space', build_space,
                                        '--install-space', install_space,
                                        '--private-space', self.private_space,
                                        '--public-space', self.public_space,
                                        '--skip-install']), SUCCSESS)

            # Install keystore packages
            self.assertEqual(main(argv=['keystore', 'build_pkg',
                                        os.path.join(self.test_dir, 'src', package_name),
                                        '--build-space', build_space,
                                        '--install-space', install_space,
                                        '--private-space', self.private_space,
                                        '--public-space', self.public_space,
                                        '--skip-build']), SUCCSESS)


if __name__ == '__main__':
    unittest.main
