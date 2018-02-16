#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
python3 $SCRIPTPATH/IotServer.py  > /dev/null &
