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

# Return various strings and SQL expressions which are 
# used in subsequent queries
def makeQueryTerms(jsonDict, job):

  query = ('SELECT sites_storages.rse_id,location,rse_name,'
           'occupancy '
           'FROM sites_storages '
           'LEFT JOIN storages ON storages.rse_id=sites_storages.rse_id '
           'LEFT JOIN sites ON sites.site_id=sites_storages.site_id '
           'WHERE sites.site_name="%s" '
           'ORDER BY location,occupancy,RAND();' 
           % job['site_name'])

  wfs.db.cur.execute(query)
  storageRows = wfs.db.cur.fetchall()

  outputRseList  = [] 
  samesiteList   = []
  nearbyList     = []
  accessibleList = []

  for storageRow in storageRows:

    if storageRow['occupancy'] < 1.0:
      outputRseList.append(storageRow['rse_name'])
  
    if storageRow['location'] == 'accessible':
      accessibleList.append('replicas.rse_id=%s' % storageRow['rse_id'])
    elif storageRow['location'] == 'nearby':
      nearbyList.append('replicas.rse_id=%s' % storageRow['rse_id'])
    elif storageRow['location'] == 'samesite':
      samesiteList.append('replicas.rse_id=%s' % storageRow['rse_id'])

  storageWhere = ' OR '.join(samesiteList + nearbyList)

  if accessibleList:
    if storageWhere:
      storageWhere += ' OR '

    storageWhere += ('(stages.any_location AND (' + 
                     ' OR '.join(accessibleList) + '))')

  if storageWhere:
    storageWhere = ' AND (' + storageWhere + ') '

  # All storages in the same class (samesite, nearby, accessible) get the
  # same ranking score (3,2,1). In the future, we can apply individual
  # scores here to each storage relative to where the job is running.
 
  if samesiteList:
    storageOrder = '3*(' + ' OR '.join(samesiteList) + ')'
  else:
    storageOrder = ''

  if nearbyList:
    if storageOrder:
      storageOrder += ' + '
  
    storageOrder += '2*(' + ' OR '.join(nearbyList) + ')'

  if accessibleList:
    if storageOrder:
      storageOrder += ' + '

    storageOrder += '1*(' + ' OR '.join(accessibleList) + ')'

  # If we got anything for the storage ordering then complete the
  # expression including the comma; otherwise an empty string
  if storageOrder:
    storageOrder += ' DESC,'

  return { "outputRseList"  : outputRseList,
           "samesiteList"   : samesiteList,
           "nearbyList"     : nearbyList,
           "accessibleList" : accessibleList,
           "storageWhere"   : storageWhere,
           "storageOrder"   : storageOrder
         }

# Just in time decision making: identify the best request+stage combination
# based on the immediate situation rather than trying to plan ahead
def findStage(queryTerms, job):

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
 "WHERE files.state='unallocated' AND " +
 str(job["processors"])   + " <= stages.max_processors AND " +
 str(job["processors"])   + " >= stages.min_processors AND " +
 str(job["rss_bytes"])    + " >= stages.max_rss_bytes AND " +
 str(job["wall_seconds"]) + " >= stages.max_wall_seconds " +
 queryTerms["storageWhere"] + " AND storages.rse_name IS NOT NULL " +
 " ORDER BY " + 
 queryTerms["storageOrder"] + "files.request_id,files.file_id"
 " LIMIT 1 FOR UPDATE"
 )

  wfs.db.cur.execute(query)
  fileRows = wfs.db.cur.fetchall()
  
  if len(fileRows) == 0:
    return None

  # Take the values of the highest priority result
  requestID   = int(fileRows[0]['request_id'])
  stageID     = int(fileRows[0]['stage_id'])
  anyLocation = bool(fileRows[0]['any_location'])
  
  # The dictionary to return
  stage = { 'request_id'  : requestID,
            'stage_id'    : stageID,
            'any_location': anyLocation }

  return stage

# Make a dictionary containing one job's information
def findJob(jsonDict):

  try:
    wfsJobID  = int(jsonDict['wfs_job_id'])
    cookie = str(jsonDict['cookie'])
  except:
    return None

  # Find the job info and the stage's any_location flag
  try:
    query = ('SELECT wfs_jobs.request_id,'
             'wfs_jobs.stage_id,'
             'wfs_jobs.state,'
             'sites.site_name,'
             'wfs_jobs.hostname,'
             'wfs_jobs.cpuinfo,'
             'wfs_jobs.os_release,'
             'wfs_jobs.rss_bytes,'
             'wfs_jobs.processors,'
             'wfs_jobs.wall_seconds,'
             'stages.any_location '
             'FROM jobs '
             'LEFT JOIN sites ON wfs_jobs.site_id=sites.site_id '
             'LEFT JOIN stages ON wfs_jobs.stage_id=stages.stage_id '
             'WHERE wfs_jobs.wfs_job_id=' + str(wfsJobID) + ' AND ' +
             'wfs_jobs.cookie="' + cookie + '"')

    wfs.db.cur.execute(query)
    rows=wfs.db.cur.fetchall()
    
    job = { 'wfs_job_id' : wfsJobID,
            'cookie'           : cookie,
            'request_id'       : int(rows[0]['request_id']),
            'stage_id'         : int(rows[0]['stage_id']),
            'state'            : rows[0]['state'],
            'site_name'        : rows[0]['site_name'],
            'hostname'         : rows[0]['hostname'],
            'cpuinfo'          : rows[0]['cpuinfo'],
            'os_release'       : rows[0]['os_release'],
            'rss_bytes'        : int(rows[0]['rss_bytes']),
            'processors'       : int(rows[0]['processors']),
            'wall_seconds'     : int(rows[0]['wall_seconds']),
            'any_location'     : bool(rows[0]['any_location'])
          }
          
    return job
    
  except:
    # WE SHOULD PROVIDE SOME KIND OF DEBUGGING FOR ALL THIS!!
    return None

# Make a dictionary containing one file's information
def findOneFile(jsonDict, queryTerms, job):

  if job['any_location']:
    # If this stage can access data on any accessible storage, then 
    # use all three lists
    storageWhere = ' OR '.join(queryTerms["samesiteList"] + 
                               queryTerms["nearbyList"] + 
                               queryTerms["accessibleList"])
  else:
    # Otherwise just use samesite and nearby lists of storages
    storageWhere = ' OR '.join(queryTerms["samesiteList"] + 
                               queryTerms["nearbyList"])

  if storageWhere:
    storageWhere = ' AND (' + storageWhere + ') '

  query = (
"SELECT files.file_id,files.file_did,storages.rse_name,"
"replicas.rse_id,replicas.pfn "
"FROM files "
"LEFT JOIN replicas ON files.file_id=replicas.file_id "
"LEFT JOIN storages ON replicas.rse_id=storages.rse_id "
"WHERE files.state='unallocated' AND files.request_id=" +
str(job['request_id']) + " AND files.stage_id=" + str(job['stage_id']) + 
storageWhere + " AND storages.rse_NAME IS NOT NULL "
"ORDER BY " + 
queryTerms["storageOrder"] + "files.file_id"
" LIMIT 1 FOR UPDATE"
) 
   
  print('DEBUG: ' + query, file=sys.stderr)
   
  wfs.db.cur.execute(query)
  fileRows = wfs.db.cur.fetchall()
  
  print('DEBUG: ' + str(fileRows), file=sys.stderr)
  
  if len(fileRows) == 0:
    return None

  try: 
    query = ("INSERT INTO allocations SET allocated_time=NOW(),"
             "rse_id=" + str(fileRows[0]['rse_id']) + ","
             "wfs_job_id=" + str(job['wfs_job_id']) + ","
             "file_id=" + str(fileRows[0]['file_id'])
            )
    wfs.db.cur.execute(query)

    allocationID = wfs.db.cur.lastrowid

    query = ("UPDATE files SET state='allocated',"
             "last_allocation_id=" + str(allocationID) + " "
             "WHERE file_id=" + str(fileRows[0]['file_id'])
            )
    wfs.db.cur.execute(query)
  except:
    # If anything goes wrong, we stop straightaway
    return None

  # The dictionary to return
  oneFile = { 'file_did'    : fileRows[0]['file_did'],
              'pfn'         : fileRows[0]['pfn'],
              'rse_name'    : fileRows[0]['rse_name']
            }
                      
  return oneFile

