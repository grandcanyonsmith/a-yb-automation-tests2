#!/bin/bash

if [ -z "$APP_PATH" ]; then
  echo You need to pass in APP_PATH
  exit 1
else
  pytest "tests/$APP_TAG"
  export RESULT=$?
fi

echo $RESULT
kill $NODE_PID
exit $RESULT
