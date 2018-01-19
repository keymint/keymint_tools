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

from keymint_tools.policy_type_discovery import yield_supported_policy_types

from keymint_tools.helper import argparse_existing_dir

from keymint_tools.verb import VerbExtension
from keymint_tools.verb.common import FilesCompleter
# from keymint_tools.verb.common import NamespaceCompleter

from osrf_pycommon.cli_utils.verb_pattern import call_prepare_arguments

from .cli import main


class InitVerb(VerbExtension):
    """Initialize Profile."""

    def add_arguments(self, parser, cli_name):
        """Add init profile arguments."""
        arg = parser.add_argument(
            '--source-space',
            help="Path to the source space (default 'CWD/src')",
        )
        arg.completer = FilesCompleter()
        arg = parser.add_argument(
            '--profile-space',
            type=argparse_existing_dir,
            help="Path to the profile space (default 'CWD/profile')",
        )
        arg.completer = FilesCompleter()
        arg = parser.add_argument(
            '--public-space',
            help="Path to the public space (default 'CWD/public')",
        )
        arg.completer = FilesCompleter()
        arg = parser.add_argument(
            '--private-space',
            help="Path to the private space (default 'CWD/private')",
        )
        arg = parser.add_argument(
            '--skip-build',
            action='store_true',
            default=False,
            help='Skip the build step (this can be used when installing or '
                 'testing and you know that the build has successfully run)',
        )
        arg = parser.add_argument(
            '--skip-install',
            action='store_true',
            default=False,
            help='Skip the install step (only makes sense when build has been '
                 'done before and no new files have been added or)',
        )
        arg = parser.add_argument(
            '--bootstrap',
            action='store',
            default=False,
            help='Bootstrap the profile step (only makes sense when no profle'
                 'is first provided to be initialized)',
        )

        # Allow all available policy_type's to provide additional arguments
        for policy_type in yield_supported_policy_types():
            policy_type_impl = policy_type.load()()
            group = parser.add_argument_group("'{0}' policy_type options"
                                              .format(policy_type_impl.policy_type))
            call_prepare_arguments(policy_type_impl.prepare_arguments, group)

    def main(self, *, args):
        """Call initialize function."""
        success = main(args)
        return 0 if success else 1
