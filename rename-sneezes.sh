#!/bin/bash
# rename files containing sneeze to sneeze.id.mp3

source load_credentials.sh

function all_ids() {
  grep "^https://" sneezes.txt | sed "s#.*/\([0-9]\+\)/.*#\1#g"
}

all_ids | while read i; do
  if [[ -f "sounds/$i.mp3" ]]; then
    mv "sounds/$i.mp3" "sounds/sneeze.$i.mp3"
  fi
done

