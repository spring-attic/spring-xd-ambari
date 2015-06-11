#!/bin/bash

python <<EOT
import json, os, socket
import xml.etree.ElementTree as ET
from pprint import pprint

def updateRepoWithSpringXd(repoinfoxml):
  springxd_repo='Spring-XD-1.2'
  springxd_repo_str = '<repo><baseurl>http://repo.spring.io/yum-release/spring-xd/1.2</baseurl><repoid>' + springxd_repo + '</repoid><reponame>' + springxd_repo + '</reponame></repo>'
  is_springxdrepo_set = None

  tree = ET.parse(repoinfoxml)
  root = tree.getroot()

  for os_tag in root.findall('.//os'):
    if os_tag.attrib['type'] == 'redhat6' or os_tag.attrib['type'] == 'suse11':
      for reponame in os_tag.findall('.//reponame'):
        if 'SPRINGXD' in reponame.text:
          is_springxdrepo_set = True
      if is_springxdrepo_set is None:
        springxd_element = ET.fromstring(springxd_repo_str)
        os_tag.append(springxd_element)
  if is_springxdrepo_set is None:
    tree.write(repoinfoxml)

if os.path.exists('/var/lib/ambari-server/resources/stacks/PHD/3.0/role_command_order.json'):
  json_data=open('/var/lib/ambari-server/resources/stacks/PHD/3.0/role_command_order.json', 'r+')
  data = json.load(json_data)
  data['general_deps']['SPRINGXD-INSTALL'] = ['HDFS-INSTALL']
  data['general_deps']['SPRINGXDADMIN-START'] = ['SPRINGXDHSQL-START','ZOOKEEPER_SERVER-START','NODEMANAGER-START','RESOURCEMANAGER-START']
  data['general_deps']['SPRINGXDCONTAINER-START'] = ['SPRINGXDHSQL-START','ZOOKEEPER_SERVER-START','NODEMANAGER-START','RESOURCEMANAGER-START']
  json_data.seek(0)
  json.dump(data, json_data, indent=2)
  json_data.close()
elif os.path.exists('/var/lib/ambari-server/resources/stacks/HDP/2.2/role_command_order.json'):
  json_data=open('/var/lib/ambari-server/resources/stacks/HDP/2.2/role_command_order.json', 'r+')
  data = json.load(json_data)
  data['general_deps']['SPRINGXD-INSTALL'] = ['HDFS-INSTALL']
  data['general_deps']['SPRINGXDADMIN-START'] = ['SPRINGXDHSQL-START','ZOOKEEPER_SERVER-START','KAFKA_BROKER-START','NODEMANAGER-START','RESOURCEMANAGER-START']
  data['general_deps']['SPRINGXDCONTAINER-START'] = ['SPRINGXDHSQL-START','ZOOKEEPER_SERVER-START','KAFKA_BROKER-START','NODEMANAGER-START','RESOURCEMANAGER-START']
  json_data.seek(0)
  json.dump(data, json_data, indent=2)
  json_data.close() 

if os.path.exists('/var/lib/ambari-server/resources/stacks/PHD/3.0/repos/repoinfo.xml'):
  updateRepoWithSpringXd('/var/lib/ambari-server/resources/stacks/PHD/3.0/repos/repoinfo.xml')
elif os.path.exists('/var/lib/ambari-server/resources/stacks/HDP/2.2/repos/repoinfo.xml'):
  updateRepoWithSpringXd('/var/lib/ambari-server/resources/stacks/HDP/2.2/repos/repoinfo.xml')

EOT


