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

import inspect
import os
import shlex
import subprocess
import sys


def run_command(base_action, context, default_cwd):
    cwd = base_action.cwd
    if cwd is None:
        cwd = default_cwd  # context.build_space
    print("==> '{0}' in '{1}'".format(' '.join(base_action.cmd), cwd))
    # flush Python output before letting the external command write to the pipe
    sys.stdout.flush()
    try:
        cmd = base_action.cmd
        if os.name != 'nt':
            cmd = ' '.join([(shlex.quote(c) if c != '&&' else c) for c in cmd])
        subprocess.check_call(cmd, shell=True, cwd=cwd, env=base_action.env)
    except subprocess.CalledProcessError as exc:
        print()
        cmd_msg = exc.cmd
        if isinstance(cmd_msg, list):
            cmd_msg = ' '.join(cmd_msg)
        msg = "<== Command '{0}' failed in '{1}' with exit code '{2}'" \
            .format(cmd_msg, cwd, exc.returncode)
        print(msg, file=sys.stderr)
        sys.exit(msg)


def handle_base_action(base_action_ret, context, default_cwd):
    if not inspect.isgenerator(base_action_ret):
        return
    for base_action in base_action_ret:
        if base_action.type == 'command':
            run_command(base_action, context, default_cwd)
        elif base_action.type == 'function':
            base_action.cmd(context)
        else:
            raise RuntimeError("Unknown ProfileAction type '{0}'"
                               .format(base_action.type))
