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

# This file creates a build environment for building and running kubernetes
# unit and integration tests

ARG KUBE_VERSION

FROM eu.gcr.io/jetstack-build-infra/dind-cluster-amd64:${KUBE_VERSION}
LABEL authors="James Munnelly <james@jetstack.io>"

# Setup workspace and symlink to gopath
RUN mkdir -p /workspace
WORKDIR /workspace
ENV WORKSPACE=/workspace \
    TERM=xterm

##### Start installing prow utilities
# common util tools
# https://github.com/GoogleCloudPlatform/gsutil/issues/446 for python-openssl
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    file \
    git \
    jq \
    openssh-client \
    pkg-config \
    python \
    python-dev \
    python-openssl \
    python-pip \
    rsync \
    unzip \
    wget \
    xz-utils \
    zip \
    zlib1g-dev \
    && apt-get clean \
    && python -m pip install --upgrade pip setuptools wheel

# Install gcloud
ENV PATH=/google-cloud-sdk/bin:/workspace:${PATH} \
    CLOUDSDK_CORE_DISABLE_PROMPTS=1

RUN wget -q https://dl.google.com/dl/cloudsdk/channels/rapid/google-cloud-sdk.tar.gz && \
    tar xzf google-cloud-sdk.tar.gz -C / && \
    rm google-cloud-sdk.tar.gz && \
    /google-cloud-sdk/install.sh \
        --disable-installation-options \
        --bash-completion=false \
        --path-update=false \
        --usage-reporting=false && \
    gcloud components install alpha beta kubectl && \
    gcloud info | tee /workspace/gcloud-info.txt
######### End installing Prow utilities

ADD ["runner", \
    "/workspace/"]

# add env we can debug with the image name:tag
ARG IMAGE_ARG
ENV IMAGE=${IMAGE_ARG}

ENTRYPOINT ["/workspace/runner"]
