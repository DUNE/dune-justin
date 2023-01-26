#
# justIn events
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
                           'Error raised by the bootstrap script'],

 # File events
 event_FILE_ALLOCATED_RESET  : ['FILE_ALLOCATED_RESET',
                                'File set back to unallocated from allocated'],
 event_FILE_SET_TO_FAILED    : ['FILE_SET_TO_FAILED',
                                'Too many attempts to process file: failed'],
 event_FILE_CREATED          : ['FILE_CREATED',
                                'Output file created in job'],
 event_FILE_OUTPUTTING_RESET : ['FILE_OUTPUTTING_RESET',
                                'File set back to unallocated from outputting']
             }
