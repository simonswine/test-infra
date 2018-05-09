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
echo $TOOL_ROOT

# Create a tmpdir to build the docker images from.
NODE_DIR=$(mktemp -d)
echo "Building node docker image from ${NODE_DIR}"

# Get the startup scripts.
cp ${TOOL_ROOT}/init-wrapper.sh ${NODE_DIR}
cp ${TOOL_ROOT}/start.sh ${NODE_DIR}
cp ${TOOL_ROOT}/node/Dockerfile ${NODE_DIR}/Dockerfile
cp ${TOOL_ROOT}/node/Makefile ${NODE_DIR}/Makefile

K8S_VERSION=$1

docker pull k8s.gcr.io/kube-apiserver:v${K8S_VERSION}
docker pull k8s.gcr.io/kube-controller-manager:v${K8S_VERSION}
docker pull k8s.gcr.io/kube-scheduler:v${K8S_VERSION}
docker pull k8s.gcr.io/kube-proxy:v${K8S_VERSION}

docker save k8s.gcr.io/kube-apiserver:v${K8S_VERSION} > ${NODE_DIR}/kube-apiserver.tar
docker save k8s.gcr.io/kube-controller-manager:v${K8S_VERSION} > ${NODE_DIR}/kube-controller-manager.tar
docker save k8s.gcr.io/kube-scheduler:v${K8S_VERSION} > ${NODE_DIR}/kube-scheduler.tar
docker save k8s.gcr.io/kube-proxy:v${K8S_VERSION} > ${NODE_DIR}/kube-proxy.tar

# Create the dind-node container
cd ${NODE_DIR}
make build K8S_VERSION=$1
cd -
