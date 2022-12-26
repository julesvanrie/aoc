#!/bin/bash

# Determine new folder based on input arguments
if [ $1 ]; then
  NEW_DIR=$1
else
  NEW_DIR=$(date +%d)
fi

# Create new dir
if [ -d "$NEW_DIR" ]; then
  echo "Folder '$NEW_DIR' exists already"
else
  mkdir "$NEW_DIR"
  echo "Folder '$NEW_DIR' created"
fi

# Clone boilerplate
if [ -e "$NEW_DIR/solve.py" ]; then
  echo "File '$NEW_DIR/solve.py' exists already"
else
  cp boilerplate.py "$NEW_DIR/solve.py"
  echo "File '$NEW_DIR/solve.py' created"
fi

# Test file
if [ -e "$NEW_DIR/test.txt" ]; then
  echo "File '$NEW_DIR/test.txt' exists already"
else
  touch "$NEW_DIR/test.txt"
  echo "File '$NEW_DIR/test.txt' created"
fi

# Done
echo "Finished"
