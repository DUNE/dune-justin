## dune-justin
justIN - DUNE workflow system

See https://dunejustin.fnal.gov/docs/ for documentation

### Branches/tags policy

Most development happens on the main branch, via pull requests. 

Version numbers in the form MM.mm.pp with major, minor and patch versions.
For releases, each of the three numbers has two digits, usually with a 
leading 0. Release candidates for new minor releases are prepared on the main
branch and have a patch version of the form rcN, for release candidate N.

When a minor release is made, a new branch named MM.mm is created.
The start of that branch is tagged as MM.mm.00 The same procedure is used for
major releases.

If patch releases are needed for any releases to fix bugs, then 
the updates are made on that existing release branch, and new tags named 
MM.mm.01 etc are made on that branch once the code is ready.

Distribution via cvmfs etc is based on those three number tags on release
branches.

Patch updates will only be bug fixes. Minor releases will only fix bugs and
add backwards compatible features. In both cases it should be possible to
upgrade without any additional human intervention. Clearly the risk of 
introducing new bugs is higher when adding new features rather than just fixing
known bugs.

Major releases introduce changes which may require human intervention to
update configuration files, use different API calls etc.
