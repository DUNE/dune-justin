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

from justin.justin_version import *
from justin.events_list import *
__all__ = [ 'justin_version', 'events_list' ]

import os
import io
import re
import pwd
import sys
import time
import json
import socket
import random
import string
import tarfile
import configparser

#import MySQLdb

# WE NEED TO REMOVE OLD MySQLdb REFERENCES STILL!
import pymysql
pymysql.install_as_MySQLdb()
MySQLdb=pymysql

import MySQLdb.constants.ER

# Globals
jobsProductionProxyString = None
jobsProductionProxyFile   = '/tmp/justin-jobs-production.proxy.pem'

jobsNoRolesProxyString = None
jobsNoRolesProxyFile   = '/tmp/justin-jobs-no-roles.proxy.pem'

# Constants
MonteCarloRseID     = 1
justinRunDir        = '/var/run/justin'
rucioProductionUser = 'dunepro'

# From justin.conf etc
mysqlUsername   = None
mysqlPassword   = None
mysqlHostname   = None
mysqlDbName     = None

cilogonClientID     = None
cilogonSecret       = None
wlcgGroups          = None
justinAdmins        = None
justinJobsUser      = None
agentUsername       = None
proDev              = None
htcondorSchedds     = None
keepWrapperFiles    = None
extraEntries        = None

metacatAuthServerURL    = None
metacatServerInputsURL  = None
metacatServerOutputsURL = None

awtWorkflowID = None

bannerMessage = None

rcdsServers = None

## Global database connection
conn = None
cur  = None

wsgiCallsCount = 0

rseAvailabilityDelete = 1
rseAvailabilityWrite  = 2
rseAvailabilityRead   = 4

#rseDisksExpression = 'istape=False\\decommissioned=True'
rseDisksExpression = 'DUNE_US_FNAL_DISK_STAGE'

htcondorIDLE                = 1
htcondorRUNNING             = 2
htcondorREMOVED             = 3
htcondorCOMPLETED           = 4
htcondorHELD                = 5
htcondorTRANSFERRING_OUTPUT = 6
htcondorSUSPENDED           = 7

cilogonScopes       = ('openid profile org.cilogon.userinfo '
                       'wlcg.capabilityset:/duneana wlcg.groups:/dune '
                       'wlcg.groups:/dune/production')

# Note that this assumes we are using UTC since we assume elsewhere this
# will convert from this MySQL date to 0 in Unix seconds
# Also Unicode date strings coming out of MySQL may not match plain strings 
# like this unless converted with str()
unixEpoch = '1970-01-01 00:00:00'

unseenSitesExpireDays = 7

# Fraction of all GlideIns/pilots that assign rank 101 to non-justIN jobs
# justIN jobs get 1-100. If non-justIN does not get 101, it gets 0.
# Set in configuration, default 0.5
nonJustinFraction = None

# When rucio ping takes this many seconds, assume Rucio is overloaded
# and back off job submissions and jobscript starts
overloadRucioSeconds = None

# Timeout is when to update cached ranks; Stale is when to remove from Finder
sitesRankCacheTimeout = 300
sitesRankCacheStale   = 3600

workflowStates = [ 'draft','submitted','approved','running',
                   'paused','checking','finished','deleted']

jobStatesTerminal = [ 'finished', 'notused', 'aborted', 'stalled', 
                      'jobscript_error', 'outputting_failed', 'none_processed' ]

jobStatesAll = [ 'submitted', 'started', 'processing', 'outputting' ] \
               + jobStatesTerminal

jobStallSeconds = 3660
maxFilesPerJob     = 20

filesPerNumberedDestination = 1000

defaultScopeName = 'usertests'

wrapperJobImage       = None
jobscriptImageSuffix  = None
jobscriptImagePrefix  = None 
jobscriptImageVersion = None 

rseCountriesRegions = { 
                        'BR'  : 'South_America',
                        'CA'  : 'North_America',
                        'CERN': 'Europe',
                        'CH'  : 'Europe',
                        'CZ'  : 'Europe',
                        'DE'  : 'Europe',
                        'ES'  : 'Europe',
                        'FR'  : 'Europe',
                        'IN'  : 'South_Asia',
                        'IT'  : 'Europe',
                        'NL'  : 'Europe',
                        'RU'  : 'Europe',
                        'UK'  : 'Europe',
                        'US'  : 'North_America'
                      }

# Catch all events
event_UNDEFINED = 0
eventTypes = { event_UNDEFINED : ['UNDEFINED', 'Undefined'] }

# Go through eventsList defining variables and adding to dictionary
# So we can say justin.event_AWT_READ_OK etc in the code elsewhere
for (eventLabel, eventID, eventText) in eventsList:
  exec('event_%s=%d' % (eventLabel, eventID))
  exec('eventTypes[event_%s]=["%s","%s"]' % (eventLabel,eventLabel,eventText))


def readConf():
  global mysqlUsername, mysqlPassword, mysqlHostname, mysqlDbName, \
         cilogonClientID, cilogonSecret, agentUsername,  \
         proDev, wlcgGroups, justinJobsUser, justinAdmins, \
         nonJustinFraction, htcondorSchedds, metacatAuthServerURL, \
         metacatServerInputsURL, metacatServerOutputsURL, \
         jobscriptImagePrefix, jobscriptImageSuffix, jobscriptImageVersion, \
         wrapperJobImage, overloadRucioSeconds, \
         awtWorkflowID, bannerMessage, rcdsServers, keepWrapperFiles, \
         extraEntries

  parser = configparser.RawConfigParser()

  # Look for configuration files in /etc/justin.d
  try:
    confFiles = os.listdir('/etc/justin.d')
  except:
    pass 
  else:
    for oneFile in sorted(confFiles):
      if oneFile[-5:] == '.conf':
        parser.read('/etc/justin.d/' + oneFile)

  # Standalone configuration file, read after justin.d 
  # in case of manual overrides
  parser.read('/etc/justin.conf')

  # Options for the [database] section

  try:
    mysqlUsername = parser.get('database','username').strip()
  except:
    mysqlUsername = 'dunejustin'

  try:
    mysqlHostname = parser.get('database','hostname').strip()
  except:
    # In case of misconfiguration, the default is dev
    mysqlHostname = 'justin-db-dev.dune.hep.ac.uk'

  try:
    mysqlPassword = parser.get('database','password').strip()
  except:
     mysqlPassword = None

  try:
    mysqlDbName = parser.get('database','db').strip()
  except:
    mysqlDbName = 'justindb'
 
  # Options for the [users] section

  try:
    cilogonClientID = parser.get('users','cilogon_client_id').strip()
  except:
    cilogonClientID = None

  try:
    cilogonSecret = parser.get('users','cilogon_secret').strip()
  except:
    cilogonSecret = None

  try:
    g = parser.get('users','wlcg_groups').strip()
    wlcgGroups = []
    for w in g.split():
      if not stringNoQuotes(w):
        raise 
      wlcgGroups.append(w.strip().lower())
  except:
    wlcgGroups = []

  try:
    a = parser.get('users','justin_admins').strip()
    justinAdmins = []
    for a in a.split():
      if not stringIsUsername(a):
        raise 
      justinAdmins.append(a.strip().lower())
  except:
    justinAdmins = []

  try:
    justinJobsUser = parser.get('users','justin_jobs_user').strip()
  except:
    justinJobsUser = 'dunepro'

  # Options for the [agents] section

  try:
    agentUsername = parser.get('agents','username').strip()
  except:
    agentUsername = 'dunejustin'

  try:
    proDev = parser.get('agents','pro_dev').strip()
  except:
    # In case of misconfiguration, the default is dev
    proDev = 'dev'

  try:
    overloadRucioMilliseconds = int(
                 parser.get('agents','overload_rucio_milliseconds').strip())
  except:
    overloadRucioMilliseconds = 100000

  try:
    nonJustinFraction = float(
                         parser.get('agents','non_justin_fraction').strip())
  except:
    nonJustinFraction = 0.5

  try:
    wrapperJobImage = parser.get('agents',
                                 'wrapper_job_image').strip()
  except:
    wrapperJobImage = \
      '/cvmfs/singularity.opensciencegrid.org/fermilab/fnal-wn-sl7:latest'

  # Default apptainer image in cvmfs is 'prefix/suffix:latest'
  try:
    jobscriptImagePrefix = parser.get('agents',
                                      'jobscript_image_prefix').strip()
  except:
    jobscriptImagePrefix = '/cvmfs/singularity.opensciencegrid.org/fermilab'

  try:
    jobscriptImageSuffix = parser.get('agents',
                                      'jobscript_image_suffix').strip()
  except:
    jobscriptImageSuffix = 'fnal-wn-sl7'

  try:
    jobscriptImageVersion = parser.get('agents',
                                       'jobscript_image_version').strip()
  except:
    jobscriptImageVersion = 'latest'

  try:
    awtWorkflowID = int(parser.get('agents','awt_workflow_id').strip())
  except:
    awtWorkflowID = 1

  try:
    a = parser.get('htcondor','schedds').strip()
    htcondorSchedds = []
    for a in a.split():
      if not stringIsDomain(a):
        raise 
      htcondorSchedds.append(a.strip().lower())
  except:
    htcondorSchedds = [ 'justin-prod-sched01.dune.hep.ac.uk',
                        'justin-prod-sched02.dune.hep.ac.uk' ]
  try:
    keepWrapperFiles = bool(parser.get('htcondor','keep_wrapper_files').strip())
  except:
    keepWrapperFiles = False

  try:
    extraEntries = parser.items('extra_entries')
  except:
    extraEntries = []
  
  try:
    metacatAuthServerURL = parser.get('metacat','auth_server_url').strip()
  except:
    metacatAuthServerURL = 'https://metacat.fnal.gov:8143/auth/dune'

  try:
    metacatServerInputsURL =parser.get('metacat','server_inputs_url').strip()
  except:
    metacatServerInputsURL ='https://metacat.fnal.gov:9443/dune_meta_prod/app'

  try:
    metacatServerOutputsURL =parser.get('metacat','server_outputs_url').strip()
  except:
    metacatServerOutputsURL ='https://metacat.fnal.gov:9443/dune_meta_prod/app'

  # Dashboard
  try:
    bannerMessage = parser.get('dashboard', 'banner_message').strip()
  except:
    bannerMessage = ''

  # FNAL Agent
  try:
    rcdsServers = parser.get('fnal_agent', 'rcds_servers').strip().split()
  except:
    rcdsServers = ['rcds01.fnal.gov']

def logLine(text):
  sys.stdout.write(time.strftime('%b %d %H:%M:%S [') + str(os.getpid())
                   + ']: ' + text + '\n')
  sys.stdout.flush()

def agentMainLoop(agentName, oneCycle, sleepSeconds, maxCycleSeconds):

  global conn, cur

  os.chdir("/")
  os.umask(0)

  try:
    os.makedirs(justinRunDir + '/last-updates',
                stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | 
                stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
  except:
    pass
        
  try:
    f = open('%s/%s.pid' % (justinRunDir, agentName), 'w')
    f.write(str(os.getpid()) + '\n')
    f.close()
  except:
    print('Failed to create %s/%s.pid - exiting'
           % (justinRunDir, agentName))
    sys.exit(1)

  # Close stdin now
  si = open('/dev/null', 'r')
  os.dup2(si.fileno(), sys.stdin.fileno())

  while True:

    # Ensure /var/log/justin directory exists
    try:
      os.makedirs('/var/log/justin', 
                  stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP
                  |stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
    except:
      pass

    # Close and reopen stdout->log file, in case of logrotate
    try:
      close(so)
    except:
      pass

    so = open('/var/log/justin/%s' % agentName, 'a+')
    os.dup2(so.fileno(), sys.stdout.fileno())

    # Close and reopen stderr->log file, in case of logrotate
    try:
      close(se)
    except:
      pass
          
    se = open('/var/log/justin/%s' % agentName, 'a+')
    os.dup2(se.fileno(), sys.stderr.fileno())

    try:
      pf = open('%s/%s.pid' % (justinRunDir, agentName), 'r')
      pid = int(pf.read().strip())
      pf.close()

      if pid != os.getpid():
        print('new %s/%s.pid - exiting' % (justinRunDir, agentName))
        break

    except:
      print('no %s/%s.pid - exiting' % (justinRunDir, agentName))
      break

    # Fork a subprocess to run each cycle
    cyclePid = os.fork()

    if cyclePid == 0:
      logLine('=============== Start cycle ===============')
          
      readConf()
          
      try:
        conn = MySQLdb.connect(
                         host   = socket.gethostbyname(mysqlHostname),
                         user   = mysqlUsername,
                         passwd = mysqlPassword,
                         db     = mysqlDbName)
        conn.autocommit(False)
        cur = conn.cursor(MySQLdb.cursors.DictCursor)
      except Exception as e:
        logLine('Failed to create database connection (' + 
                    str(e) + ') - skipping cycle')
      else:
        try:
          p = pwd.getpwnam(agentUsername)
          os.chown(justinRunDir + '/last-updates', p[2], p[3])
          os.setgid(p[3])
          os.setuid(p[2])
          oneCycle()
        except Exception as e:
          print('Cycle fails with exception ' + str(e))

        conn.close()

      logLine('================ End cycle ================')
      # The subprocess is only used for this one cycle
      sys.exit(0)

    for count in range(0, maxCycleSeconds + 60, 60):
      if pidIsActive(cyclePid):
        time.sleep(60)
      else:
        break

    if pidIsActive(cyclePid):
      # subprocess still running despite reaching maxCycleSeconds so kill it
      print('PID %d is still running after %d seconds - kill it' 
            % (cyclePid, maxCycleSeconds))
      try:
        os.kill(cyclePid)
      except Exception:
        logLine('Kill of %d fails with: %s' % (cyclePid, str(e)))
   
      try:
        # Clear zombie state subprocess by reading outcome
        os.waitpid(cyclePid, 0)
      except:
        pass

    # wait the allotted time between cycles
    time.sleep(sleepSeconds)

  sys.exit(0) # if we break out of the while loop then we exit

def stringIsJobsubID(s):
  return re.search('[^A-Za-z0-9_.@-]', s) is None

def stringIsUsername(s):
  return re.search('[^a-z0-9_.@-]', s) is None

# What characters are valid? Same as File for now
def stringIsScope(s):
  return re.search('[^A-Za-z0-9_.-]', s) is None

def stringIsFile(s):
  return re.search('[^A-Za-z0-9_.-]', s) is None

def stringIsFilePattern(s):
  return re.search('[^*A-Za-z0-9_.-]', s) is None

def stringIsURL(s):
  return re.search('[^/A-Za-z0-9_.:-]', s) is None

def stringIsDID(s):
  return re.search('[^A-Za-z0-9_.:-]', s) is None

# RSE Expression
def stringIsExpression(s):
  return re.search('[^A-Za-z0-9_&=|()\<> -]', s) is None

def stringIsDomain(s):
  return re.search('[^A-Za-z0-9.-]', s) is None

def stringIsSite(s):
  return re.search('[^A-Za-z0-9_-]', s) is None

def stringIsEnvName(s):
  return re.search('[^A-Za-z0-9_]', s) is None

def stringNoQuotes(s):
  return re.search('["`\']', s) is None

# Use os.path.expandvars() to replace environment variables from dictionary envs
def expandEnvVars(s, envs):
  savedEnviron = dict(os.environ)
  os.environ.clear()

  try:
    os.environ.update(envs)
    expandedString = os.path.expandvars(s)
  except:
    expandedString = s
  finally:
    os.environ.clear()
    os.environ.update(savedEnviron)

  return expandedString

# Log an event to the database, returning an error message or None if no
# errors. You must ensure events are committed along with anything else
# you are writing to the database!!!
def logEvent(eventTypeID = event_UNDEFINED,
             workflowID = 0,
             stageID = 0,
             fileID = 0,
             justinJobID = 0,
             jobscriptExit = 0,
             siteID = 0,
             siteName = None,
             entryID = 0,
             entryName = None,
             rseID = 0,
             rseName = None,
             seconds = 0.0):

  if siteName:
    siteExpr = ('(SELECT site_id FROM sites WHERE sites.site_name="%s")' 
                % siteName)
  else:
    siteExpr = str(siteID)

  if entryName:
    entryExpr = ('(SELECT entry_id FROM entries WHERE entries.entry_name="%s")' 
                % entryName)
  else:
    entryExpr = str(entryID)

  if rseName:
    rseExpr = ('(SELECT rse_id FROM storages WHERE storages.rse_name="%s")' 
                % rseName)  
  else:
    rseExpr = str(rseID)

  try:
    query = ('INSERT INTO events SET '
             'event_type_id=%d,'
             'workflow_id=%d,'
             'stage_id=%d,'
             'file_id=%d,'
             'justin_job_id=%d,'
             'jobscript_exit=%d,'
             'site_id=%s,'
             'entry_id=%s,'
             'rse_id=%s,'
             'seconds=%.3f,'
             'event_time=NOW()' %
             (eventTypeID,
              workflowID,
              stageID,
              fileID,
              justinJobID,
              jobscriptExit,
              siteExpr,
              entryExpr,
              rseExpr,
              seconds))

    cur.execute(query)
    return None
  except Exception as e:
    return 'Error logging event: ' + str(e)

def select(query, justOne = False, tries = 10, showQuery = False):

  if showQuery:
    print('Query: ' + str(query), file=sys.stderr)

  for tryNumber in range(1, tries + 1):

    try:
      cur.execute(query)
 
    except MySQLdb.OperationalError as e:
      # We try again iff a deadlock error
      if ( (e.args[0] == MySQLdb.constants.ER.LOCK_DEADLOCK or 
            e.args[0] == MySQLdb.constants.ER.LOCK_WAIT_TIMEOUT) and
           tryNumber < tries ):
        print('Lock error but will retry (%d/%d): %s:' % 
              (tryNumber, tries, str(e)), file=sys.stderr)
        time.sleep(3 * random.random() * tryNumber)
        continue
   
      # Otherwise we re-raise the same exception
      raise
      
    else:
      # Success! Return the results!
      if justOne:
        # fetchone() returns None of no matching rows were found
        return cur.fetchone()
      else:
        return cur.fetchall()

def insertUpdate(query, tries = 10):

  for tryNumber in range(1, tries + 1):

    try:
      cur.execute(query)
 
    except MySQLdb.OperationalError as e:
      # We try again iff a deadlock error
      if ( (e.args[0] == MySQLdb.constants.ER.LOCK_DEADLOCK or
            e.args[0] == MySQLdb.constants.ER.LOCK_WAIT_TIMEOUT) and
           tryNumber < tries ):
        print('Lock error but will retry (%d/%d): %s' % 
              (tryNumber, tries, str(e)), file=sys.stderr)
        time.sleep(3 * random.random() * tryNumber)
        continue
   
      # Otherwise we re-raise the same exception
      raise
      
    else:
      return cur.lastrowid

def update(query, tries = 10):

  for tryNumber in range(1, tries + 1):

    try:
      changed = cur.execute(query)
 
    except MySQLdb.OperationalError as e:
      # We try again iff a deadlock error
      if ( (e.args[0] == MySQLdb.constants.ER.LOCK_DEADLOCK or
            e.args[0] == MySQLdb.constants.ER.LOCK_WAIT_TIMEOUT) and
           tryNumber < tries ):
        print('Lock error but will retry (%d/%d): %s' % 
              (tryNumber, tries, str(e)), file=sys.stderr)
        time.sleep(3 * random.random() * tryNumber)
        continue
   
      # Otherwise we re-raise the same exception
      raise
      
    else:
      return changed

# Temporary function to fix PFNs from Rucio that have faulty URLs
def fixPfn(pfn):

  for (old, new) in \
     [('.cern.ch/eos/',          '.cern.ch//eos/'          ),
      ('.in2p3.fr:1097/xrootd/', '.in2p3.fr:1097//xrootd/' ),
      ('.bnl.gov:1094/pnfs/',    '.bnl.gov:1094//pnfs/'    ),
      ('.bnl.gov:1096/pnfs/',    '.bnl.gov:1096//pnfs/'    ),
      ('.lancs.ac.uk/dpm/',      '.lancs.ac.uk//dpm/'      ),
      ('.liv.ac.uk/dune/',       '.liv.ac.uk//dune/'       ),
      ('.manchester.ac.uk/dune/','.manchester.ac.uk//dune/'),
      ('.qmul.ac.uk:1094/dune/', 'qmul.ac.uk:1094//dune/'  )
     ]:
    pfn = pfn.replace(old, new)
    
  return pfn

def checkProxyStrings():
  global jobsNoRolesProxyString, jobsProductionProxyString
  
  try:
    with open(jobsNoRolesProxyFile, 'rb') as f:
      jobsNoRolesProxyString = f.read()
  except Exception as e:
    print('Failed loading X.509 proxy from %s : %s'
          % (jobsNoRolesProxyFile, str(e)), file=sys.stderr)

  try:
    with open(jobsProductionProxyFile, 'rb') as f:
      jobsProductionProxyString = f.read()
  except Exception as e:
    print('Failed loading X.509 proxy from %s : %s'
          % (jobsProductionProxyFile, str(e)), file=sys.stderr)


# Check if a process is still active
# Linux specific but avoids installing psutil
def pidIsActive(pid):

  try:
    statList = open('/proc/%d/stat' % pid).read().split()
  except:
    return False

  if statList[2] in ['R', 'S', 'D']:
    return True
    
  return False


# Return the Rucio ping milliseconds 
# Exceptions must be handled by the caller!
def pingRucioMilliseconds():

  pingClient = rucio.client.pingclient.PingClient()  
  startTime  = time.time()
  for i in range(0,3):
    pingDict = pingClient.ping()  
  endTime    = time.time()
  
  return int((endTime - startTime) * 333.333)
