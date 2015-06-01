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

import sys
from resource_management import *

from springxd import springxd
from springxd_service import springxd_service

class SpringXdContainer(Script):

  def install(self, env):
    self.install_packages(env)

  def configure(self, env):
    import params
    env.set_params(params)
    springxd(name='container')

  def start(self, env):
    import params
    env.set_params(params)
    self.configure(env)
    springxd_service(action = 'start', name = 'container')

  def stop(self, env):
    import params
    env.set_params(params)
    springxd_service(action = 'stop', name = 'container')

  def status(self, env):
    import status_params
    env.set_params(status_params)
    check_process_status(status_params.container_pid_file)

if __name__ == "__main__":
  SpringXdContainer().execute()
