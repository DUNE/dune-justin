# justIN security model

justIN has three largely independent security systems: how users are
authenticated and receive DUNE group memberships; how justIN decides what it
will do on behalf of a particular user; and how credentials are supplied to
justIN jobs to allow them to act for a particular user.

## User authentication

Users authenticate to justIN through the 
[justIN web dashboard](dashboard.md), using CILogon
and the Fermilab SSO identity provider. This is the case whether the user
is using the web dashboard itself or using the 
[`justin` command-line client](justin_command.md).
For the `justin` command, the user must re-authorize their session every
7 days by visiting a specified URL on the web dashboard. justIN gives the
command a session ID and secret which it stores in a file in `/var/tmp`.

After authenticating the user with their web browser, justIN uses an OIDC
call to CILogon to check the validity of the authentication and obtain a WLCG
access token, identity token, and refresh token for that user, and extracts
the users's eduPersonPrincipalName and DUNE wlcg.groups. 

The access token and refresh token are saved in the justIN database, and the
[justIN finder agent](agents.finder.md) refreshes the access token with
OIDC calls to CILogon so it is immediately available to the 
[justIN allocator](services.allocator.md) without any latency.
Refreshing continues as long as the user has an unexpired web or
command line session. 

Users may view their current access token after
logging in by clicking on the orange button with their username at the top 
right of any page and looking at the Your Access Token table. This also
shows the OAuth scopes requested from CILogon.

## DUNE groups and Rucio scopes

To use justIN, each user must be a member of the /dune group and may be a
member of additional groups. These are updated from CILogon each time the 
user logs in. 

justIN also obtains a list of the current scopes known to Rucio and 
assigns some of them to a group. In general, several scopes are assigned to
each group. Every member of the group for a particular scope is entitled to 
create files and datasets within that scope. justIN checks user group 
membership when a user asks justIN to create files within a scope. This only
covers writing and file creation: every DUNE member is able to read DUNE
files.

The scopes are also used to control write the 
ability to modify workflows to process files. 

## Credentials in justIN jobs

When the [justIN job factory](agents.job_factory.md) submits wrapper jobs to 
the DUNE HTCondor pool, 
it creates a secret for that cluster of jobs as a string. This secret
is passed to the job as a file and also stored in the justIN database for 
each job in the cluster. The wrapper jobs use the secrets to authenticate
to the justIN allocator service, in the form of HMAC SHA256 hashes of the
method, time and job ID to prevent replay attacks and reuse of unused hashes.

When the wrapper job starts it sends a `get_jobscript` request to the allocator 
to get the jobscript and job parameters for its stage within its workflow 
that it will work on. As part of this
message, the job includes an X.509 certificate signing request which matches
an RSA key it has created. The allocator signs the request with a VOMS proxy
it has and returns the certificates chain to the job, which is then able to 
assemble a valid VOMS proxy includng the private key it created earlier.

Two VOMS proxies are delegated to the job in this way: one with no roles and
only the ability to read from storage, which is shared with the container
running the user's jobscript; and one with the DUNE Production role
which allows the wrapper job to register output files in MetaCat and Rucio 
and to upload files on behalf of the user after the
jobscript has finished.

This response also provides another secret: the
jobscript secret. This is only used within the inner Apptainer container 
that runs the user's jobscript, to ask the justIN allocator to allocate files 
to the job. This secret is specific to that job and cannot be used
for other methods than `get_file`.

When the user jobscript finishes, the wrapper job uses the `record_results` 
method to tell the allocator which files have been processed and what output
files are to be uploaded. 

The allocator supplies the user's access token 
to allow the wrapper job to upload to scratch areas as the user.

Output files either go to dCache scratch space using the token or to
Rucio-managed storage using the Production role VOMS proxy. In the Rucio
case the files are also registered in MetaCat and added to the correct 
Rucio dataset. 

Finally the `confirm_results` method uses the job's hashed
secret to communicate the outcome of the uploads to the allocator. 
