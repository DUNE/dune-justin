# Interactive testing of jobscripts

If you need to create or modify jobscripts yourself then you need to learn 
how to test them. This is especially important since you do not want to 
create thousands of failing jobs, wasting your time, wasting the site's 
hardware, and wasting electricity.

justIN provides the command justin-test-jobscript which allows you to run a 
jobscript interactively on your computer. In jobs at remote sites, justIN 
runs your jobscripts inside a Singularity container. The 
justin-test-jobscript command runs your jobscript using the same container 
format and so provides a very realistic test of your script. The command 
is available to you after using the same setup justin command as for 
justin itself.

See the Interactive Tests section of the [DUNE Tutorial](tutorials.dune.md)
and the [justin-test-jobscript](jobscripts.interactive_tests.man_page.md) 
man page.

