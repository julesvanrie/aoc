#!/bin/bash

# trap "echo Some \(environment\) variable was missing. Exited" exit 1
[[ -z "$AOC_SESSION" ]] && echo -e "\e[0;31m Some (environment) variable was missing. Exited \e[0m" && exit 1

# Generate year and date if not provided as CLI argument
[[ $1 ]] && [[ $2 ]]   && DAY=$1 && YEAR=$2
[[ $1 ]] && [[ ! $2 ]] && DAY=$1 && YEAR=2022
[[ ! $1 ]]             && DAY=$(date +%-d) && YEAR=$(date +%Y)

URL=https://adventofcode.com/$YEAR/day/$DAY/input

# Generate cookie, data and headers
COOKIE="session=$AOC_SESSION"
HEADERS="User-Agent: https://github.com/julesvanrie/aoc/input.sh by jules@vanrie.be"

# Post the answer and store the result
ZEROS=00
curl $URL --cookie $COOKIE --header "$HEADERS" > day${ZEROS:${#DAY}}$DAY/input.txt
