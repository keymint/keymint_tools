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

import em

from keymint_comarmor.permissions import ComArmorPermissionsHelper

# from keymint_keymake.exceptions import InvalidPermissionsXML, InvalidGovernanceXML
from keymint_keymake.governance import DDSGovernanceHelper
from keymint_keymake.permissions import DDSPermissionsHelper
from keymint_keymake.identities import DDSIdentitiesHelper
from keymint_keymake.authorities import DDSAuthoritiesHelper
from keymint_package import templates

from keymint_tools.policy_type import PolicyAction, PolicyType

from keymint_tools.context import ContextExtender


class KeymintROS2ComarmorPolicyType(PolicyType):
    policy_type = 'keymint_ros2_comarmor'
    description = 'comarmor policy for ROS 2'

    # def extend_context(self, opts):
    #     ce = ContextExtender()
    #     ce.add('skip_build', opts.skip_build)
    #     ce.add('skip_install', opts.skip_install)
    #     return ce

    # def prepare_arguments(self, parser):
    #     return parser

    def on_init(self, context):
        self.dds_authorities_helper = DDSAuthoritiesHelper()
        yield PolicyAction(self._init_action, type='function')

    def _init_action(self, context):
        if context.profile_manifest.authorities is not None:
            if not context.skip_build:
                print("++++ Building Authorities")
                dds_authorities_iter = self.dds_authorities_helper.build_iter(context)
                for dds_authority in dds_authorities_iter:
                    print("+++++ Building '{0}'".format(dds_authority['name']))
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

            if not context.skip_install:
                print("++++ Installing Authorities")
                dds_authorities_iter = self.dds_authorities_helper.install_iter(context)
                for dds_authority in dds_authorities_iter:
                    print("+++++ Installing '{0}'".format(dds_authority['name']))
                    dds_csr_file = os.path.join(
                        context.public_space,
                        dds_authority['name'] + '.cert.pem')
                    with open(dds_csr_file, 'wb') as f:
                        f.write(dds_authority['dds_cert']['bytes'])


    def on_create_pkg(self, context):
        self.comarmor_permissions_helper = ComArmorPermissionsHelper()
        self.dds_permissions_helper = DDSPermissionsHelper()
        self.dds_governance_helper = DDSGovernanceHelper()
        self.dds_identities_helper = DDSIdentitiesHelper()
        yield PolicyAction(self._create_pkg_action, type='function')

    def _create_pkg_action(self, context):
        print("++++ Creating '{0}'".format('permissions.xml'))
        permissions_str = self.comarmor_permissions_helper.create(context)
        permissions_file = os.path.join(context.source_space, 'permissions.xml')
        with open(permissions_file, 'w') as f:
            f.write(permissions_str)

        config = {
            'pkg_name': context.pkg_name,
            'package_type': "keymint_ros2_dds"
        }

        def expand_template(meta_name):
            meta_template_file = templates.get_package_template_path(meta_name + '.em')
            with open(meta_template_file, 'r') as f:
                meta_template_str = f.read()
            meta_str = em.expand(meta_template_str, config)
            meta_file = os.path.join(context.source_space, meta_name)
            with open(meta_file, 'w') as f:
                f.write(meta_str)

        print("++++ Creating '{0}'".format('governance.xml'))
        expand_template('governance.xml')

        print("++++ Creating '{0}'".format('identities.xml'))
        expand_template('identities.xml')

        print("++++ Creating '{0}'".format('keymint_package.xml'))
        expand_template('keymint_package.xml')

        src = os.path.join(context.profile_space, 'package.defaults')
        dst = os.path.join(context.source_space, 'package.defaults')
        if not os.path.isdir(dst):
            os.symlink(src=src, dst=dst)
