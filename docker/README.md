# justIN Docker

1. cd <YourFavouriteDirectory>
2. git checkout https://github.com/rajanandakumar/dune-justin.git
3. git pull (if needed)
4. cd dune-justin
5. Get the certificates directory ready (see below)
6. docker-compose -f docker/justin-infra.yaml -f docker/justin-agents.yaml build
7. docker-compose -f docker/justin-infra.yaml -f docker/justin-agents.yaml up -d

### Certificates directory

1. Make a certificates directory within the docker directory (mkdir docker/certificates)
2. Populate the directory with the following certificates (looks better in a simple text editor). Note that this is a simple dump of all the available certificates. The actual ones needed may be different. In particular, the subdirectory "wfs.dune.hep.ac.uk" below should actually correspond to the machine being set up.

certificates/
    ├── dune-vm.blackett.manchester.ac.uk.cert.pem
    ├── dune-vm.blackett.manchester.ac.uk.key.pem
    ├── justin-allocator.cert.pem
    ├── justin-allocator.key.pem
    ├── justin-allocator-pro.dune.hep.ac.uk.cert.pem
    ├── justin-allocator-pro.dune.hep.ac.uk.key.pem
    ├── justin.cert.pem
    ├── justin-dev.cert.pem
    ├── justin-dev.key.pem
    ├── justin-jobs-analysis.cert.pem
    ├── justin-jobs-analysis.dune.hep.ac.uk.cert.pem
    ├── justin-jobs-analysis.dune.hep.ac.uk.key.pem
    ├── justin-jobs-analysis.key.pem
    ├── justin-jobs-no-roles.cert.pem
    ├── justin-jobs-no-roles.dune.hep.ac.uk.cert.pem
    ├── justin-jobs-no-roles.dune.hep.ac.uk.key.pem
    ├── justin-jobs-no-roles.key.pem
    ├── justin-jobs-production.cert.pem
    ├── justin-jobs-production.dune.hep.ac.uk.cert.pem
    ├── justin-jobs-production.dune.hep.ac.uk.key.pem
    ├── justin-jobs-production.key.pem
    ├── justin.key.pem
    ├── justin-samweb-pro.dune.hep.ac.uk.cert.pem
    ├── justin-samweb-pro.dune.hep.ac.uk.key.pem
    ├── justin-ui.cert.pem
    ├── justin-ui.key.pem
    ├── justin-ui-pro.dune.hep.ac.uk.cert.pem
    ├── justin-ui-pro.dune.hep.ac.uk.key.pem
    ├── usercert.pem
    ├── userkey.pem
    ├── wfs-cert.pem
    ├── wfs.dune.hep.ac.uk
    │   ├── cert.pem
    │   ├── chain.pem
    │   ├── fullchain.pem
    │   ├── privkey.pem
    │   └── README
    ├── wfs.dune.hep.ac.uk.cert.pem
    ├── wfs.dune.hep.ac.uk.key.pem
    ├── wfs.dune.hep.ac.uk.tar.gz
    ├── wfs-key.pem
    ├── wfs-pro.dune.hep.ac.uk.cert.pem
    └── wfs-pro.dune.hep.ac.uk.key.pem

3. Decide whether to copy the certificates over (as currently in the docker/httpd/Dockerfile) or if you want to mount it within the docker-compose file (justin-infra.yaml). They are equivalent and both methods should work.
4. Then perform the build and bringing up of the containers.
