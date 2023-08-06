#!/usr/bin/env bash
set -e

VERSION=`python -c "exec(open('pybindcpp/version.py', 'r').read()); print(__version__)"`
echo v$VERSION

git tag v$VERSION
git push
git push --tags
python setup.py sdist
twine upload dist/*${VERSION}*
