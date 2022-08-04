import configparser

# Constants
MonteCarloRseID = 1

mysqlUsername = None
mysqlPassword = None
mysqlHostname = None
mysqlDbName   = None

def readConf():
  global mysqlUsername, mysqlPassword, mysqlHostname, mysqlDbName

  try:
    f = open('/var/lib/wfs/VERSION', 'r')
    wfsVersion = f.readline().split('=',1)[1].strip()
    f.close()
  except:
    pass
    
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

