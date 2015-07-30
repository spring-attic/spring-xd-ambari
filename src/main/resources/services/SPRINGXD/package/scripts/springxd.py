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

from resource_management import *
from yaml_utils import escape_yaml_property
import sys


def springxd(name = None):
  import params

  if name == "admin":
    params.HdfsDirectory("/xd",
                         action="create_delayed",
                         owner=params.springxd_user,
                         mode=0777
    )
    params.HdfsDirectory(params.springxd_hdfs_user_dir,
                         action="create_delayed",
                         owner=params.springxd_user,
                         mode=0777
    )
    params.HdfsDirectory(None, action="create")

  Directory(params.log_dir,
            owner=params.springxd_user,
            group=params.user_group,
            mode=0775,
            recursive=True
  )

  Directory([params.pid_dir, params.conf_dir, params.conf_modules_dir],
            owner=params.springxd_user,
            group=params.user_group,
            recursive=True
  )

  dfs_ha_map = {}
  if params.dfs_ha_enabled:
    for nn_id in params.dfs_ha_namemodes_ids_list:
      nn_host = params.config['configurations']['hdfs-site'][format('dfs.namenode.rpc-address.{dfs_ha_nameservices}.{nn_id}')]
      dfs_ha_map[nn_id] = nn_host

  configurations = params.config['configurations']['springxd-site']
  modules = params.config['configurations']['springxd-modules-site']
  sec_filtered_map = {}
  for key,value in configurations.iteritems():
    if "security" in value:
      sec_filtered_map[key] = value

  File(format("{conf_dir}/servers.yml"),
       content=Template("servers.yml.j2",
                        extra_imports=[escape_yaml_property],
                        configurations = configurations),
       owner=params.springxd_user,
       group=params.user_group
  )

  File(format("{conf_dir}/modules/modules.yml"),
       content=Template("modules.yml.j2",
                        extra_imports=[escape_yaml_property],
                        configurations = modules),
       owner=params.springxd_user,
       group=params.user_group
  )

  File(format("{conf_dir}/xd-shell.init"),
       content=Template("xd-shell.init.j2",
                        dfs_ha_map = dfs_ha_map),
       owner=params.springxd_user,
       group=params.user_group
  )

  File(format("{conf_dir}/xd-admin-logback.groovy"),
       content=Template("xd-admin-logback.groovy.j2"),
       owner=params.springxd_user,
       group=params.user_group
  )

  File(format("{conf_dir}/xd-container-logback.groovy"),
       content=Template("xd-container-logback.groovy.j2"),
       owner=params.springxd_user,
       group=params.user_group
  )

  File(format("{conf_dir}/hadoop.properties"),
       content=Template("hadoop.properties.j2",
                        dfs_ha_map = dfs_ha_map,
                        sec_filtered_map = sec_filtered_map),
       owner=params.springxd_user,
       group=params.user_group
  )

  File(format("{conf_dir}/springxd-admin-env.sh"),
    owner=params.springxd_user,
    content=InlineTemplate(params.springxd_admin_env_sh_template)
  )

  File(format("{conf_dir}/springxd-container-env.sh"),
    owner=params.springxd_user,
    content=InlineTemplate(params.springxd_container_env_sh_template)
  )

