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

import os

from keymint_tools.build_type_discovery import yield_supported_build_types

from keymint_tools.helper import argparse_existing_dir

from keymint_tools.verb import VerbExtension
from keymint_tools.verb.common import FilesCompleter
# from keymint_tools.verb.common import NamespaceCompleter

from osrf_pycommon.cli_utils.verb_pattern import call_prepare_arguments

# from .cli import main


class BuildVerb(VerbExtension):
    """Build keystore."""

    def add_arguments(self, parser, cli_name):
        """Add build arguments."""
        arg = parser.add_argument(
            '-C', '--directory',
            default=os.curdir,
            help="The base path of the workspace (default '%s')" % os.curdir,
        )
        arg = parser.add_argument(
            'basepath',
            nargs='?',
            type=argparse_existing_dir,
            default=os.path.join(os.curdir, 'src'),
            help="Base path to the packages (default 'CWD/src')",
        )
        arg.completer = FilesCompleter()
        arg = parser.add_argument(
            '--only-packages',
            nargs='+', default=[],
            help='Only process a particular set of packages',
        )
        arg = parser.add_argument(
            '--skip-packages',
            nargs='*', default=[],
            help='Set of packages to skip',
        )
        arg = parser.add_argument(
            '--parallel',
            action='store_true',
            help='Enable building packages in parallel',
        )

        # Allow all available build_type's to provide additional arguments
        for build_type in yield_supported_build_types():
            build_type_impl = build_type.load()()
            group = parser.add_argument_group("'{0}' build_type options"
                                              .format(build_type_impl.build_type))
            call_prepare_arguments(build_type_impl.prepare_arguments, group)
            print(build_type)

    def main(self, *, args):
        """Call build function."""
        # success = main(args)
        success = True
        return 0 if success else 1
