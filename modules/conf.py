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

    
