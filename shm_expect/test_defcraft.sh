#!/bin/bash

if [[ $# -ne 3 ]]
then
  echo "Usage: $(basename $0) [ShM] [USERNAME] [PASSWORD]"
  exit 1
fi

DIR="`dirname $0`"
SHM=$1
USERNAME=$2
PASSWORD=$3

echo "Starting test_defcraft on ${SHM}"
timeout 1m expect ${DIR}/test_defcraft.exp ${SHM} ${USERNAME} ${PASSWORD}
if [[ $? -eq 124 ]]
then
  echo "test_defcraft failed"
  exit 1
fi

exit 0
