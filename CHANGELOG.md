# Changelog

## 01.01.00
- justin-prod-sched01.dune.hep.ac.uk and justin-prod-sched01.dune.hep.ac.uk
  included in defaults
- Event type IDs are generated using exec() from a list in __init__.py
- justin-check-db to be run when the justin-info-collector container starts
  and checks the event types in the code are also in the DB table event_types
- entry_has_gpus and always_has_gpus added to entries table in DB
- Add archived workflow pages
- Allow jobscripts to come from GitHub repos (DUNE/dist-comp#152)
- Automatic logs.tgz files created in 4m second per-RSE datasets which keep
  logs on the original RSE. Standalone justin-fetch-logs command added which
  uses Rucio client to fetch directly, and justin fetch-logs subcommand
  which fetches via justIN UI service without needing Rucio authentication
  (DUNE/dist-comp#137)
- Letsencrypt/certbot renewals done within justin-httpd container
  Files kept in /etc/justin-letsencrypt/ mounted from the host.
- Support for integration instance added
- MetaCat server URLs can now be set in the configuration
- MetaCat file info shown directly on justIN dashboard file pages

## 01.00.00
- The "1.0" release of justIN after DC24
