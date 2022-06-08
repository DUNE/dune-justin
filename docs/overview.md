## Overview of the Workflow System

The Workflow subsystem includes all aspects of orchestrating the execution 
of code to generate simulated data and to process real or simulated 
data at computing sites around the world.

To make the most efficient use of the finite computing, network, and 
storage resources available to the experiment, the design of 
the Workflow System are driven by the location and availability of data to 
be processed and it’s proximity to computing capacity as it becomes available. 

Efficiently matching CPU and data is a long-standing problem in 
HEP computing. We have developed 
a relatively un-hierachical system that uses improved knowledge of the 
computing properties of applications (I/O rate, memory needs, data size) 
and the network connections between Rucio Storage Elements (RSEs) and 
CPU resources to optimally match processing and data.

### Request Lifecycle

The central concept of the Workflow System is a request that 
describes how some data processing activity is to be carried out. Requests 
are submitted by users (which may include members of a central production 
team) to the [Workflow Database](database.md), where it progresses 
through several states. For example: draft > submitted > approved > 
running > paused > running > checking > completed > archived. Human 
intervention is needed for some transitions, e.g., from submitted to 
approved. Requests also have types and priorities. For example, simulation 
or user analysis, and high or low, respectively.

As part of its definition, a request may include one or more stages, each 
of which can apply a sequence of processing steps to the input or output 
files. Each stage specifies a bootstrap script used by generic jobs to run 
the relevant applications. The script specifies the requirements on the 
worker nodes (for example memory) and the maximum number of input files to 
be issued to the job executing that stage.

The request definition will usually include a MetaCat MQL query 
to generate a list of files to be processed in the first stage. This list of 
files is cached in the central Workflow Database, associated with the 
first stage of that request. All these files are set to the unallocated 
state.

Once the [Finder agent](wfs-finder.md) has finished building the request, 
it can move to the running state and the bootstrap script associated with 
the first stage will begin execution.

