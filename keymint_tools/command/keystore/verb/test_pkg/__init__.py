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

from .cli import main


class TestPkgVerb(VerbExtension):
    """Test Package."""

    def add_arguments(self, parser, cli_name):
        """Add test package arguments."""
        arg = parser.add_argument(
            'path',
            nargs='?',
            type=argparse_existing_dir,
            default=os.curdir,
            help="Path to the package (default '%s')" % os.curdir,
        )
        arg.completer = FilesCompleter()
        arg = parser.add_argument(
            '--build-space',
            help="Path to the build space (default 'CWD/build')",
        )
        arg.completer = FilesCompleter()
        arg = parser.add_argument(
            '--install-space',
            help="Path to the install space (default 'CWD/install')",
        )
        arg.completer = FilesCompleter()
        parser.add_argument(
            '--skip-build',
            action='store_true',
            default=False,
            help='Skip the build step (this can be used when installing or '
                 'testing and you know that the build has successfully run)',
        )
        parser.add_argument(
            '--skip-install',
            action='store_true',
            default=False,
            help='Skip the install step (only makes sense when install has been '
                 'done before using symlinks and no new files have been added or '
                 'when testing after a successful install)',
        )

        # Allow all available build_type's to provide additional arguments
        for build_type in yield_supported_build_types():
            build_type_impl = build_type.load()()
            group = parser.add_argument_group("'{0}' build_type options"
                                              .format(build_type_impl.build_type))
            call_prepare_arguments(build_type_impl.prepare_arguments, group)

    def main(self, *, args):
        """Call test function."""
        success = main(args)
        return 0 if success else 1
