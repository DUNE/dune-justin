#
# justIn allocator module
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
import uuid
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
        matches = justin.db.select('SELECT COUNT(*) AS count FROM files '
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

