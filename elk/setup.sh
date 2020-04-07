#!/bin/bash
#
# related doc: https://elk-docker.readthedocs.io/

# change setting for elastic search
# run this or add to /etc/sysctl.conf
sysctl -w vm.max_map_count=262144
