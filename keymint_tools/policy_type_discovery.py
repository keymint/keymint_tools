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

import pkg_resources

KEYMINT_BUILD_TYPES_ENTRY_POINT = 'keymint.policy_types'


def yield_supported_policy_types(name=None):
    return pkg_resources.iter_entry_points(
        group=KEYMINT_BUILD_TYPES_ENTRY_POINT,
        name=name,
    )


class MissingPluginError(Exception):
    pass


def get_class_for_policy_type(policy_type):
    """
    Get the class for a given profile policy type.

    :param str policy_type: name of policy_type plugin, e.g. 'keymint_ros2'
    :returns: class for the requirest policy_type plugin
    :raises: RuntimeError if there are more than one plugins for a requested
        policy type.
    :raises: MissingPluginError if there is no plugin for the requested
        policy type.
    """
    entry_points = list(yield_supported_policy_types(policy_type))
    if len(entry_points) > 1:
        # Shouldn't happen, defensive
        raise RuntimeError('More than one policy_type entry_point.')
    if len(entry_points) == 0:
        raise MissingPluginError(
            "No plugin to handle a profile with policy_type '{0}'"
            .format(policy_type))
    return entry_points[0].load()
