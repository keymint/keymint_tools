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

"""Implements the PolicyType support for ros2 based comarmor policies."""

import os
import shutil
# import re
# import shutil

# from keymint_keymake.exceptions import InvalidPermissionsXML, InvalidGovernanceXML
# from keymint_keymake.governance import DDSGovernanceHelper
# from keymint_keymake.permissions import DDSPermissionsHelper
# from keymint_keymake.identities import DDSIdentitiesHelper
from keymint_keymake.authorities import DDSAuthoritiesHelper

from keymint_tools.policy_type import PolicyAction
from keymint_tools.policy_type import PolicyType


class KeymintROS2ComarmorPolicyType(PolicyType):
    policy_type = 'keymint_ros2_comarmor'
    description = 'comarmor policy for ROS 2'

    def prepare_arguments(self, parser):
        arg = parser.add_argument(
            '-f', '--force',
            action='store_true',
            help='overwrite existing files')
        arg = parser.add_argument(
            '-u', '--unsigned',
            action='store_true',
            help='leave builds unsigned')
        return parser

    def on_init(self, context):
        self.dds_authorities_helper = DDSAuthoritiesHelper()
        yield PolicyAction(self._init_action, type='function')

    def _init_action(self, context):
        if context.profile_manifest.authorities is not None:
            print("++++ Building '{0}'".format('authorities'))
            # returns an array of authorities
            dds_authorities = self.dds_authorities_helper.build(context)
            for dds_authority in dds_authorities:
                dds_key_file = os.path.join(
                    context.private_space,
                    dds_authority['name'] + '.key.pem')
                dds_csr_file = os.path.join(
                    context.private_space,
                    dds_authority['name'] + '.csr.pem')
                with open(dds_key_file, 'wb') as f:
                    f.write(dds_authority['dds_key']['bytes'])
                with open(dds_csr_file, 'wb') as f:
                    f.write(dds_authority['dds_csr']['bytes'])

            print("++++ Installing '{0}'".format('authorities'))
            # returns an array of authorities
            for dds_authority in dds_authorities:
                self.dds_authorities_helper.install(context, dds_authority)
                dds_csr_file = os.path.join(
                    context.public_space,
                    dds_authority['name'] + '.cert.pem')
                with open(dds_csr_file, 'wb') as f:
                    f.write(dds_authority['dds_cert']['bytes'])


    # def on_create(self, context):
    #     self.dds_permissions_helper = DDSPermissionsHelper()
    #     self.dds_governance_helper = DDSGovernanceHelper()
    #     self.dds_identities_helper = DDSIdentitiesHelper()
    #     yield PolicyAction(self._create_action, type='function')
    #
    # def _create_action(self, context):
    #     pass
