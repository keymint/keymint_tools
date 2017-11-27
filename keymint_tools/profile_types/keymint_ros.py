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

from keymint_profile import PROFILE_MANIFEST_FILENAME
from keymint_profile import profile_exists_at
from keymint_profile import parse_profile

__all__ = ('entry_point_data')

# meta information of the entry point
entry_point_data = {
    'name': 'keymint_ros',
    'description': "A profile containing a '%s' manifest file." % PROFILE_MANIFEST_FILENAME,
    'profile_exists_at': profile_exists_at,
    'parse_profile': parse_profile,
    'depends': [],
}
