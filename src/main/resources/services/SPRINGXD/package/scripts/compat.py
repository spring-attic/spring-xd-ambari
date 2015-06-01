#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Ambari Agent

"""
import os
import tempfile
from resource_management.core.logger import Logger
from resource_management.core import shell

def get_full_stack_version(stack_version):
  """
  Gets stack version with build number. Uses hdp-select/distro-select to get the stack version.
  :return: Returns a stack version with build number as a string.

  """
  # copy from 1.7.1 because 1.7.0 only has hdp-select
  distro_select = "/usr/bin/distro-select"
  if not os.path.exists(distro_select):
    distro_select = "/usr/bin/hdp-select"
  # Ubuntu returns: "stdin: is not a tty", as subprocess output.
  tmpfile = tempfile.NamedTemporaryFile()
  with open(tmpfile.name, 'r+') as file:
    get_stack_version_cmd = '%s versions > %s' % (distro_select, tmpfile.name)
    code, stdoutdata = shell.call(get_stack_version_cmd)
    out = file.read()
  pass
  if code != 0 or out is None or not out.startswith(stack_version):
    Logger.warning("Could not verify stack version by calling '%s'. Return Code: %s, Output: %s." %
                   (get_stack_version_cmd, str(code), str(out)))
    return ""

  return out.strip() # this should include the build number
