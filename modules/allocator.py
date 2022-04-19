#!/usr/bin/python3
#
#  Workflow Allocator module
#
#  Andrew McNab, University of Manchester.
#  Copyright (c) 2013-22. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or
#  without modification, are permitted provided that the following
#  conditions are met:
#
#    o Redistributions of source code must retain the above
#      copyright notice, this list of conditions and the following
#      disclaimer. 
#    o Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials
#      provided with the distribution. 
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
#  CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#  INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
#  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
#  TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#  ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
#  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
#

import os
import io
import re
import sys
import time
import json
import uuid
import string
import tarfile
import MySQLdb

# wfs/conf.py must define these variables in a way that is both
# valid Python and valid Bash!
#
# mysqlUser='username'
# mysqlPassword='PAsSWoRd'
#
import wfs

allocatorName = None

# Return information about the job from tnhe jobsubID
def makeJobDict(jobsubID, cookie = None):

  # Find the job info and the stage's any_location flag
  try:
    query = ('SELECT '
             'jobs.slot_size_id,'
             'jobs.allocation_state,'
             'jobs.cookie,'
             'stages.any_location,'
             'jobs.request_id,'
             'jobs.stage_id,'
             'jobs.wfs_job_id, '
             'jobs.site_id '
             'FROM jobs '
             'LEFT JOIN stages ON jobs.stage_id=stages.stage_id '
             'WHERE jobs.jobsub_id="' + jobsubID + '"')

    wfs.db.cur.execute(query)
    job = wfs.db.cur.fetchone()
  except:
    return { "error_message": "Failed to find job from jobsubID" }

  if job['allocation_state'] != 'submitted' and \
     (cookie is None or job['cookie'] != cookie):
    return { "error_message": "Cookie mismatch" }

  return { "error_message"    : None,
           "request_id"       : job['request_id'],
           "stage_id"         : job['stage_id'],
           "site_id"          : job['site_id'],
           "wfs_job_id"       : job['wfs_job_id'],
           "allocation_state" : job['allocation_state'],
           "slot_size_id"     : job['slot_size_id'],
           "any_location"     : job['any_location']
         }
 
def makeQueryDict(slotSizeID):

  # Find the job info and the stage's any_location flag
  try:
    query = ('SELECT '
             'sites.site_name,'
             'slot_sizes.min_processors,'
             'slot_sizes.max_processors,'
             'slot_sizes.min_rss_bytes,'
             'slot_sizes.max_rss_bytes,'
             'slot_sizes.max_wall_seconds '
             'FROM slot_sizes '
             'LEFT JOIN sites ON slot_sizes.site_id=sites.site_id '
             'WHERE slot_sizes.slot_size_id=' + str(slotSizeID))

    wfs.db.cur.execute(query)
    slotSize = wfs.db.cur.fetchone()
  except:
    return { "error_message": "Failed to find slot size from slotSizeID" }
 
  try:
    query = ('SELECT sites_storages.rse_id,location,rse_name,'
             'occupancy,rse_write,rse_read,ignore_for_output '
             'FROM sites_storages '
             'LEFT JOIN storages ON storages.rse_id=sites_storages.rse_id '
             'LEFT JOIN sites ON sites.site_id=sites_storages.site_id '
             'WHERE sites.site_name="%s" '
             'ORDER BY location,occupancy,RAND();' % slotSize['site_name'])

    wfs.db.cur.execute(query)
    storageRows = wfs.db.cur.fetchall()

  except:
    return { "error_message": "Failed to fetch storages info" }

  outputRseList  = [] 
  samesiteList   = []
  nearbyList     = []
  sameregionList = []
  accessibleList = []

  for storageRow in storageRows:

    if not storageRow['ignore_for_output'] and \
       storageRow['rse_id'] != wfs.conf.MonteCarloRseID and \
       storageRow['occupancy'] < 1.0 and \
       storageRow['rse_write']:
      # storageRows is already sorted by RSE location vs our site
      outputRseList.append(storageRow['rse_name'])

    if storageRow['rse_read']:
      if storageRow['location'] == 'accessible':
        accessibleList.append('replicas.rse_id=%s' % storageRow['rse_id'])
      elif storageRow['location'] == 'sameregion':
        sameregionList.append('replicas.rse_id=%s' % storageRow['rse_id'])
      elif storageRow['location'] == 'nearby':
        nearbyList.append('replicas.rse_id=%s' % storageRow['rse_id'])
      elif storageRow['location'] == 'samesite':
        samesiteList.append('replicas.rse_id=%s' % storageRow['rse_id'])

  storageWhere = ' OR '.join(samesiteList + nearbyList)

  if accessibleList or sameregionList:
    if storageWhere:
      storageWhere += ' OR '

    storageWhere += ('(stages.any_location AND (' + 
                     ' OR '.join(accessibleList + sameregionList) + '))')

  if storageWhere:
    storageWhere = ' AND (' + storageWhere + ') '

  # All storages in the same class (samesite, nearby, sameregion, accessible) 
  # get the same ranking score (4,3,2,1). In the future, we can apply 
  # individual scores here to each storage relative to where the job is 
  # running.
 
  if samesiteList:
    storageOrder = '4*(' + ' OR '.join(samesiteList) + ')'
  else:
    storageOrder = ''

  if nearbyList:
    if storageOrder:
      storageOrder += ' + '
  
    storageOrder += '3*(' + ' OR '.join(nearbyList) + ')'

  if sameregionList:
    if storageOrder:
      storageOrder += ' + '

    storageOrder += '2*(' + ' OR '.join(sameregionList) + ')'

  if accessibleList:
    if storageOrder:
      storageOrder += ' + '

    storageOrder += '1*(' + ' OR '.join(accessibleList) + ')'

  # If we got anything for the storage ordering then complete the
  # expression including the comma; otherwise an empty string
  if storageOrder:
    storageOrder += ' DESC,'

  return { "error_message"   : None,
           "outputRseList"   : outputRseList,
           "samesiteList"    : samesiteList,
           "nearbyList"      : nearbyList,
           "accessibleList"  : accessibleList,
           "storageWhere"    : storageWhere,
           "storageOrder"    : storageOrder,
           "min_processors"  : slotSize['min_processors'],
           "max_processors"  : slotSize['max_processors'],
           "min_rss_bytes"   : slotSize['min_rss_bytes'],
           "max_rss_bytes"   : slotSize['max_rss_bytes'],
           "max_wall_seconds": slotSize['max_wall_seconds']
         }

# Just in time decision making: identify the best request+stage combination
# based on the immediate situation rather than trying to plan ahead
def findStage(queryDict):

  query = (
 "SELECT stages.request_id,stages.stage_id,"
 "stages.any_location,"
 "files.file_did,files.file_id,storages.rse_name "
 "FROM files "
 "LEFT JOIN stages ON files.request_id=stages.request_id AND "
 "files.stage_id=stages.stage_id "
 "LEFT JOIN requests ON requests.request_id=files.request_id "
 "LEFT JOIN replicas ON files.file_id=replicas.file_id "
 "LEFT JOIN storages ON replicas.rse_id=storages.rse_id "
 "WHERE files.state='unallocated' AND " 
 "requests.state='running' AND "
 "((%d < stages.processors AND stages.processors <= %d AND "
 "  stages.rss_bytes <= %d) OR "
 " (%d < stages.rss_bytes AND stages.rss_bytes <= %d AND "
 "  stages.processors <= %d)) AND "
 "stages.wall_seconds <= %d %s "
 "AND storages.rse_name IS NOT NULL "
 "ORDER BY %sfiles.request_id,files.file_id "
 "LIMIT 1 FOR UPDATE" %
 (queryDict["min_processors"], queryDict["max_processors"], 
  queryDict["max_rss_bytes"],
  queryDict["min_rss_bytes"], queryDict["max_rss_bytes"],
  queryDict["max_processors"],
  queryDict["max_wall_seconds"], 
  queryDict["storageWhere"],
  queryDict["storageOrder"]
 ))

#  print(query, file=sys.stderr)
  
  wfs.db.cur.execute(query)
  fileRow = wfs.db.cur.fetchone()
  
  if not fileRow:
    return None

  # The dictionary to return, with the highest priority result
  stage = { 'request_id'  : fileRow['request_id'],
            'stage_id'    : fileRow['stage_id'],
            'any_location': bool(fileRow['any_location']) }

  return stage

# Make a dictionary containing one file's information
def findFile(jobDict, queryDict):

  if jobDict['any_location']:
    # If this stage can access data on any accessible storage, then 
    # use all three lists
    storageWhere = ' OR '.join(queryDict["samesiteList"] + 
                               queryDict["nearbyList"] + 
                               queryDict["sameregionList"] + 
                               queryDict["accessibleList"])
  else:
    # Otherwise just use samesite and nearby lists of storages
    storageWhere = ' OR '.join(queryDict["samesiteList"] + 
                               queryDict["nearbyList"])

  if storageWhere:
    storageWhere = ' AND (' + storageWhere + ') '

  query = (
"SELECT files.file_id,files.file_did,storages.rse_name,"
"replicas.rse_id,replicas.pfn "
"FROM files "
"LEFT JOIN replicas ON files.file_id=replicas.file_id "
"LEFT JOIN storages ON replicas.rse_id=storages.rse_id "
"WHERE files.state='unallocated' AND files.request_id=%d "
"AND files.stage_id=%d %s AND storages.rse_NAME IS NOT NULL "
"ORDER BY %sfiles.file_id LIMIT 1 FOR UPDATE" %
(jobDict['request_id'], jobDict['stage_id'], 
 storageWhere, 
 queryDict['storageOrder'])) 
      
  wfs.db.cur.execute(query)
  fileRows = wfs.db.cur.fetchall()
  
  if len(fileRows) == 0:
    # No matches found
    return { 'error_message': None,
             'file_did'     : None
           }

  try: 
    query = ("INSERT INTO allocations SET allocation_time=NOW(),"
             "rse_id=" + str(fileRows[0]['rse_id']) + ","
             "wfs_job_id=" + str(jobDict['wfs_job_id']) + ","
             "file_id=" + str(fileRows[0]['file_id'])
            )
    wfs.db.cur.execute(query)

    allocationID = wfs.db.cur.lastrowid

    query = ("UPDATE files SET state='allocated',"
             "last_allocation_id=" + str(allocationID) + " "
             "WHERE file_id=" + str(fileRows[0]['file_id'])
            )
    wfs.db.cur.execute(query)
  except Exception as e:
    # If anything goes wrong, we stop straightaway
    return { 'error_message': 'Failed recording state change: ' + str(e) }

  # The dictionary to return
  return { 'error_message': None,
           'file_did'     : fileRows[0]['file_did'],
           'pfn'          : fileRows[0]['pfn'],
           'rse_name'     : fileRows[0]['rse_name']
         }

def updateStageCounts(requestID, stageID):

  try:
    # Use a brute force recount of everything for this 
    # stage rather than try to use increments
    query = ('UPDATE stages SET '
             'num_finding=(SELECT COUNT(*) FROM files'
             ' WHERE state="finding" AND request_id=%d AND stage_id=%d),'
             'num_unallocated=(SELECT COUNT(*) FROM files'
             ' WHERE state="unallocated" AND request_id=%d AND stage_id=%d),'
             'num_allocated=(SELECT COUNT(*) FROM files'
             ' WHERE state="allocated" AND request_id=%d AND stage_id=%d),'
             'num_processed=(SELECT COUNT(*) FROM files'
             ' WHERE state="processed" AND request_id=%d AND stage_id=%d) '
             'WHERE request_id=%d AND stage_id=%d' % 
             (requestID, stageID,
              requestID, stageID,
              requestID, stageID,
              requestID, stageID,
              requestID, stageID)
            )
    wfs.db.cur.execute(query)
  except:
    pass
