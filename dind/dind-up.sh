#!/bin/bash

# Copyright 2017 The Kubernetes Authors.
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

K8S_VERSION=$1

CONTAINER=$(docker run -d --privileged=true --security-opt seccomp:unconfined --cap-add=SYS_ADMIN \
  -p 6443:443 -v $(pwd)/kubedir:/var/kubernetes -v /lib/modules:/lib/modules -v /sys/fs/cgroup:/sys/fs/cgroup:ro \
  eu.gcr.io/jetstack-build-infra/dind-cluster-amd64:${K8S_VERSION})
echo "The cluster lives in container ${CONTAINER}"
