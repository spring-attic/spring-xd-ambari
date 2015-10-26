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

from resource_management import *

def springxd_service(action='none', name='none'):
  import params
  import status_params

  pid_file = format("{pid_dir}/springxd_{name}.pid")
  no_op_test = format("ls {pid_file} >/dev/null 2>&1 && ps `cat {pid_file}` >/dev/null 2>&1")

  if name == 'admin':
    process_grep = "AdminServerApplication"
  elif name == 'container':
    process_grep = "ContainerServerApplication"
  elif name == 'hsql':
    process_grep = "HsqlServerApplication"

  find_proc = format("{jps_binary} -l  | grep {process_grep}")
  write_pid = format("{find_proc} | awk {{'print $1'}} > {pid_file}")
  crt_pid_cmd = format("{find_proc} && {write_pid}")

  if action == 'start':
    if name == 'admin':
      process_cmd = format("source {conf_dir}/springxd-admin-env.sh ; /opt/pivotal/spring-xd/xd/bin/xd-admin > {log_dir}/admin.out 2>&1")
    elif name == 'hsql':
      process_cmd = format("source {conf_dir}/springxd-admin-env.sh ; /opt/pivotal/spring-xd/hsqldb/bin/hsqldb-server --xd.data.home={data_dir} --hsql.server.port={hsql_port} > {log_dir}/hsql.out 2>&1")
    else:
      process_cmd = format("source {conf_dir}/springxd-container-env.sh ; /opt/pivotal/spring-xd/xd/bin/xd-container > {log_dir}/container.out 2>&1")

    Execute(process_cmd,
           user=params.springxd_user,
           wait_for_finish=False
    )

    Execute(crt_pid_cmd,
            user=params.springxd_user,
            logoutput=True,
            tries=6,
            try_sleep=10
    )

  elif action == 'stop':
    process_dont_exist = format("! ({no_op_test})")
    pid = format("`cat {pid_file}` >/dev/null 2>&1")
    Execute(format("kill {pid}"),
            not_if=process_dont_exist
    )
    Execute(format("kill -9 {pid}"),
            not_if=format("sleep 2; {process_dont_exist} || sleep 20; {process_dont_exist}"),
            ignore_failures=True
    )
    Execute(format("rm -f {pid_file}"))

