# Support for GPU jobscripts

If your application requires an NVIDIA GPU, then you can request one by
giving the option `--gpu` to the `justin create-stage` or 
`justin simple-workflow` commands as described in the 
[justin man page](justin_command.man_page.md).

**Currently there are a limited number of sites offering GPUs to DUNE and you
may need to wait significantly longer (hours?) than usual for jobs in the workflow
to start running.**

The CUDA libraries, drivers, /dev/nvidiaX devices, and tools like `nvidia-smi` are 
made available to your jobscript in the usual way. `$CUDA_VISIBLE_DEVICES` is
set to the UUID of the GPU allocated to your job by the site, in the newer form
`GPU-uuid` *not* as 0, 1, 2 etc. Please do not try to use any other GPUs you
might be able to access: by default CUDA should respect `$CUDA_VISIBLE_DEVICES` as
given and do what the site wants.

Once the wrapper job starts, it reports to justIN information about the GPU it has
discovered, including the GPU model name, the driver version, the compute
capability, the VBIOS version, and the nonreserved memory in MiB. 
This information is shown on the job's own page in the dashboard. 


