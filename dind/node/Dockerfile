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

FROM eu.gcr.io/jetstack-build-infra/dind-test-base-amd64:0.1

# Addon config changes infrequently, so get them next.
# COPY cluster /

RUN curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && add-apt-repository \
    "deb [arch=amd64] http://apt.kubernetes.io \
    kubernetes-xenial \
    main"

ARG KUBE_VERSION
ENV KUBE_VERSION $KUBE_VERSION

RUN apt-get update \
    && apt-get install -y \
        kubelet=${KUBE_VERSION}-00 \
        kubeadm=${KUBE_VERSION}-00 \
        kubectl=${KUBE_VERSION}-00 \
        kubernetes-cni=0.6.0-00

# Install the binaries before getting the component images, because if they've
# changed, we're already redoing everything.

# kubernetes-cni.deb needs this dir
RUN mkdir -p /opt/cni/bin

# Get the component docker images last, because they're most likely to change.
COPY kube-proxy.tar /
COPY kube-controller-manager.tar /
COPY kube-scheduler.tar /
COPY kube-apiserver.tar /
RUN echo "$KUBE_VERSION" > /kube_version

# Get our short startup scripts first, because they're least likely to change.
COPY init-wrapper.sh /init-wrapper.sh
COPY start.sh /start.sh

ENTRYPOINT ["/init-wrapper.sh"]
