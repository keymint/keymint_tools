# Copyright 2016-2017 Open Source Robotics Foundation, Inc.
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

from keymint_tools.api.keystore import KeyStoreManager
from keymint_tools.verb import VerbExtension
from keymint_tools.verb.common import FilesCompleter


class InitVerb(VerbExtension):
    """Initialize keystore."""

    def add_arguments(self, parser, cli_name):
        """Add init arguments."""
        arg = parser.add_argument(
            '-r', '--reset',
            action='store_true',
            help='reset existing workspace')
        arg = parser.add_argument(
            '-w', '--workspace',
            help='path to workspace')
        arg.completer = FilesCompleter()

    def main(self, *, args):
        """Call init function."""
        keystore_manager = KeyStoreManager()
        success = keystore_manager.init(args)
        return 0 if success else 1
