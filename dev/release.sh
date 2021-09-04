#! /bin/bash

set -exuo pipefail

VERSION="$1"
CHANGES="/tmp/pyperplan-$VERSION-changes"

function set_version {
    local version="$1"
    sed -i -e "s/VERSION = \".*\"/VERSION = \"$version\"/" setup.py
}

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

tox

set_version "$VERSION"
git commit -am "Update version number to ${VERSION} for release."
git tag -a "v$VERSION" -m "v$VERSION" HEAD

# Requirements:
#   pipx install twine
#   pip install --user wheel
python3 setup.py sdist bdist_wheel --universal
twine upload dist/pyperplan-${VERSION}.tar.gz dist/pyperplan-${VERSION}-py2.py3-none-any.whl

git push
git push --tags

# Add changelog to GitHub release.
./dev/make-release-notes.py "$VERSION" CHANGELOG.md "$CHANGES"
hub release create "v$VERSION" --file="$CHANGES"
