#!/bin/bash
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo run $SCRIPTPATH
python3 $SCRIPTPATH/IotServer.py  > /dev/null &
