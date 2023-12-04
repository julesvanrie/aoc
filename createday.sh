#!/bin/bash

# Determine new folder based on input arguments
if [ $1 ]; then
  NEW_DIR=day$1
else
  NEW_DIR=day$(date +%d)
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
  cp ../boilerplate.py "$NEW_DIR/solve.py"
  echo "File '$NEW_DIR/solve.py' created"
fi

# Test file
if [ -e "$NEW_DIR/test_one.txt" ]; then
  echo "File '$NEW_DIR/test_one.txt' exists already"
else
  touch "$NEW_DIR/test_one.txt"
  echo "File '$NEW_DIR/test_one.txt' created"
fi

# Test file
if [ -e "$NEW_DIR/test_two.txt" ]; then
  echo "File '$NEW_DIR/test_two.txt' exists already"
else
  touch "$NEW_DIR/test_two.txt"
  echo "File '$NEW_DIR/test_two.txt' created"
fi

# Done
echo "Finished"
