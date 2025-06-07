#! /usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

COOKIECUTTER_DIR=$1
TEST_DIR=$(mktemp -d)
cookiecutter --no-input -o "$TEST_DIR" "$COOKIECUTTER_DIR"
pushd "$TEST_DIR/projectname"
tox
popd
rm -rf "$TEST_DIR"
