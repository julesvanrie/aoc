#!/bin/bash

# trap "echo Some \(environment\) variable was missing. Exited" exit 1
[[ -z "$AOC_SESSION" ]] && echo -e "\e[0;31m Some (environment) variable was missing. Exited \e[0m" && exit 1

# Generate year and date if not provided as CLI argument
[[ $1 ]] && [[ $2 ]]   && DAY=$1 && YEAR=$2
[[ $1 ]] && [[ ! $2 ]] && DAY=$1 && YEAR=2022
[[ ! $1 ]]             && DAY=$(date +%-d) && YEAR=$(date +%Y)

URL=https://adventofcode.com/$YEAR/day/$DAY/answer

# Anser data - TODO work this out to retrieve it from env variable
LEVEL=1
ANSWER=52

# Generate cookie, data and headers
COOKIE="session=$AOC_SESSION"
DATA="level=$LEVEL&answer=$ANSWER"
HEADERS="User-Agent: https://github.com/julesvanrie/aoc/submit.sh by jules@vanrie.be"

# Post the answer and store the result
RESULT=$(curl -s -X POST $URL --cookie $COOKIE --header $HEADERS --data $DATA)

# Echo relevant message from the html file, or the whole result
if [[ "$RESULT" == *"<article>"* ]]; then
  awk '{ sub(/.*<article><p>/, ""); sub(/<a href.*/, ""); print $0 }' <<< $(awk '/<article>/ {print $0}' <<< $RESULT)
else
  echo $RESULT
fi
# echo curl $URL --cookie "$COOKIE" -H $HEADERS -d $DATA


# curl -X POST https://reqbin.com/echo/post/json \
# -H 'Content-Type: application/json' \
# -d '{"e-mail":"my_mail","password":"my_password"}'
