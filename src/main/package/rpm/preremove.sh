#!/bin/bash

python <<EOT
import json, os, socket
import xml.etree.ElementTree as ET
from pprint import pprint

def updateRepoWithSpringXd(repoinfoxml):
  is_springxdrepo_set = None

  tree = ET.parse(repoinfoxml)
  root = tree.getroot()

  for os_tag in root.findall('.//os'):
    if os_tag.attrib['type'] == 'redhat6':
      for repo in os_tag.findall('.//repo'):
        for reponame in repo.findall('.//reponame'):
          if 'SPRINGXD-1.2-1' in reponame.text:
            is_springxdrepo_set = True
            os_tag.remove(repo)
  if is_springxdrepo_set == True:
    tree.write(repoinfoxml)

if os.path.exists('/var/lib/ambari-server/resources/stacks/PHD/3.0/role_command_order.json'):
  json_data=open('/var/lib/ambari-server/resources/stacks/PHD/3.0/role_command_order.json', 'r+')
  data = json.load(json_data)
  if data['general_deps'].has_key('SPRINGXD-INSTALL'):
    data['general_deps'].pop('SPRINGXD-INSTALL')
  if data['general_deps'].has_key('SPRINGXDADMIN-START'):
    data['general_deps'].pop('SPRINGXDADMIN-START')
  if data['general_deps'].has_key('SPRINGXDCONTAINER-START'):
    data['general_deps'].pop('SPRINGXDCONTAINER-START')
  json_data.seek(0)
  json_data.truncate()
  json.dump(data, json_data, indent=2)
  json_data.close()
elif os.path.exists('/var/lib/ambari-server/resources/stacks/HDP/2.2/role_command_order.json'):
  json_data=open('/var/lib/ambari-server/resources/stacks/HDP/2.2/role_command_order.json', 'r+')
  data = json.load(json_data)
  if data['general_deps'].has_key('SPRINGXD-INSTALL'):
    data['general_deps'].pop('SPRINGXD-INSTALL')
  if data['general_deps'].has_key('SPRINGXDADMIN-START'):
    data['general_deps'].pop('SPRINGXDADMIN-START')
  if data['general_deps'].has_key('SPRINGXDCONTAINER-START'):
    data['general_deps'].pop('SPRINGXDCONTAINER-START')
  json_data.seek(0)
  json_data.truncate()
  json.dump(data, json_data, indent=2)
  json_data.close()

if os.path.exists('/var/lib/ambari-server/resources/stacks/PHD/3.0/repos/repoinfo.xml'):
  updateRepoWithSpringXd('/var/lib/ambari-server/resources/stacks/PHD/3.0/repos/repoinfo.xml')
elif os.path.exists('/var/lib/ambari-server/resources/stacks/HDP/2.2/repos/repoinfo.xml'):
  updateRepoWithSpringXd('/var/lib/ambari-server/resources/stacks/HDP/2.2/repos/repoinfo.xml')

EOT

