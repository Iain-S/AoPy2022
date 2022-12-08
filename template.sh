#!/bin/bash

set -o errexit
set -o nounset

DAY=$1

cp "src/template.py" "src/day$DAY.py"
sed -i "" "s/THE_DAY/$DAY/g" "src/day$DAY.py"

cp "tests/template.py" "tests/test_day$DAY.py"
sed -i "" "s/THE_DAY/$DAY/g" "tests/day$DAY.py"

touch "examples/day$DAY.txt"
mkdir -p "inputs/day$DAY.txt"