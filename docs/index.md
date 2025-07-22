# justIN workflow system documentation

justIN manages DUNE workflows on the grid. It allows you to process datasets 
registered in MetaCat and Rucio and to run simulations, and implements the
design described in the DUNE Offline Computing Conceptual Design Report.

- [System Overview](overview.md)

## Tutorials

- [DUNE Tutorial](tutorials.dune.md)
- [DUNE GPU mini-tutorial](/20250521-mcnab-justin-gpu.pdf)

## User Guides

- [justin command](justin_command.md)
    - [man page](justin_command.man_page.md)
    - [Standalone setup](justin_command.standalone.md)
    - [justin-fetchlogs man page](justin-fetch-logs.man_page.md)
- [Monte Carlo workflows](monte_carlo.md)
- [Jobscripts](jobscripts.md)
    - [Interactive testing](jobscripts.interactive_tests.md)
    - [Rapid Code Distribution Service](jobscripts.rcds.md)
    - [Support for GPU jobscripts](jobscripts.gpu.md)

## System Components

- [Database](database.md)
- [Agents](agents.md)
- [Services](services.md)
- [Dashboard](dashboard.md)
- [Automated Workflow Tests](awt.md)
- [Information API](api.info.md)

## Reference 

- [Current change log](CHANGELOG.md)
- [Integration instance](integration_instance.md)
- [Event types](event_types.md)
- [Wrapper jobs](wrapper_jobs.md)
- [Files](files.md)
- [File processing lifecycle](file_processing.md)
- [Security model](security_model.md)
- [Download statistics](download_statistics.md)

Versioned copies of this documentation are kept in the docs subdirectory
of the [dune-justin GitHub repo](https://github.com/DUNE/dune-justin/). All the
files are in written in Markdown and so they can be read directly from the 
repository
if necessary. For convenience, the version of the documentation from the 
current release branch is available on the justIN dashboard
[https://dunejustin.fnal.gov/docs/](https://dunejustin.fnal.gov/docs/)
