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


class BaseAction:
    """
    Represent an action to do at action time, either a command or a functor.

    These objects are yielded from the ``on_*`` methods in the BaseType class
    for a particular ``base_type``.

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

    The default working directory for commands is the action space which can be
    overridden with the optional ``cwd`` parameter.

    The environment used when running the command can be overridden using the
    the optional ``env`` parameter.
    """

    def __init__(
        self,
        cmd,
        type='command',  # noqa: A002
        title=None,
        dry_run_cmd=None,
        cwd=None,
        env=None,
    ):
        self.cmd = cmd
        self.type = self.__validate_type(type, cmd, dry_run_cmd)
        self.title = title
        self.dry_run_cmd = dry_run_cmd
        self.cwd = cwd
        self.env = env

    def __validate_type(self, type_str, cmd, dry_run_cmd):
        if type_str not in ['command', 'function']:
            raise ValueError("Invalid BaseAction type '{0}'".format(type_str))
        if cmd is None:
            return type_str
        if type_str == 'command' and not hasattr(cmd, '__iter__'):
            raise ValueError('BaseAction cmd is expected to be list or tuple '
                             "when type is 'command', got '{0}' of type "
                             "'{1}' instead.".format(cmd, type(cmd)))
        if type_str == 'function' and not callable(cmd):
            raise ValueError('BaseAction cmd is expected to be callable '
                             "when type is 'function', but '{0}' is not "
                             'callable.'.format(cmd))
        if dry_run_cmd is None:
            return type_str
        if type_str == 'command' and not hasattr(dry_run_cmd, '__iter__'):
            raise ValueError('BaseAction dry_run_cmd is expected to be list '
                             "or tuple when type is 'command', got '{0}' of "
                             "type '{1}' instead."
                             .format(dry_run_cmd, type(dry_run_cmd)))
        if type_str == 'function' and not callable(dry_run_cmd):
            raise ValueError('BaseAction cmd is expected to be callable '
                             "when type is 'function', but '{0}' is not "
                             'callable.'.format(dry_run_cmd))
        return type_str


class DefaultBaseTypeLogger:
    """
    Base class logger for using with BaseType.

    This class provides an logging for events in ``BaseType``
    """

    def info(self, *args):
        print(*args)

    def warn(self, *args):
        print(*args)


class BaseType:
    """
    Base class interface for using a ``base_type`` with keymint tools.

    This class provides an interface for how to handle using of keymint
    ``base_type``'s, but it cannot be used as is and requires subclassing.
    """

    description = None
    """
    Description of this base type.

    This should be set by the subclass.
    """

    logger = DefaultBaseTypeLogger()
    """Logging singleton, allows executor to hook in a custom logger."""

    def extend_context(self, opts):
        """
        Convert arguments into a ContextExtender object.

        Override this function to be able to convert resulting options from
        argparse into a ContextExtender object which will be used to extend
        the build Context object given to the ``on_*`` methods.

        :param opts: options from argparse, already extended with extra options
            from the ``argument_preprocessor``.
        :type opts: :py:class:`argparse.Namespace`
        :returns: A ContextExtender object.
        :rtype: :py:class:`keymint_tools.context.ContextExtender`
        """
        return ContextExtender()

    def prepare_arguments(self, parser):
        """
        Add BaseType specific arguments to the command line options.

        Override this function to extend the command line arguments using the
        provided argparse ArgumentParser.
        Also, be sure to return the parser you were given.

        For example:

        .. code:: python

            class MyBaseType(BaseType):
                def prepare_arguments(self, parser):
                    parser.add_argument('--arg', help="My new argument")
                    return parser

        Overriding this method is optional, by default it simply returns the
        parser unchanged.

        :param parser: argparse ArgumentParser to which arguments can be added.
        :type parser: :py:class:`argparse.ArgumentParser`
        :returns: The given parser.
        :rtype: :py:class:`argparse.ArgumentParser`
        """
        return parser

    def argument_preprocessor(self, args):
        """
        Process arguments before being processed with argparse.

        Override this function to perform preprocessing on the arguments
        before they are passed to argparse.
        This is sometimes necessary when argparse is not clever enough to
        handle your arguments.
        """
        extra_opts = {}
        return args, extra_opts

    def info(self, *args):
        """Log informational messages for this base."""
        self.logger.info(*args)

    def warn(self, *args):
        """Log warning messages for this base."""
        self.logger.warn(*args)
