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

# Return information about the job from the jobsubID
def makeJobDict(jobsubID, cookie = None):

  # Find the job info and the stage's max_distance value
  try:
    query = ('SELECT '
             'jobs.slot_size_id,'
             'jobs.allocation_state,'
             'jobs.cookie,'
             'stages.max_distance,'
             'jobs.request_id,'
             'jobs.stage_id,'
             'jobs.wfs_job_id,'
             'jobs.site_id,'
             'slot_sizes.min_processors,'
             'slot_sizes.max_processors,'
             'slot_sizes.min_rss_bytes,'
             'slot_sizes.max_rss_bytes,'
             'slot_sizes.max_wall_seconds '
             'FROM jobs '
             'LEFT JOIN stages ON jobs.request_id=stages.request_id '
             'AND jobs.stage_id=stages.stage_id '
             'LEFT JOIN slot_sizes '
             'ON slot_sizes.slot_size_id=jobs.slot_size_id '
             'WHERE jobs.jobsub_id="' + jobsubID + '"')

    wfs.db.cur.execute(query)
    job = wfs.db.cur.fetchone()
  except Exception as e:
    return { "error_message": "Error finding job from jobsubID: " + str(e) }

  if not job:
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
           "max_distance"     : job['max_distance'],
           "min_processors"   : job['min_processors'],
           "max_processors"   : job['max_processors'],
           "min_rss_bytes"    : job['min_rss_bytes'],
           "max_rss_bytes"    : job['max_rss_bytes'],
           "max_wall_seconds" : job['max_wall_seconds']
         }

# Make a dictionary in the same format as makeJobDict() but using the 
# slotSizeID - this is used by wfs-job-agent to test for waiting matches
def makeSlotSizeDict(slotSizeID):

  try:
    query = ('SELECT '
             'sites.site_name,'
             'slot_sizes.site_id,'
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

  return { "error_message"   : None,
           "site_id"         : slotSize['site_id'],
           "min_processors"  : slotSize['min_processors'],
           "max_processors"  : slotSize['max_processors'],
           "min_rss_bytes"   : slotSize['min_rss_bytes'],
           "max_rss_bytes"   : slotSize['max_rss_bytes'],
           "max_wall_seconds": slotSize['max_wall_seconds']
         }

# Just in time decision making: identify the best request+stage combination
# based on the immediate situation rather than trying to plan ahead
def findStage(jobDict, limit=1):

  query = (
 "SELECT stages.request_id,stages.stage_id,stages.max_distance "
 "FROM files "
 "LEFT JOIN stages ON files.request_id=stages.request_id AND "
 "files.stage_id=stages.stage_id "
 "LEFT JOIN requests ON requests.request_id=files.request_id "
 "LEFT JOIN replicas ON files.file_id=replicas.file_id "
 "LEFT JOIN storages ON replicas.rse_id=storages.rse_id "
 "LEFT JOIN sites_storages ON replicas.rse_id=sites_storages.rse_id AND "
 "sites_storages.site_id=%d "
 "WHERE files.state='unallocated' AND " 
 "replicas.accessible_until > NOW() AND "
 "requests.state='running' AND "
 "((%d < stages.processors AND stages.processors <= %d AND "
 "  stages.rss_bytes <= %d) OR "
 " (%d < stages.rss_bytes AND stages.rss_bytes <= %d AND "
 "  stages.processors <= %d)) AND "
 "stages.wall_seconds <= %d "
 "AND sites_storages.distance IS NOT NULL "
 "AND sites_storages.distance <= stages.max_distance "
 "AND storages.rse_read "
 "ORDER BY sites_storages.distance,files.request_id,files.file_id "
 "LIMIT %d FOR UPDATE" %
 (
  jobDict["site_id"],
  jobDict["min_processors"], jobDict["max_processors"], 
  jobDict["max_rss_bytes"],
  jobDict["min_rss_bytes"], jobDict["max_rss_bytes"],
  jobDict["max_processors"],
  jobDict["max_wall_seconds"],
  limit
 ))
  
  wfs.db.cur.execute(query)
  fileRows = wfs.db.cur.fetchall()
  
  if len(fileRows) == 0:
    return None

  # The dictionary to return, with the highest priority result
  stage = { 'request_id'  : fileRows[0]['request_id'],
            'stage_id'    : fileRows[0]['stage_id'],
            'max_distance': fileRows[0]['max_distance'],
            'matches'     : len(fileRows) }

  return stage

# Make a dictionary containing one file's information
def findFile(jobDict):

  query = (
"SELECT files.file_id,files.file_did,storages.rse_name,"
"replicas.rse_id,replicas.pfn "
"FROM files "
"LEFT JOIN replicas ON files.file_id=replicas.file_id "
"LEFT JOIN storages ON replicas.rse_id=storages.rse_id "
"LEFT JOIN sites_storages ON replicas.rse_id=sites_storages.rse_id AND "
"sites_storages.site_id=%d "
"WHERE files.state='unallocated' "
"AND files.request_id=%d "
"AND files.stage_id=%d AND storages.rse_NAME IS NOT NULL "
"AND sites_storages.distance IS NOT NULL "
"AND sites_storages.distance <= %f "
"AND replicas.accessible_until > NOW() "
"ORDER BY sites_storages.distance,files.file_id LIMIT 1 FOR UPDATE" %
(jobDict['site_id'], jobDict['request_id'], jobDict['stage_id'],
 jobDict['max_distance'])
          )
      
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
             "allocations=allocations+1,"
             "wfs_job_id=" + str(jobDict['wfs_job_id']) + " "
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
# Do a brute force recount of everything for this stage rather than try 
# to use increments

# DEADLOCKS!!!
#  try:
#    # Use a brute force recount of everything for this 
#    # stage rather than try to use increments
#    query = ('UPDATE stages SET '
#             'num_finding=(SELECT COUNT(*) FROM files'
#             ' WHERE state="finding" AND request_id=%d AND stage_id=%d),'
#             'num_unallocated=(SELECT COUNT(*) FROM files'
#             ' WHERE state="unallocated" AND request_id=%d AND stage_id=%d),'
#             'num_allocated=(SELECT COUNT(*) FROM files'
#             ' WHERE state="allocated" AND request_id=%d AND stage_id=%d),'
#             'num_uploading=(SELECT COUNT(*) FROM files'
#             ' WHERE state="uploading" AND request_id=%d AND stage_id=%d),'
#             'num_notfound=(SELECT COUNT(*) FROM files'
#             ' WHERE state="processed" AND request_id=%d AND stage_id=%d),'
#             'num_notfound=(SELECT COUNT(*) FROM files'
#             ' WHERE state="notfound" AND request_id=%d AND stage_id=%d) '
#             'WHERE request_id=%d AND stage_id=%d' % 
#             (requestID, stageID,
#              requestID, stageID,
#              requestID, stageID,
#              requestID, stageID,
#              requestID, stageID,
#              requestID, stageID,
#              requestID, stageID)
#            )
#    wfs.db.cur.execute(query)
#  except:
#    pass

  try:
    # Get the counts
    query = ('SELECT '
             '(SELECT COUNT(*) FROM files'
             ' WHERE state="finding" AND request_id=%d AND stage_id=%d) '
             ' AS num_finding,'
             '(SELECT COUNT(*) FROM files'
             ' WHERE state="unallocated" AND request_id=%d AND stage_id=%d) '
             ' AS num_unallocated,'
             '(SELECT COUNT(*) FROM files'
             ' WHERE state="allocated" AND request_id=%d AND stage_id=%d) '
             ' AS num_allocated,'
             '(SELECT COUNT(*) FROM files'
             ' WHERE state="uploading" AND request_id=%d AND stage_id=%d) '
             ' AS num_uploading,'
             '(SELECT COUNT(*) FROM files'
             ' WHERE state="processed" AND request_id=%d AND stage_id=%d) '
             ' AS num_processed,'
             '(SELECT COUNT(*) FROM files'
             ' WHERE state="notfound" AND request_id=%d AND stage_id=%d) '
             ' AS num_notfound'
             % 
             (requestID, stageID,
              requestID, stageID,
              requestID, stageID,
              requestID, stageID,
              requestID, stageID,
              requestID, stageID)
            )
    wfs.db.cur.execute(query)
    row = wfs.db.cur.fetchone()

    # Update the stage
    query = ('UPDATE stages SET '
             'num_finding=%d,'
             'num_unallocated=%d,'
             'num_allocated=%d,'
             'num_uploading=%d,'
             'num_processed=%d,'
             'num_notfound=%d '
             'WHERE request_id=%d AND stage_id=%d' %
             (row['num_finding'],
              row['num_unallocated'],
              row['num_allocated'],
              row['num_uploading'],
              row['num_processed'],
              row['num_notfound'],
              requestID, stageID))
             
    wfs.db.cur.execute(query)

  except:
    pass

