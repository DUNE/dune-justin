Release notes for 00.12 

This version of justIN involves several significant and visible changes from 
previous versions.

1) The term "workflow" replaces "request" and "workflow request" throughout.
   A workflow is now the name for a set of one or more processing stages.
2) The quick-request subcommand of the justin command is now simple-workflow
3) The --refind-start-date option has been dropped from the create-workflow
   and simple-workflow subcommands. If refinding is triggered then it will
   start as soon as the workflow enters the running state.
4) It is now possible to pass options to the justin command using the 
   $JUSTIN_OPTIONS environment variable. The contents of this variable are
   inserted in the list of options directly after the subcommand. 
5) A --classad option has been added to create-stage and simple-workflow 
   which allows the insertion of extra ClassAds in the HTCondor wrapper
   jobs.

The justin and other command man pages have been updated to reflect these and
other changes.