# Copyright 2014 Open Source Robotics Foundation, Inc.
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
import re
import sys

from keymint_tools.policy_type_discovery import get_class_for_policy_type
# from keymint_tools.policy_type_discovery import MissingPluginError
from keymint_tools.context import Context
from keymint_tools.helper import determine_path_argument
# from ament_tools.helper import extract_argument_group
from keymint_tools.profile_types import profile_exists_at
from keymint_tools.profile_types import parse_profile

from keymint_tools.base_type_helper import handle_base_action

profile_cache_ = {}


def _get_cached_profile_manifest(path):
    global profile_cache_
    if path not in profile_cache_:
        profile_cache_[path] = parse_profile(path)
    return profile_cache_[path]


def get_policy_type(path):
    """
    Extract the policy_type from the profile manifest at the given path.

    :param str path: path to a profile manifest file
    :returns: profile_type as a string
    """
    profile = _get_cached_profile_manifest(path)

    policy_type_exports = profile.export.findall('policy_type')
    if len(policy_type_exports) > 1:
        print("The profile in '%s' exports multiple policy types" % path,
              file=sys.stderr)

    default_policy_type = '<not-specified>'
    if not policy_type_exports:
        return default_policy_type

    return policy_type_exports[0].text


def handle_policy_action(policy_action_ret, context, default_cwd):
    handle_base_action(policy_action_ret, context, default_cwd)


def main(opts):
    context = get_context(opts)
    return run(opts, context)


def get_context(opts):
    update_options(opts)
    return create_context(opts)


def run(opts, context):
    # Load up policy type plugin class
    policy_type = get_policy_type(opts.profile_space)
    policy_type_impl = get_class_for_policy_type(policy_type)()

    prf_name = context.profile_manifest.name

    # Run the create command
    print("+++ Initializing '{0}'".format(prf_name))
    on_init_ret = policy_type_impl.on_init(context)
    handle_policy_action(on_init_ret, context, context.profile_space)


def update_options(opts):
    # use PWD in order to work when being invoked in a symlinked location
    cwd = os.getenv('PWD', os.curdir)
    # no -C / --directory argument yet
    opts.directory = cwd
    opts.profile_space = determine_path_argument(cwd, opts.directory,
                                                 opts.profile_space, 'profile')
    opts.public_space = determine_path_argument(cwd, opts.directory,
                                                opts.public_space, 'public')
    opts.private_space = determine_path_argument(cwd, opts.directory,
                                                 opts.private_space, 'private')


def create_context(opts):
    # Setup init profile context
    context = Context()
    context.profile_manifest = _get_cached_profile_manifest(opts.profile_space)
    prf_name = context.profile_manifest.name

    # context.source_space = opts.source_space
    context.profile_space = opts.profile_space
    context.public_space = opts.public_space
    context.private_space = opts.private_space
    # context.symlink_install = opts.symlink_install
    context.dry_run = False
    print('')
    print("Utilizing profile '{0}' with context:".format(prf_name))
    print('-' * 80)
    keys = [
        # 'source_space',
        'private_space',
        'profile_space',
        'public_space',
    ]
    max_key_len = str(max(len(k) for k in keys))
    for key in keys:
        value = context[key]
        if isinstance(value, list):
            value = ', '.join(value) if value else 'None'
        print(('{0:>' + max_key_len + '} => {1}').format(key, value))
    print('-' * 80)

    # Load up policy type plugin class
    policy_type = get_policy_type(opts.profile_space)
    policy_type_impl = get_class_for_policy_type(policy_type)()

    # Allow the policy type plugin to process options into a context extender
    ce = policy_type_impl.extend_context(opts)
    # Extend the context with the context extender
    ce.apply_to_context(context)

    return context
