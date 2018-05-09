#!/bin/bash

# Copyright 2018 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -o errexit
set -o nounset
set -o pipefail

TOOL_ROOT=${TOOL_ROOT:-"$(pwd)"}

# Create a tmpdir for the Docker build's context.
CLUSTER_DIR=$(mktemp -d)
echo "Building cluster docker image from ${CLUSTER_DIR}"

K8S_VERSION=$1

# Get systemd wrapper (needed until we put cluster-up into a systemd target).
cp ${TOOL_ROOT}/init-wrapper.sh ${CLUSTER_DIR}
# Get the cluster-up script.
cp ${TOOL_ROOT}/start.sh ${CLUSTER_DIR}

cp ${TOOL_ROOT}/cluster/Dockerfile ${CLUSTER_DIR}/Dockerfile
cp ${TOOL_ROOT}/cluster/Makefile ${CLUSTER_DIR}/Makefile

# Create the dind-cluster container
cd ${CLUSTER_DIR}
docker save eu.gcr.io/jetstack-build-infra/dind-node-amd64:${K8S_VERSION} -o dind-node-bundle.tar
make build K8S_VERSION=${K8S_VERSION}
cd -
