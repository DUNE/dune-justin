# Overview of the justIN workflow system

justIN implements the workflow system design described in chapter 13 of the
["DUNE Offline Computing Conceptual Design Report"](https://arxiv.org/abs/2210.15665), 
A. Abed Abud et al (the DUNE Collaboration), FERMILAB-DESIGN-2022-01, 
28 October 2022.

The system is summarised in ["Just-in-time workflow management for DUNE"](https://www.epj-conferences.org/articles/epjconf/abs/2025/22/epjconf_chep2025_01216/epjconf_chep2025_01216.html),
Andrew McNab and Christopher Brew, 
EPJ Web of Conferences 337, 01216 (2025). This is the
best paper reference to give for the justIN system.

The justIN system includes all aspects of orchestrating the execution 
of code to generate simulated data and to process real or simulated 
data at computing sites around the world.

To make the most efficient use of the finite computing, network, and 
storage resources available to the experiment, the design of 
justIN was driven by the location and availability of data to 
be processed and its proximity to computing capacity as it becomes available. 

Efficiently matching CPU and data is a long-standing problem in 
HEP computing. We have developed 
a relatively un-hierachical system that uses improved knowledge of the 
computing properties of applications (I/O rate, memory needs, data size) 
and the network connections between Rucio Storage Elements (RSEs) and 
CPU resources to optimally match processing and data.

## Workflow Lifecycle

The central concept of justIN is the workflow, which 
describes how some data processing activity is to be carried out. Workflows 
are submitted by users (which may include members of a central production 
team) to the [justIN database](database.md), where it progresses 
through several states. For example: 
draft > submitted > running > paused > running > finished. 

As part of its definition, a workflow may include one or more stages, each 
of which can apply a sequence of processing steps to the input or output 
files. Each stage specifies a 
[jobscript](jobscripts.md) used by wrapper jobs to run 
the relevant applications. The stage definition specifies the requirements on 
the worker nodes (for example memory and job duration).

The workflow definition will usually include a MetaCat MQL query 
to generate a list of files to be processed in the first stage. This list of 
files is cached in the central justIN database, associated with the 
first stage of that workflow. All these files are set to the unallocated 
state.

Once the workflow has moved to the running state the 
[Finder agent](agents.finder.md) builds the list of input files for its first
stage, and looks up the replicas of each file using Rucio. Once replicas are 
available, then wrapper jobs submitted by the 
[justIN Job Factory](agents.job_factory.md)
will begin to match unallocated files and processing can begin.
