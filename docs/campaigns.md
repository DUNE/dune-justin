## justIN campaigns

Campaigns allow you to group your workflows together to make it easier to
monitor and manage them. By default, each workflow is created as a member 
of a new campaign containing only itself. You can see a workflow's 
campaign ID number by going to the page dedicated to that workflow.

You can add a workflow to an existing campaign with ID number NN by using 
the `--campaign-id NN` option to the `justin create-workflow` 
or `justin simple-workflow` commands. 

You can also create a new campaign from scratch with the 
`justin create-campaign` command. You can use the options `--description` 
to add a short description, `--quota` to specify the named quota of the
campaign, and `--campaign-id-file` to add the resulting campaign ID to
a file (as well as to your screen still.) 

For example:

    justin create-campaign --description 'my test campaign' \
      --quota usertests --campaign-id-file $HOME/mycampaigns.txt

You could then use that campaign ID with the option

    --campaign-id `tail -1 $HOME/mycampaigns.txt`

when you create workflows to be assigned to it.

Each campaign has a dedicated page on the Dashboard which you can either
find from the [list of campaigns](/dashboard/?method=list-campaigns) or
from the link on one of its workflows' pages.

If you are signed in to the Dashboard, where a workflow's own page says
what campaign it is in, there is an Edit button which allows you to assign
the workflow to another campaign or to create a new, empty campaign to
put the workflow into (unless the workflow is already in a campaign by 
itself.)

The real power of the campaigns feature is the table of workflows on the
page for each campaign. This shows the state and file processed statistics 
for each workflow, and allows you to see at a glance the percentage
completion. At the bottom of the table are grand totals and links to CSV
and JSON versions of the table which you can import into spreadsheets and
your own scripts.
