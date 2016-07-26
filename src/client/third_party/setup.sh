#!/bin/bash

root_dir=$(cd $(dirname $0) && pwd)

# setup minitouch
cd $root_dir
pwd
echo "Installing minitouch start"
git clone git@github.com:openstf/minitouch.git
cd minitouch
git submodule init
git submodule update
ndk-build

# setup minicap
cd $root_dir
pwd
echo "Installing minicap start"
git clone git@github.com:openstf/minicap.git
cd minicap
git submodule init
git submodule update
ndk-build