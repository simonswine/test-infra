#!/usr/bin/env python

# Copyright 2018 Jetstack Ltd.
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

# pylint: disable=bad-continuation

"""Runs verify/test-go checks for jetstack/cert-manager."""

import argparse
import os
import re
import subprocess
import sys
import socket

BRANCH_VERSION = {
    'master': '0.3',
}

VERSION_TAG = {
    '0.3': '0.3-v20180510-6dc7d4e5d',
}

def check_output(*cmd):
    """Log and run the command, return output, raising on errors."""
    print >>sys.stderr, 'Run:', cmd
    return subprocess.check_output(cmd)


def check(*cmd):
    """Log and run the command, raising on errors."""
    print >>sys.stderr, 'Run:', cmd
    subprocess.check_call(cmd)


def retry(func, times=5):
    """call func until it returns true at most times times"""
    success = False
    for _ in range(0, times):
        success = func()
        if success:
            return success
    return success


def try_call(cmds):
    """returns true if check(cmd) does not throw an exception
    over all cmds where cmds = [[cmd, arg, arg2], [cmd2, arg]]"""
    try:
        for cmd in cmds:
            check(*cmd)
        return True
    # pylint: disable=bare-except
    except:
        return False

def start_node(master, ip):
    node_image="eu.gcr.io/jetstack-build-infra/dind-node-amd64:1.10.2"
    cmd = [
        'docker', 'run', '-d', '--privileged',
        '--net', 'testnet',
        '--ip', ip,
        '-v', '/image-loader:/image-loader',
        '-v', '/lib/modules:/lib/modules',
    ]
    if master:
        cmd.extend([
            '-p', '443:6443',
            '-v', '/etc/kubernetes:/etc/kubernetes',
        ])
    cmd.extend([node_image])
    if master:
        hostname = socket.gethostbyname(socket.gethostname())
        cmd.extend(['master', hostname])
    else:
        cmd.extend(['worker'])
    check(*cmd)

def start_cluster():
    check('mount', '-o', 'remount,ro', '/sys')
    check('mount', '--make-rshared', '/lib/modules')
    check('mount', '--make-rshared', '/')
    check('mkdir', '-p', '/etc/kubernetes')
    check('docker', 'network', 'create', '--subnet=10.14.0.0/24', 'testnet')
    check('docker', 'network', 'ls')
    start_node(True, '10.14.0.20')
    start_node(False, '10.14.0.21')
    start_node(False, '10.14.0.22')
    start_node(False, '10.14.0.23')


def main(branch, script, force):
    """Test branch using script, optionally forcing verify checks."""
    # If branch has 3-part version, only take first 2 parts.
    verify_branch = re.match(r'master|release-(\d+\.\d+)', branch)
    if not verify_branch:
        raise ValueError(branch)
    # Extract version if any.
    ver = verify_branch.group(1) or verify_branch.group(0)
    tag = VERSION_TAG[BRANCH_VERSION.get(ver, ver)]
    force = 'y' if force else 'n'
    artifacts = '%s/_artifacts' % os.environ['WORKSPACE']
    k8s = os.getcwd()
    if not os.path.basename(k8s) == 'cert-manager':
        raise ValueError(k8s)

    check('rm', '-rf', '.gsutil')
    remote = 'bootstrap-upstream'
    uri = 'https://github.com/jetstack/cert-manager.git'

    current_remotes = check_output('git', 'remote')
    if re.search('^%s$' % remote, current_remotes, flags=re.MULTILINE):
        check('git', 'remote', 'remove', remote)
    check('git', 'remote', 'add', remote, uri)
    check('git', 'remote', 'set-url', '--push', remote, 'no_push')
    # If .git is cached between runs this data may be stale
    check('git', 'fetch', remote)

    if not os.path.isdir(artifacts):
        os.makedirs(artifacts)

    ###### Start dind cluster
    start_cluster()
    ###### End dind cluster

    cmd = [
        'docker', 'run', '--rm=true', '--privileged=true',
        '--net', 'testnet',
        '-v', '/var/run/docker.sock:/var/run/docker.sock',
        '-v', '/etc/localtime:/etc/localtime:ro',
        '-v', '/etc/kubernetes:/etc/kubernetes',
        '-v', '/image-loader:/image-loader',
        '-v', '%s:/go/src/github.com/jetstack/cert-manager' % k8s,
        '-v', '%s:/workspace/artifacts' % artifacts,
        '-e', 'KUBE_FORCE_VERIFY_CHECKS=%s' % force,
        '-e', 'KUBECONFIG=/etc/kubernetes/admin.conf',
        '--tmpfs', '/tmp:exec,mode=1777',
        'eu.gcr.io/jetstack-build-infra/cert-manager-test:%s' % tag,
        'bash', '-c', 'cd cert-manager && %s' % script,
    ]
    check(*cmd)



if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        'Runs verification checks on the cert-manager repo')
    PARSER.add_argument(
        '--branch', default='master', help='Upstream target repo')
    PARSER.add_argument(
        '--force', action='store_true', help='Force all verify checks')
    PARSER.add_argument(
        '--script',
        default='./hack/ci/test-dockerized.sh',
        help='Script in jetstack/cert-manager that runs checks')
    ARGS = PARSER.parse_args()
    main(ARGS.branch, ARGS.script, ARGS.force)
