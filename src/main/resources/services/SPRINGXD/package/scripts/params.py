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
from resource_management.libraries.functions.version import compare_versions
from resource_management import *
from compat import get_full_stack_version
import status_params

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_version = str(config['hostLevelParams']['stack_version'])
stack_version = get_full_stack_version(stack_version)
stack_name = str(config['hostLevelParams']['stack_name']).lower()
conf_dir = "/etc/springxd/conf"

# common configs
log_dir = config['configurations']['springxd-admin-env']['springxd_log_dir']
user_group = config['configurations']['cluster-env']['user_group']
pid_dir = status_params.pid_dir
java64_home = config['hostLevelParams']['java_home']
jps_binary = format("{java64_home}/bin/jps")

# xd configs
xd_transport = config['configurations']['springxd-site']['xd.transport'].strip()
hsql_port = config['configurations']['springxd-site']['hsql.server.port']
admin_port = config['configurations']['springxd-site']['server.port']
spring_redis_port = config['configurations']['springxd-site']['spring.redis.port']
spring_redis_host = config['configurations']['springxd-site']['spring.redis.host'].strip()
xd_messagebus_kafka_brokers = config['configurations']['springxd-site']['xd.messagebus.kafka.brokers'].strip()
spring_rabbitmq_addresses = config['configurations']['springxd-site']['spring.rabbitmq.addresses'].strip()

if stack_name == 'phd':
  hadoop_distro = "phd30"
elif stack_name == 'hdp':
  hadoop_distro = "hdp22"
else:
  hadoop_distro = None

# xd env configs
springxd_admin_env_sh_template = config['configurations']['springxd-admin-env']['content']
springxd_container_env_sh_template = config['configurations']['springxd-container-env']['content']
springxd_user = config['configurations']['springxd-admin-env']['springxd_user']
springxd_hdfs_user_dir = format("/user/{springxd_user}")

# cluster configs
kafka_port = config['configurations']['kafka-broker']['port']
zk_port = config['configurations']['zoo.cfg']['clientPort']
fs_defaultfs = config['configurations']['core-site']['fs.defaultFS']
yarn_rm_address = config['configurations']['yarn-site']['yarn.resourcemanager.address']
yarn_rm_address_host = yarn_rm_address.split(':')[0]
yarn_rm_address_port = yarn_rm_address.split(':')[1]
yarn_rm_scheduler_address = config['configurations']['yarn-site']['yarn.resourcemanager.scheduler.address']
job_history_address = config['configurations']['mapred-site']['mapreduce.jobhistory.address']
yarn_app_classpath = config['configurations']['yarn-site']['yarn.application.classpath']
yarn_app_classpath = yarn_app_classpath.replace('${hdp.version}', stack_version)
yarn_app_classpath = yarn_app_classpath.replace('${stack.version}', stack_version)
yarn_app_classpath = yarn_app_classpath.replace('${stack.name}', stack_name)
mr_app_classpath = config['configurations']['mapred-site']['mapreduce.application.classpath']
mr_app_classpath = mr_app_classpath.replace('${hdp.version}', stack_version)
mr_app_classpath = mr_app_classpath.replace('${stack.version}', stack_version)
mr_app_classpath = mr_app_classpath.replace('${stack.name}', stack_name)

# collect what is actually installed
if 'kafka_broker_hosts' in config['clusterHostInfo'] and \
    len(config['clusterHostInfo']['kafka_broker_hosts'])>0:
  kafka_installed = True
  kafka_server = config['clusterHostInfo']['kafka_broker_hosts'][0]
else:
  kafka_installed = False

if 'zookeeper_hosts' in config['clusterHostInfo'] and \
    len(config['clusterHostInfo']['zookeeper_hosts'])>0:
  zk_installed = True
  zk_server = config['clusterHostInfo']['zookeeper_hosts'][0]
else:
  zk_installed = False

if 'springxdhsql_hosts' in config['clusterHostInfo'] and \
    len(config['clusterHostInfo']['springxdhsql_hosts'])>0:
  hsql_installed = True
  hsql_server = config['clusterHostInfo']['springxdhsql_hosts'][0]
else:
  hsql_installed = False

if 'springxdadmin_hosts' in config['clusterHostInfo'] and \
    len(config['clusterHostInfo']['springxdadmin_hosts'])>0:
  xd_admin_installed = True
  xd_admin_server = config['clusterHostInfo']['springxdadmin_hosts'][0]
else:
  xd_admin_installed = False

redis_installed = False
rabbitmq_installed = False

# tweak actual message bus settings
# we default to kafka if its installed and transport is not set
if len(xd_messagebus_kafka_brokers)>0:
  xd_transport = "kafka"
elif len(xd_transport)<1 and kafka_installed:
  xd_transport = "kafka"
  xd_messagebus_kafka_brokers = format("{kafka_server}:{kafka_port}")
elif len(spring_rabbitmq_addresses)>1:
  rabbitmq_installed = True
else:
  xd_transport = "redis"
  redis_installed = True

# for xd shell
xd_shell_hdfs_address = fs_defaultfs
xd_shell_admin_server_address = format("http://{xd_admin_server}:{admin_port}")

# needed for hdfs directory setup
hadoop_conf_dir = "/etc/hadoop/conf"
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
security_enabled = config['configurations']['cluster-env']['security_enabled']
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']
hdfs_principal_name = config['configurations']['hadoop-env']['hdfs_principal_name']
kinit_path_local = functions.get_kinit_path(["/usr/bin", "/usr/kerberos/bin", "/usr/sbin"])
hadoop_bin_dir = "/usr/hdp/current/hadoop-client/bin"

# for other sec
if security_enabled:
  nn_principal_name = config['configurations']['hdfs-site']['dfs.namenode.kerberos.principal']
  rm_principal_name = config['configurations']['yarn-site']['yarn.resourcemanager.principal']
  jhs_principal_name = config['configurations']['mapred-site']['mapreduce.jobhistory.principal']
  user_principal_name = config['configurations']['springxd-site']['spring.hadoop.security.userPrincipal']
  user_keytab = config['configurations']['springxd-site']['spring.hadoop.security.userKeytab']

import functools
HdfsDirectory = functools.partial(
  HdfsDirectory,
  conf_dir=hadoop_conf_dir,
  hdfs_user=hdfs_user,
  security_enabled = security_enabled,
  keytab = hdfs_user_keytab,
  kinit_path_local = kinit_path_local,
  bin_dir = hadoop_bin_dir
)

