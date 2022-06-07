#
#  WFS Database globals and functions
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


## Global database connection
conn = None
cur  = None

import re

rseAvailabilityDelete = 1
rseAvailabilityWrite  = 2
rseAvailabilityRead   = 4

unixEpoch = '1970-01-01 00:00:00'

jobStatesTerminal = [ 'finished', 'notused', 'aborted', 'stalled' ]

jobStatesAll = [ 'submitted', 'started', 'processing', 'uploading' ] \
               + jobStatesTerminal

maxAllocations = 6

def stringIsJobsubID(s):
  return re.search('[^A-Z,a-z,0-9,_,.,@,-]', s) is None

def stringIsDomain(s):
  return re.search('[^A-Z,a-z,0-9,.,-]', s) is None

def stringIsSite(s):
  return re.search('[^A-Z,a-z,0-9,_,-]', s) is None

def stringNoQuotes(s):
  return re.search('[",`,\']', s) is None

# Log an event to the database, returning an error message or None if no
# errors. You must ensure events are committed along with anything else
# you are writing to the database!!!
def logEvent(requestID = 0,
             stageID = 0,
             fileID = 0,
             wfsJobID = 0,
             siteID = 0,
             rseID = 0):

  try:
    query = ('INSERT INTO events SET '
             'request_id=%d,'
             'stage_id=%d,'
             'file_id=%d,'
             'wfs_job_id=%d,'
             'site_id=%d,'
             'rse_id=%d,'
             'event_time=NOW()' %
             requestID,
             stageID,
             fileID,
             wfsJobID,
             siteID,
             rseID)

    cur.execute(query)
    return None
  except Exception as e:
    return "Error logging event: " + str(e)
