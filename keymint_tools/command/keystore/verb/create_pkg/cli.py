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
from keymint_tools.context import Context
from keymint_tools.helper import determine_path_argument

from keymint_tools.command.keystore.verb.init.cli import (
    _get_cached_profile_manifest,
    get_policy_type,
    handle_policy_action,
)


def validate_package_name(name):
    """
    Assert the given name follows naming conventions.

    :param str name: name of the package
    :raises: ValueError if name does not follow naming conventions
    """
    valid_package_name_regexp = '([^/ ]+/*)+(?<!/)'
    if not re.match(valid_package_name_regexp, name):
        raise ValueError("Package name '{0}' does not follow naming conventions".format(name))


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

    pkg_name = context.profile_manifest.name

    if not os.path.exists(context.source_space) and not context.dry_run:
        os.makedirs(context.source_space, exist_ok=True)

    # Run the create command
    print("+++ Creating '{0}'".format(pkg_name))
    on_create_pkg_ret = policy_type_impl.on_create_pkg(context)
    handle_policy_action(on_create_pkg_ret, context, context.source_space)


def update_options(opts):
    try:
        validate_package_name(opts.name)
    except ValueError as exc:
        sys.exit('Error: {0}'.format(exc))

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

    pkg_name = opts.name
    pkg_namespace = os.path.normpath(pkg_name)
    default_source_space = os.path.join('src', pkg_namespace)
    opts.source_space = determine_path_argument(cwd, opts.directory,
                                           opts.source_space, default_source_space)


def create_context(opts):
    # Setup init profile context
    context = Context()
    context.profile_manifest = _get_cached_profile_manifest(opts.profile_space)
    prf_name = context.profile_manifest.name
    context.pkg_name = opts.name

    context.source_space = opts.source_space
    context.profile_space = opts.profile_space
    context.public_space = opts.public_space
    context.private_space = opts.private_space
    # context.symlink_install = opts.symlink_install
    context.dry_run = False
    print('')
    print("Utilizing profile '{0}' with context:".format(prf_name))
    print('-' * 80)
    keys = [
        'source_space',
        'profile_space',
        'public_space',
        'private_space',
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
