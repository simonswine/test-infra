# Jetstack specific test-infra docs

This document contains helpful information for managing the Jetstack test-infra deployment,
covering some common tasks.

## Adding an outside collaborator to an open-source project

In order for outside collaborators to interact with our bots without adding them to the main
'jetstack' organisation, a number of extra steps must be taken.

The example below is to add an external user (`@someone`) to cert-manager, in order to allow them
to `/close` issues/PRs as well as allowing them to test PRs without requiring an explicit `/ok-to-test`
each time from a Jetstack member.

### Add user to the 'cert-manager' organisation

As part of our Prow configuration, we have created a standalone (and empty) GitHub organisation named
[cert-manager](https://github.com/cert-manager).
Members of this organisation **do not require** `/ok-to-test` when submitting PRs against the main
[jetstack/cert-manager](https://github.com/jetstack/cert-manager) repostiory.

In order to do this, invite `@someone` to the [cert-manager](https://github.com/cert-manager) organisation on
GitHub as a **regular member** (not owner).

The user should no longer have their PRs labelled `needs-ok-to-test` when created.

### Add user to the 'cert-manager' repo

Large parts of Prow depend on being able to **assign** a user to a PR/issue in order for them to interact
with it, e.g. `/close`.

On GitHub, it is only possible for a user to be assigned to an issue if they are a member of the repo or
organisation in question.

As we are not able to add users to the main Jetstack org, we can instead add the user to the **repo** as a
**read-only collaborator**.

> **PLEASE NOTE**: It is **absolutely essential** that you add the user as a **read-only** collaborator, else
the user will have **full** permission to modify any release/branch of the project! This is **VERY IMPORTANT** to
get right.

Unfortunately, GitHub does **not** provide any mechanism via the web UI to add a user as a read-only collaborator to
a repo.

Instead, you can achieve the same thing with a `curl` command like follows:

```
curl -H "Authorization: token {auth-token}" \
  -d '{"permission":"pull"}' \
  -XPUT \
  https://api.github.com/repos/jetstack/cert-manager/collaborators/someone
```

You will need to replace `{auth-token}` with an authentication token with suitable privileges to perform the operation
(i.e. you will need to yourself be an owner of the cert-manager repo, or use a bot token that is)
