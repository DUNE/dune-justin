#
# justIN allocator module
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

import os
import io
import re
import sys
import time
import json
import string
import tarfile
import MySQLdb

import justin

# Populate the list unallocatedCounts with tuples for the number of
# unallocated files for any running request or stage for each processor
# and memory combination
def getUnallocatedCounts():

  unallocatedCounts = []

  for processors in range(1, 9):
    for bytesPerProcessor in [2000 * 1024 * 1024, 4000 * 1024 * 1024]:
      
      try:
        matches = justin.select('SELECT COUNT(*) AS count FROM files '
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

# Try to find the text of a jobscript from the Jobscripts Library 
# given a JSID
def lookupJobscript(jsid):
  if ':' not in jsid:
    return { 'error': 'Jobscript identifier must contain ":"' }

  (prefix,name) = jsid.split(':',1)

  if not prefix or not name:
    return { 'error': 'Both parts of the JSID must be given' }

  if not justin.stringIsDomain(name):
    return { 'error': 'Invalid characters in jobscript name in JSID' }

  if '@' in prefix:
    # JSID is USER:NAME

    if not justin.stringIsUsername(prefix):
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

    if not justin.stringIsDomain(prefix):
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
    jobscriptRow = justin.select(query, justOne = True)
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

