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

# Populate the list unallocatedCounts with tuples for the number of
# unallocated files for any running request or stage for each processor
# and memory combination
def getUnallocatedCounts():

  unallocatedCounts = []

  for processors in range(1, 9):
    for bytesPerProcessor in [2000 * 1024 * 1024, 4000 * 1024 * 1024]:
      
      try:
        matches = wfs.db.select('SELECT COUNT(*) AS count FROM files '
                                'LEFT JOIN requests '
                                'ON requests.request_id = files.request_id '
                                'LEFT JOIN stages '
                                'ON stages.request_id = files.request_id AND '
                                'stages.stage_id = files.stage_id '
                                'WHERE files.state = "unallocated" AND '
                                'requests.state="running" AND '
                                'stages.processors = %d AND '
                                'stages.rss_bytes > %d AND '
                                'stages.rss_bytes <= %d' %
                                (processors,
                                 bytesPerProcessor * (processors - 1),
                                 bytesPerProcessor * processors
                                ), justOne = True
                               )

        if matches['count']:
          unallocatedCounts.append((processors, 
                                    bytesPerProcessor,
                                    matches['count']
                                  ))
      except Exception as e:
        logLine('Failed getting count of unallocated: ' + str(e))
        continue

  return unallocatedCounts

def updateStageCounts(requestID, stageID):
# Do a brute force recount of everything for this stage rather than try 
# to use increments

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
             ' WHERE state="outputting" AND request_id=%d AND stage_id=%d) '
             ' AS num_outputting,'
             '(SELECT COUNT(*) FROM files'
             ' WHERE state="processed" AND request_id=%d AND stage_id=%d) '
             ' AS num_processed,'
             '(SELECT COUNT(*) FROM files'
             ' WHERE state="notfound" AND request_id=%d AND stage_id=%d) '
             ' AS num_notfound,'
             '(SELECT COUNT(*) FROM files'
             ' WHERE state="failed" AND request_id=%d AND stage_id=%d) '
             ' AS num_failed'
             % 
             (requestID, stageID,
              requestID, stageID,
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
             'num_outputting=%d,'
             'num_processed=%d,'
             'num_notfound=%d,'
             'num_failed=%d '
             'WHERE request_id=%d AND stage_id=%d' %
             (row['num_finding'],
              row['num_unallocated'],
              row['num_allocated'],
              row['num_outputting'],
              row['num_processed'],
              row['num_notfound'],
              row['num_failed'],
              requestID, stageID))
             
    wfs.db.cur.execute(query)

  except:
    pass

