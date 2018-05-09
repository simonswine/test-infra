# cert-manager-test

This image defines an environment for running cert-manager unit and integration
tests.

This is primarily used by the pull-cert-manager-verify job.

We provide a build image per minor version, to allow for divergences in the build
process when maintaining old branches.
