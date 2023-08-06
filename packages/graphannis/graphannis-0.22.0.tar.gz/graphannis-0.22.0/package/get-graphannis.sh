#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

if [ -z "$GRAPHANNIS_VERSION" ]; then
  # GRAPHANNIS_VERSION not set, but TRAVIS_TAG might be
  if [ -z "$TRAVIS_TAG" ]; then
    # also not set
    echo "Not a Travis deploy build"
  else
    # TRAVIS_TAG is set, set GRAPHANNIS_VERSION to its value
    GRAPHANNIS_VERSION=$TRAVIS_TAG
  fi
fi

if [ -z "$GRAPHANNIS_VERSION" ]; then
  # compile latest development
  mkdir "$DIR"/../ext/
  git clone https://github.com/korpling/graphANNIS "$DIR"/../ext/graphANNIS
  cd "$DIR"/../ext/graphANNIS
  cargo build --release --features "c-api"
  cp target/release/libgraphannis.so "$DIR"/../graphannis/linux-x86-64/
  cd "$DIR"/..
else
  # get released version
  echo "getting $GRAPHANNIS_VERSION"
  "$DIR"/download-release-binaries.sh "$GRAPHANNIS_VERSION"
fi
