# Finder agent

The Finder agent periodically executes searches in the 
[justIN database](database.md) to discover updates that are required to
the state of workflows, files, replicas and jobs.

It processes workflows using the specified MQL expression to generate a
list of input files for the first stage of the workflow, either by submitting
a true MQL query to MetaCat, or it submits a query to Rucio to obtain a list
of files in a given dataset, or it creates a list of virtual counter files
to keep track of [Monte Carlo](monte_carlo.md) productions.

It processes files in the finding state to discover the location of their
replicas from Rucio.

It processes workflows where all input files to all stages have reached a
terminal state (processsed, failed, or output), and sets these workflows to
the Finished state.

