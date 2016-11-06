#!/bin/bash
# download files similar to those in sneezes.txt

source load_credentials.sh

OUTFILE=similar_result.json

function all_ids() {
  grep "^https://" sneezes.txt | sed "s#.*/\([0-9]\+\)/.*#\1#g"
}

echo "[" > $OUTFILE
all_ids | while read i; do
  curl -s "https://www.freesound.org/apiv2/sounds/$i/similar/?token=$API_TOKEN&fields=id,name,description,duration" >> $OUTFILE
  echo "," >> $OUTFILE
done
echo "{}]" >> $OUTFILE

