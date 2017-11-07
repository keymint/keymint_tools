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
"""Common Keystore API."""

import logging
import os

from sros2keystore.utils import context, metadata

logger = logging.getLogger(__name__)


class KeyStore:
    """KeyStore Base Class."""

    def __init__(self, profile, storage, transport):
        """Initlise KeyStore with profile, storage, transport interfaces."""
        self.profile = profile
        self.storage = storage
        self.transport = transport


class ContextError(Exception):
    """Context Error Class."""

    pass


def get_context(workspace):
    """Get workspace context."""
    # Load a context with initialization
    ctx = context.Context.load(workspace, strict=True)

    # Check the workspace
    if ctx:
        logger.info('Keystore workspace was found.')
    else:
        logger.info('Keystore workspace not found.')
        raise ContextError("Keystore workspace not found. "
                           "Please initialize a keystore workspace.")

    return ctx


def init_context(workspace, reset):
    """Initialize workspace context."""
    # Load a context with initialization
    ctx = context.Context.load(workspace, strict=True)

    # Initialize the workspace if necessary
    if ctx:
        logger.info('Keystore workspace already exists.')
        print(("Keystore workspace `{workspace}` is already initialized. "
              "No action taken.").format(workspace=ctx.workspace))
    else:
        workspace_path = workspace or os.getcwd()
        logger.info('Keystore workspace was created.')
        print("Initializing keystore workspace in `{workspace}`.".format(
            workspace=workspace_path))
        # initialize the workspace
        metadata.init_metadata_root(
            workspace_path=workspace_path, reset=reset)
