#!/bin/sh
# DSM manual task: does not create a container, DB, credential or port.
set -eu
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
export PATH
docker pull postgres:17-bookworm
docker image inspect --format '{{index .RepoDigests 0}}' postgres:17-bookworm
