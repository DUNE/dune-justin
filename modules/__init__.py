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
__all__ = [ 'justin_version' ]

import os
import io
import re
import sys
import time
import json
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

# Constantas
MonteCarloRseID = 1

justinRunDir    = '/var/run/justin'

# From justin.conf etc
mysqlUsername   = None
mysqlPassword   = None
mysqlHostname   = None
mysqlDbName     = None

cilogonClientID     = None
cilogonSecret       = None
wlcgGroups          = None
justinAdmins        = None
rucioProductionUser = None
agentUsername       = None
proDev              = None
htcondorSchedds     = None

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

# Timeout is when to update cached ranks; Stale is when to remove from Finder
sitesRankCacheTimeout = 300
sitesRankCacheStale   = 3600

jobStatesTerminal = [ 'finished', 'notused', 'aborted', 'stalled', 
                      'jobscript_error', 'outputting_failed' ]

jobStatesAll = [ 'submitted', 'started', 'processing', 'outputting' ] \
               + jobStatesTerminal

jobStallSeconds = 3660

defaultScopeName = 'usertests'

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

awtWorkflowID = 1
awtFileID     = 1

maxAllocations = 6

# Catch all events
event_UNDEFINED = 0

# Workflow Allocator events
# DEPRECATED: DO NOT USE NOW!!!
#old_event_HEARTBEAT_RECEIVED  = 100
#old_event_GET_STAGE_RECEIVED  = 101
#old_event_STAGE_ALLOCATED     = 102
#old_event_FILE_ALLOCATED      = 103
#old_event_OUTPUTTING_RECEIVED = 104
#old_event_CONFIRM_RECEIVED    = 105

# Finder events
#event_FILE_ADDED                = 201
event_REPLICA_ADDED             = 202
event_REPLICA_STAGING_REQUESTED = 203
event_REPLICA_STAGING_DONE      = 204
event_REPLICA_STAGING_CANCELLED = 205

# Job events
event_JOB_SUBMITTED		= 301
event_JOB_STARTED		= 302
event_JOB_PROCESSING		= 303
event_JOB_OUTPUTTING		= 304
event_JOB_FINISHED		= 305
event_JOB_NOTUSED		= 306
event_JOB_ABORTED		= 307
event_JOB_STALLED_HEARTBEAT	= 308
event_JOB_SCRIPT_ERROR          = 309
event_JOB_OUTPUTTING_FAILED     = 310
event_JOB_STALLED_HTCONDOR	= 311

# File events
event_FILE_ADDED                = 201
#event_FILE_ADDED                = 400
#event_FILE_ALLOCATED            = 103
event_FILE_ALLOCATED            = 401
event_FILE_ALLOCATED_RESET      = 402
event_FILE_SET_TO_FAILED        = 403
event_FILE_CREATED              = 404
event_FILE_OUTPUTTING_RESET     = 405
event_FILE_UPLOADED             = 406

# AWT events 
event_AWT_READ_OK               = 501
event_AWT_READ_FAIL             = 502
event_AWT_WRITE_OK              = 503
event_AWT_WRITE_FAIL            = 504

eventTypes = { 
 
 # Catch all events
 event_UNDEFINED       : ['UNDEFINED',       'Undefined'],

 # Workflow Allocator events (DEPRECATED)
# old_event_HEARTBEAT_RECEIVED : ['HEARTBEAT_RECEIVED', 
#                             'Heartbeat received by allocator'],
# old_event_GET_STAGE_RECEIVED : ['GET_STAGE_RECEIVED', 
#                             'get_stage received from job by allocator'],
# old_event_STAGE_ALLOCATED    : ['STAGE_ALLOCATED', 
#                             'Stage allocated to job'],
# old_event_FILE_ALLOCATED     : ['FILE_ALLOCATED',  
#                             'File allocated to job'],
# old_event_OUTPUTTING_RECEIVED : ['OUTPUTTING_RECEIVED',
#                             'Outputting state received from job by allocator'],
# old_event_CONFIRM_RECEIVED   : ['CONFIRM_RECEIVED',
#                             'Confirmation received from job by allocator'],

# SHOULD REPLACE WITH SOMETHING DYNAMIC USING exec() TO AVOID DUPLICATION
# OF NAMES?

 # Replica events
 event_REPLICA_ADDED             : ['REPLICA_ADDED',
                                    'Replica added for file by finder'],
 event_REPLICA_STAGING_REQUESTED : ['REPLICA_STAGING_REQUESTED',
                                    'Finder workflows replica staging'],
 event_REPLICA_STAGING_DONE      : ['REPLICA_STAGING_DONE',
                                    'Replica staging workflowed by finder done'],
 event_REPLICA_STAGING_CANCELLED : ['REPLICA_STAGING_CANCELLED',
                                    'Replica staging cancelled by finder'],

 # Job events               
 event_JOB_SUBMITTED    : ['JOB_SUBMITTED',
                           'Job submitted by factory'],
 event_JOB_STARTED      : ['JOB_STARTED',
                           'Job started running at site'],
 event_JOB_PROCESSING   : ['JOB_PROCESSING',
                           'Job began processing files'],
 event_JOB_OUTPUTTING   : ['JOB_OUTPUTTING',
                           'Job began outputting files to storage'],
 event_JOB_FINISHED     : ['JOB_FINISHED',
                           'Job finished'],
 event_JOB_NOTUSED      : ['JOB_NOTUSED',
                           'Job was not allocated a stage'],
 event_JOB_ABORTED      : ['JOB_ABORTED',
                           'Job aborted'],
 event_JOB_STALLED_HEARTBEAT : ['JOB_STALLED_HEARTBEAT',
                                'Job stalls with missing heartbeats'],
 event_JOB_SCRIPT_ERROR : ['JOB_SCRIPT_ERROR',
                           'Error raised by the jobscript'],
 event_JOB_OUTPUTTING_FAILED : ['JOB_OUTPUTTING_FAILED',
                                'Job outputting failed'],
 event_JOB_STALLED_HTCONDOR : ['JOB_STALLED_HTCONDOR',
                               'Job stalls as absent from HTCondor'],

 # File events
 event_FILE_ADDED            : ['FILE_ADDED',
                                'File added to first stage by finder'],
 event_FILE_ALLOCATED        : ['FILE_ALLOCATED',  
                                'File allocated to job'],
 event_FILE_ALLOCATED_RESET  : ['FILE_ALLOCATED_RESET',
                                'File set back to unallocated from allocated'],
 event_FILE_SET_TO_FAILED    : ['FILE_SET_TO_FAILED',
                                'Too many attempts to process file: failed'],
 event_FILE_CREATED          : ['FILE_CREATED',
                                'Output file created in job'],
 event_FILE_OUTPUTTING_RESET : ['FILE_OUTPUTTING_RESET',
                                'File set back to unallocated from outputting'],
 event_FILE_UPLOADED          : ['FILE_UPLOADED',
                                'Output file uploaded in job'],

 # AWT events
 event_AWT_READ_OK     : ['AWT_READ_OK',
                          'AWT read test succeeds'],
 event_AWT_READ_FAIL   : ['AWT_READ_FAIL',
                          'AWT read test fails'],
 event_AWT_WRITE_OK    : ['AWT_WRITE_OK',
                          'AWT write test succeeds'],
 event_AWT_WRITE_FAIL  : ['AWT_WRITE_FAIL',
                          'AWT write test fails']
             }

def readConf():
  global mysqlUsername, mysqlPassword, mysqlHostname, mysqlDbName, \
         cilogonClientID, cilogonSecret, agentUsername,  \
         proDev, wlcgGroups, rucioProductionUser, justinAdmins, \
         nonJustinFraction, htcondorSchedds

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
    mysqlHostname = 'justin-db-pro.dune.hep.ac.uk'

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
    rucioProductionUser = parser.get('users','rucio_production_user').strip()
  except:
    rucioProductionUser = 'dunepro'

  # Options for the [agents] section

  try:
    agentUsername = parser.get('agents','username').strip()
  except:
    agentUsername = 'dunejustin'

  try:
    proDev = parser.get('agents','pro_dev').strip()
  except:
    proDev = 'pro'

  try:
    nonJustinFraction = float(
                         parser.get('agents','non_justin_fraction').strip())
  except:
    nonJustinFraction = 0.5

  try:
    a = parser.get('htcondor','schedds').strip()
    htcondorSchedds = []
    for a in a.split():
      if not stringIsDomain(a):
        raise 
      htcondorSchedds.append(a.strip().lower())
  except:
    htcondorSchedds = [ 'justin-prod-sched01.dune.hep.ac.uk' ]

# Try to find the text of a jobscript from the Jobscripts Library 
# given a JSID
def lookupJobscript(jsid):
  if ':' not in jsid:
    return { 'error': 'Jobscript identifier must contain ":"' }

  (prefix,name) = jsid.split(':',1)

  if not prefix or not name:
    return { 'error': 'Both parts of the JSID must be given' }

  if not stringIsDomain(name):
    return { 'error': 'Invalid characters in jobscript name in JSID' }

  if '@' in prefix:
    # JSID is USER:NAME

    if not stringIsUsername(prefix):
      return { 'error': 'Invalid characters in user name in JSID' }

    query = ('SELECT jobscripts_library.description,'
             'authors_principals.principal_name AS authorname,'
             'created_time,jobscript,jobscript_id '
             'FROM jobscripts_library '
             'LEFT JOIN users AS authors '
             'ON jobscripts_library.author_id=authors.user_id '
             'LEFT JOIN principal_names AS authors_principals '
             'ON authors.main_pn_id=authors_principals.pn_id '
             'LEFT JOIN users AS jobscripts_users '
             'ON jobscripts_library.user_id=jobscripts_users.user_id '
             'LEFT JOIN principal_names AS users_principals '
             'ON jobscripts_users.main_pn_id=users_principals.pn_id '
             'WHERE users_principals.principal_name="%s" '
             'AND jobscript_name="%s"'
             % (prefix, name))
  else:
    # JSID is SCOPE:NAME

    if not stringIsDomain(prefix):
      return { 'error': 'Invalid characters in scope name in JSID' }

    query = ('SELECT jobscripts_library.description,'
             'authors_principals.principal_name AS authorname,'
             'created_time,jobscript,jobscript_id '
             'FROM jobscripts_library '
             'LEFT JOIN users AS authors '
             'ON jobscripts_library.author_id=authors.user_id '
             'LEFT JOIN principal_names AS authors_principals '
             'ON authors.main_pn_id=authors_principals.pn_id '
             'LEFT JOIN scopes '
             'ON jobscripts_library.scope_id=scopes.scope_id '
             'WHERE scope_name="%s" AND jobscript_name="%s"'
             % (prefix, name))
  try:
    jobscriptRow = select(query, justOne = True)
  except Exception as e:
    return { 'error': 'Query to justIN failed: ' + str(e) }

  if not jobscriptRow or not jobscriptRow['jobscript']:
    return { 'error': 'Jobscript %s not found' % jsid }   

  return { 'jobscript'    : jobscriptRow['jobscript'],
           'jobscript_id' : jobscriptRow['jobscript_id'],
           'description'  : jobscriptRow['description'],
           'authorname'   : jobscriptRow['authorname'],
           'created_time' : jobscriptRow['created_time'],           
           'error'        : None }


def stringIsJobsubID(s):
  return re.search('[^A-Za-z0-9_.@-]', s) is None

def stringIsUsername(s):
  return re.search('[^a-z0-9_.@-]', s) is None

def stringIsFilePattern(s):
  return re.search('[^*A-Za-z0-9_.-]', s) is None

def stringIsURL(s):
  return re.search('[^/A-Za-z0-9_.:-]', s) is None

def stringIsDID(s):
  return re.search('[^a-z0-9_.:-]', s) is None

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
             siteID = 0,
             siteName = None,
             rseID = 0,
             rseName = None,
             seconds = 0.0):

  if siteName:
    siteExpr = ('(SELECT site_id FROM sites WHERE sites.site_name="%s")' 
                % siteName)
  else:
    siteExpr = str(siteID)

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
             'site_id=%s,'
             'rse_id=%s,'
             'seconds=%.3f,'
             'event_time=NOW()' %
             (eventTypeID,
              workflowID,
              stageID,
              fileID,
              justinJobID,
              siteExpr,
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
        # fetchone() returns None of no matching rows were found
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
