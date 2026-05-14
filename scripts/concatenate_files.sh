#!/bin/bash

# Concatenate files and display filenames at the top of each output.

if [ $# -eq 0 ]; then
  echo "Usage: $0 <file1> <file2> ..."
  echo "Example: $0 AVAS_JOURNAL.md entities/AVA_STONE.yml research/AVA_QUALIA_UNDERSTANDING.yml"
  exit 1
fi

for file in "$@"
do
  if [ -f "$file" ]; then
    echo "========================================================================"
    echo "File: $file"
    echo "========================================================================"
    cat "$file"
    echo ""
  else
    echo "File not found: $file"
  fi
done