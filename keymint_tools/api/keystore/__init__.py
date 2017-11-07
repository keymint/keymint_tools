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

import logging

# from sros2keystore.api import profile, storage, transport
#
#
# from .common import get_context, init_context
# from .common import KeyStore

logger = logging.getLogger(__name__)


class KeyStoreManager:
    """Manager for KeyStore interface."""

    def __init__(self):
        """Initlise KeyStore Manager."""
        # self.profile_interface_class = profile.comarmor.ComArmorProfileInterface
        # self.storage_interface_class = storage.workspace.WorkspaceStorageInterface
        # self.transport_interface_class = transport.dds.DdsTransportInterface

        # self.keystore_class = KeyStore

    # def auto(self, args):
    #     """Automatically initialize, build, create, and sign keystore."""
    #     print('Automatically initialize, build, create, and sign keystore.')
    #     print(args)
    #     print("just kidding, sorry, this isn't implemented yet.")
    #     return True
    #
    # def build(self, args):
    #     """Build keystore."""
    #     logger.info('Building keystore workspace.')
    #     ctx = get_context(workspace=args.workspace)
    #
    #     print('Builds keystore; regenerating and distributes governance.')
    #     print(args)
    #     print("just kidding, sorry, this isn't implemented yet.")
    #     return True
    #
    # def create(self, args):
    #     """Create keystore entry for given namespaces."""
    #     print('Create keystore entry for given namespaces.')
    #     print(args)
    #     print("just kidding, sorry, this isn't implemented yet.")
    #     return True

    def init(self, args):
        """Initialize keystore workspace."""
        logger.info('Initializing keystore workspace.')
        # ctx = init_context(workspace=args.workspace, reset=args.reset)
        print('Create keystore entry for given namespaces.')
        print(args)
        print("just kidding, sorry, this isn't implemented yet.")
        return True

    # def sign(self, args):
    #     """Sign keystore entry for given namespaces."""
    #     print('Sign keystore entry for given namespaces.')
    #     print(args)
    #     print("just kidding, sorry, this isn't implemented yet.")
    #     return True
