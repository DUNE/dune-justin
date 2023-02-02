## Jobscripts Library

When a stage is created within a request in justIN, a 
[jobscript](jobscripts.md) is cached with the stage definition and executed
by all jobs that are allocated to that stage. The jobscript can be supplied
to the create-stage or quick-request command as a local file. Alternatively,
the jobscript can be taken from the Jobscripts Library. 

You can view the jobscripts currently in the library 
[on the justIN dashboard](https://justin.dune.hep.ac.uk/dashboard/?method=list-jobscripts).

Each jobscript in the library is referred to by its jobscript identifier
(JSID), of the form SCOPE:NAME or USER:NAME, where SCOPE is a Rucio scope
known to justIN and USER is a user name known to justIN, itself in the form
NAME@DOMAIN 

In the create-stage and quick-request subcommands of the justin command,
jobscripts from the library can be specified using the --jobscript-id JSID
option. The text of the jobscript at the time the stage is created is cached
with the stage, and future changes in the library are ignored for that stage.

To put a jobscript into the library, use the create-jobscript subcommand.

```
justin create-jobscript --name example1 \
                        --jobscript exam1.jobscript

justin create-jobscript --scope myscope --name example2 \
                        --jobscript exam2.jobscript
```

The first example takes your user name in NAME@DOMAIN format and uploads
the exam1.jobscript file to the library with a jobscript identifier like 
NAM@DOMAIN:example1. The second example uses the Rucio scope myscope and 
uploads exam2.jobscript with jobscript identifier myscope:example2.

You can create a description for the jobscript with the --description option.
