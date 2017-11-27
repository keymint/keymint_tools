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

from .context import ContextExtender
from .base_type import BaseAction, BaseType, DefaultBaseTypeLogger


class PolicyAction(BaseAction):
    """
    Represent an action to do at policy time, either a command or a functor.

    These objects are yielded from the ``on_*`` methods in the BuildType class
    for a particular ``policy_type``.

    The constructor for this class takes a cmd, a type, optionally a title,
    optionally a dry run cmd, optionally a different current working directory
    (``cwd``), and optionally different environment variables (``env``).

    The cmd (command) is either a list of arguments as strings which is meant
    to be executed as a subprocess, or a callable Python object like
    a function or a method of an object.

    The type parameter indicates the type of the action.
    Currently the possible values for this are either ``command`` or
    ``function``.

    The title (optional) is used when logging the action.

    There is also an optional parameter to the constructor, ``dry_run_cmd``
    which defaults to None.
    This parameter can be used to provide an alternative cmd for the
    dry run case, e.g. ``['git', 'push']`` might become
    ``['git', 'push', '--dry-run']``.

    The default working directory for commands is the source space which can be
    overridden with the optional ``cwd`` parameter.

    The environment used when running the command can be overridden using the
    the optional ``env`` parameter.
    """


class DefaultPolicyTypeLogger(DefaultBaseTypeLogger):
    """
    Policy class logger for using with PolicyType.

    This class provides an logging for events in ``PolicyType``
    """


class PolicyType(BaseType):
    """
    Base class interface for interpreting a ``policy_type`` with keymint tools.

    This class provides an interface for how to handle interpreting of keymint
    ``policy_type``'s, but it cannot be used as is and requires subclassing.

    When subclassing this class, the only functions which raise a
    :py:exc:`NotImplementedError` by default are :py:meth:`on_init`,
    :py:func:`on_create`.
    Therefore those functions need to be overridden.
    """

    policy_type = None
    """
    Build type identification string.

    This should be set by the subclass and should match the ``built_type``
    set in the package manifest of applicable packages.
    """

    description = None
    """
    Description of this policy type.

    This should be set by the subclass.
    """

    logger = DefaultPolicyTypeLogger()
    """Logging singleton, allows executor to hook in a custom logger."""

    def on_init(self, context):
        raise NotImplementedError

    def on_create(self, context):
        raise NotImplementedError
