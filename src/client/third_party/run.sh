#/bin/bash

root_dir=$(cd $(dirname $0) && pwd)

# setup port forwarding
adb forward tcp:1111 localabstract:minitouch
adb forward tcp:1313 localabstract:minicap
echo "port forwarding settled..."

# starting binary
cd "${root_dir}/minitouch"
./run.sh &

cd "${root_dir}/minicap"
./run.sh -P 1200x1920@960x600/90 &
