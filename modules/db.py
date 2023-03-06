#
# justIN database globals and functions
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


## Global database connection
conn = None
cur  = None

import re
import sys
import time
import random
import MySQLdb
import MySQLdb.constants.ER

wsgiCallsCount = 0

rseAvailabilityDelete = 1
rseAvailabilityWrite  = 2
rseAvailabilityRead   = 4

unixEpoch = '1970-01-01 00:00:00'

jobStatesTerminal = [ 'finished', 'notused', 'aborted', 'stalled', 
                      'jobscript_error', 'outputting_failed' ]

jobStatesAll = [ 'submitted', 'started', 'processing', 'outputting' ] \
               + jobStatesTerminal

jobStallSeconds = 3660

awtRequestID = 1
awtFileID    = 1

maxAllocations = 6

### EVENT DEFINITIONS BELOW ARE NOW IN events.py !!!!!
# Catch all events
event_UNDEFINED = 0

# Workflow Allocator events
event_HEARTBEAT_RECEIVED  = 100
event_GET_STAGE_RECEIVED  = 101
event_STAGE_ALLOCATED     = 102
event_FILE_ALLOCATED      = 103
event_OUTPUTTING_RECEIVED = 104
event_CONFIRM_RECEIVED    = 105

# Finder events
event_FILE_ADDED                = 201
event_REPLICA_ADDED             = 202
event_REPLICA_STAGING_REQUESTED = 203
event_REPLICA_STAGING_DONE      = 204
event_REPLICA_STAGING_CANCELLED = 205
event_REQUEST_FINISHED          = 206

# Job events
event_JOB_SUBMITTED		= 301
event_JOB_STARTED		= 302
event_JOB_PROCESSING		= 303
event_JOB_OUTPUTTING		= 304
event_JOB_FINISHED		= 305
event_JOB_NOTUSED		= 306
event_JOB_ABORTED		= 307
event_JOB_STALLED		= 308
event_JOB_SCRIPT_ERROR          = 309

# File events
#event_FILE_ALLOCATED           = 401
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

 # Workflow Allocator events
 event_HEARTBEAT_RECEIVED : ['HEARTBEAT_RECEIVED', 
                             'Heartbeat received by allocator'],
 event_GET_STAGE_RECEIVED : ['GET_STAGE_RECEIVED', 
                             'get_stage received from job by allocator'],
 event_STAGE_ALLOCATED    : ['STAGE_ALLOCATED', 
                             'Stage allocated to job'],
 event_FILE_ALLOCATED     : ['FILE_ALLOCATED',  
                             'File allocated to job'],
 event_OUTPUTTING_RECEIVED : ['OUTPUTTING_RECEIVED',
                             'Outputting state received from job by allocator'],
 event_CONFIRM_RECEIVED   : ['CONFIRM_RECEIVED',
                             'Confirmation received from job by allocator'],

 # Finder events
 event_FILE_ADDED                : ['FILE_ADDED',
                                    'File added to first stage by finder'],
 event_REPLICA_ADDED             : ['REPLICA_ADDED',
                                    'Replica added for file by finder'],
 event_REPLICA_STAGING_REQUESTED : ['REPLICA_STAGING_REQUESTED',
                                    'Finder requests replica staging'],
 event_REPLICA_STAGING_DONE      : ['REPLICA_STAGING_DONE',
                                    'Replica staging requested by finder done'],
 event_REPLICA_STAGING_CANCELLED : ['REPLICA_STAGING_CANCELLED',
                                    'Replica staging cancelled by finder'],
 event_REQUEST_FINISHED          : ['REQUEST_FINISHED',
                                    'Finder identifies request as finished'],

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
 event_JOB_STALLED      : ['JOB_STALLED',
                           'Job identified as stalled by Finder'],
 event_JOB_SCRIPT_ERROR : ['JOB_SCRIPT_ERROR',
                           'Error raised by the jobscript'],

 # File events
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

# Log an event to the database, returning an error message or None if no
# errors. You must ensure events are committed along with anything else
# you are writing to the database!!!
def logEvent(eventTypeID = event_UNDEFINED,
             requestID = 0,
             stageID = 0,
             fileID = 0,
             justinJobID = 0,
             siteID = 0,
             siteName = None,
             rseID = 0,
             rseName = None):

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
             'request_id=%d,'
             'stage_id=%d,'
             'file_id=%d,'
             'justin_job_id=%d,'
             'site_id=%s,'
             'rse_id=%s,'
             'event_time=NOW()' %
             (eventTypeID,
              requestID,
              stageID,
              fileID,
              justinJobID,
              siteExpr,
              rseExpr))

    cur.execute(query)
    return None
  except Exception as e:
    return 'Error logging event: ' + str(e)

def select(query, justOne = False, tries = 10):

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
