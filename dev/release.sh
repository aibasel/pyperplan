#! /bin/bash

set -exuo pipefail

VERSION="$1"
CHANGES="/tmp/pyperplan-$VERSION-changes"

cd $(dirname "$0")/../

# Check for uncommited changes.
set +e
git diff --quiet && git diff --cached --quiet
retcode=$?
set -e
if [[ $retcode != 0 ]]; then
    echo "There are uncommited changes:"
    git status
    exit 1
fi

if [[ $(git rev-parse --abbrev-ref HEAD) != master ]]; then
    echo "Must be on master for release"
    exit 1
fi

git tag -a "v$VERSION" -m "v$VERSION" HEAD

git push
git push --tags

# Add changelog to Github release.
./dev/make-release-notes.py "$VERSION" CHANGELOG.md "$CHANGES"
hub release create "v$VERSION" --file "$CHANGES"
