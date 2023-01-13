#
# Copyright 2013-23, Andrew McNab for the University of Manchester
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
#

import configparser

# Constants
MonteCarloRseID = 1

wfsLibDir     = '/var/lib/wfs'
wfsLogDir     = '/var/log/wfs'
wfsRunDir     = '/var/run/wfs'

mysqlUsername = None
mysqlPassword = None
mysqlHostname = None
mysqlDbName   = None

def readConf():
  global mysqlUsername, mysqlPassword, mysqlHostname, mysqlDbName

  parser = configparser.RawConfigParser()

  # Look for configuration files in /etc/wfs.d
  try:
    confFiles = os.listdir('/etc/wfs.d')
  except:
    pass 
  else:
    for oneFile in sorted(confFiles):
      if oneFile[-5:] == '.conf':
        parser.read('/etc/wfs.d/' + oneFile)

  # Standalone configuration file, read after wfs.d in case of manual overrides
  parser.read('/etc/wfs.conf')

  # Options for the [shared] section

  try:
    f = open(wfsLibDir + '/VERSION', 'r')
    wfsVersion = f.readline().split('=',1)[1].strip()
    f.close()
  except:
    wfsVersion = '00.00.00'

  # Options for the [database section]

  try:
    mysqlUsername = parser.get('database','username').strip()
  except:
    mysqlUsername = 'root'

  try:
    mysqlPassword = parser.get('database','password').strip()
  except:
    mysqlPassword = None

  try:
    mysqlHostname = parser.get('database','hostname').strip()
  except:
    mysqlHostname = 'localhost'

  try:
    mysqlDbName = parser.get('database','db').strip()
  except:
    mysqlDbName = 'wfdb'

    
