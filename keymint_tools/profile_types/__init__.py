# Copyright 2015 Open Source Robotics Foundation, Inc.
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

from collections import Counter

import pkg_resources

KEYMINT_PROFILE_TYPES_ENTRY_POINT = 'keymint.profile_types'


def profile_exists_at(path):
    for profile_type in get_profile_types():
        if profile_type['profile_exists_at'](path):
            return True
    return False


def parse_profile(path):
    for profile_type in get_profile_types():
        if profile_type['profile_exists_at'](path):
            pkg = profile_type['parse_profile'](path)
            return pkg
    raise RuntimeError("Failed to parse profile in '%s'" % path)


def bootstrap_profile(path, profile_type):
    for _profile_type in get_profile_types():
        if profile_type == _profile_type['name']:
            _profile_type['bootstrap_profile'](path)
            return True
    raise RuntimeError("Failed to find profile_type: '%s'" % profile_type)


_cached_profile_types = None


def get_profile_types(force_loading_entry_points=False):
    global _cached_profile_types
    if _cached_profile_types is None or force_loading_entry_points:
        entry_points = list(pkg_resources.iter_entry_points(
            group=KEYMINT_PROFILE_TYPES_ENTRY_POINT))
        if not entry_points:
            raise RuntimeError('No profile type entry points')
        entry_points_data = [ep.load() for ep in entry_points]

        # ensure unique names
        counter = Counter()
        counter.update([d['name'] for d in entry_points_data])
        most_common = counter.most_common(1)[0]
        if most_common[1] > 1:
            raise RuntimeError("Multiple profile types with the same name '%s'" % most_common[0])

        # order topologically
        ordered = []
        by_name = {d['name']: [set(d['depends']), d] for d in entry_points_data}
        while by_name:
            for name in sorted(by_name.keys()):
                depends = by_name[name][0]
                # take first entry with no unsatisfied dependencies
                if not depends:
                    data = by_name[name][1]
                    ordered.append(data)
                    del by_name[name]
                    # remove name from dependency list of other entries
                    for v in by_name.values():
                        v[0].remove(name)
                    break
            else:
                raise RuntimeError(
                    'Failed to determine topological order of the following profile types: ' +
                    (', '.join(sorted(by_name.keys()))))
        _cached_profile_types = ordered

    return _cached_profile_types
