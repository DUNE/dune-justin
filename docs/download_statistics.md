## Download statistics

Several places in the dashboard give the option to download tables of
statistics about jobs and files in Comma Separated Variables (CSV) and JSON
formats. The CSV files have a header line with the column names and the same
names appear in a JSON dictionary for each row of the results. This page
gives further explaination. 

### File states

This is a live view of the states of the files during one stage of a
particular workflow. Go to the page for that workflow or for the stage. Then
in the table titled **File states per stage** or **File states** click on
one of the numbers representing the count of files in that state.

This takes you to a page with a list of files in that state. Near the bottom
are links to CSV and JSON versions of the table, with up to 10,000 rows. 

### Input and output file stats

These files are accessed by going to the page for a particular stage of a
workflow and then scrolling down to the **RSEs used** table. Below that
table are links to CSV and JSON files for input files processed and output
files uploaded. Only successes are included. size_bytes refers to the size
of that file. All the distances are the nominal distances applied by justIN
to group 
[site](https://justin-dev.dune.hep.ac.uk/dashboard/?method=list-sites) and 
[storages](https://justin-dev.dune.hep.ac.uk/dashboard/?method=list-storages) 
by location, nationality, region, and continent:
you can view distances by going to the page for any site or storage and
lookign at the table near the bottom.

For input files, seconds refers to the time for which the user's jobscript ran, 
which may have processed more than one file. The jobsub_id is provided, and so
it would be possible for you to reconstruct what input files were read 
together and from what RSEs at what distances. How that impacts any analysis of
performance you do depends on what metrics you are trying to understand
though.

For output files, seconds refers to the duration of the succesful Rucio upload
of that file, ignoring any retries and previous attempts to contact other
RSEs. 
