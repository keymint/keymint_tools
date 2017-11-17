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

"""Implements the BuildType support for ros2 based keymint packages."""

import os
import shutil
# import re
# import shutil

from keymint_keymake.exceptions import InvalidPermissionsXML, InvalidGovernanceXML
from keymint_keymake.governance import DDSGovernanceHelper
from keymint_keymake.permissions import DDSPermissionsHelper
from keymint_keymake.identities import DDSIdentitiesHelper

from keymint_tools.build_type import BuildAction
from keymint_tools.build_type import BuildType

# from ament_tools.helper import deploy_file
#
# from keymint_tools.setup_arguments import get_data_files_mapping
# from keymint_tools.setup_arguments import get_setup_arguments_with_context


class KeymintROS2DDSBuildType(BuildType):
    build_type = 'keymint_ros2_dds'
    description = 'keymint package built for ROS 2'

    def prepare_arguments(self, parser):
        arg = parser.add_argument(
            '-f', '--force',
            action='store_true',
            help='overwrite existing builds')
        arg = parser.add_argument(
            '-u', '--unsigned',
            action='store_true',
            help='leave builds unsigned')
        return parser

    def on_build(self, context):
        self.dds_permissions_helper = DDSPermissionsHelper()
        self.dds_governance_helper = DDSGovernanceHelper()
        self.dds_identities_helper = DDSIdentitiesHelper()
        yield BuildAction(self._build_action, type='function')

    def _build_action(self, context):
        if context.package_manifest.permissions is not None:
            print("++++ Building '{0}'".format('permissions.xml'))
            dds_permissions_str = self.dds_permissions_helper.build(context)
            dds_permissions_file = os.path.join(context.build_space, 'permissions.xml')
            with open(dds_permissions_file, 'w') as f:
                f.write(dds_permissions_str)

        if context.package_manifest.governance is not None:
            print("++++ Building '{0}'".format('governance.xml'))
            dds_governance_str = self.dds_governance_helper.build(context)
            dds_governance_file = os.path.join(context.build_space, 'governance.xml')
            with open(dds_governance_file, 'w') as f:
                f.write(dds_governance_str)

        if context.package_manifest.identities is not None:
            print("++++ Building '{0}'".format(['key.pem', 'csr.pem']))
            # returns an array of identities but currently len(dds_identities) == 1
            dds_identities = self.dds_identities_helper.build(context)
            # TODO to think if multple identities should be a thing
            for dds_identity in dds_identities:
                dds_key_file = os.path.join(context.build_space, 'key.pem')
                dds_csr_file = os.path.join(context.build_space, 'csr.pem')
                with open(dds_key_file, 'wb') as f:
                    f.write(dds_identity['dds_key']['bytes'])
                with open(dds_csr_file, 'wb') as f:
                    f.write(dds_identity['dds_csr']['bytes'])

    def on_test(self, context):
        self.dds_permissions_helper = DDSPermissionsHelper()
        self.dds_governance_helper = DDSGovernanceHelper()
        yield BuildAction(self._test_action, type='function')

    def _test_action(self, context):
        try:
            dds_permissions_file = os.path.join(context.build_space, 'permissions.xml')
            if os.path.isfile(dds_permissions_file):
                print("++++ Testing '{0}'".format('permissions.xml'))
                dds_permissions_file = os.path.join(context.build_space, 'permissions.xml')
                with open(dds_permissions_file, 'r') as f:
                    dds_permissions_str = f.read()
                self.dds_permissions_helper.test(dds_permissions_str, dds_permissions_file)
        except InvalidPermissionsXML as ex:
            print(ex)

        try:
            dds_governance_file = os.path.join(context.build_space, 'governance.xml')
            if os.path.isfile(dds_governance_file):
                print("++++ Testing '{0}'".format('governance.xml'))
                dds_governance_file = os.path.join(context.build_space, 'governance.xml')
                with open(dds_governance_file, 'r') as f:
                    dds_governance_str = f.read()
                self.dds_governance_helper.test(dds_governance_str, dds_governance_file)
        except InvalidGovernanceXML as ex:
            print(ex)

    def on_install(self, context):
        self.dds_permissions_helper = DDSPermissionsHelper()
        self.dds_governance_helper = DDSGovernanceHelper()
        self.dds_identities_helper = DDSIdentitiesHelper()
        yield BuildAction(self._install_action, type='function')

    def _install_action(self, context):
        if context.package_manifest.identities is not None:
            print("++++ Install '{0}'".format(['key.pem', 'cert.pem']))
            dds_identity = {}
            # Install key
            dds_key_file = os.path.join(context.build_space, 'key.pem')
            shutil.copy(dds_key_file, context.install_space)
            # Install cert
            dds_csr_file = os.path.join(context.build_space, 'csr.pem')
            dds_cert_file = os.path.join(context.install_space, 'cert.pem')
            with open(dds_csr_file, 'rb') as f:
                dds_identity['dds_csr'] = {'bytes': f.read()}
            self.dds_identities_helper.install(context, dds_identity)
            with open(dds_cert_file, 'wb') as f:
                f.write(dds_identity['dds_cert']['bytes'])

    def _remove_empty_directories(self, context, path):
        assert path.startswith(context.install_space), \
            "The path '%s' must be within the install space '%s'" % (path, context.install_space)
        if path == context.install_space:
            return
        try:
            os.rmdir(path)
            self._remove_empty_directories(context, os.path.dirname(path))
        except OSError:
            # directory is likely not empty
            pass
