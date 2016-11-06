#!/bin/bash

rm -r splitsounds
mkdir -p splitsounds

for i in sounds/wav/*.wav; do
	fileid=$(basename "$i")
	fileid=${fileid%.wav}
	sox -V3 $i splitsounds/$fileid.wav silence 1 0.1 0.1% 1 0.30 0.1% : newfile : restart
done

# blacklist (not really sneezes)
cd splitsounds
rm -v sneeze.13770200[123456789].wav sneeze.137702011.wav sneeze.36657900[12].wav

# delete empty files
for i in *.wav; do
     LEN=$(sox "$i" -n stat 2>&1|grep "Length.*0\\.0000")
     if [[ -n "$LEN" ]]; then
        rm -v "$i"
    fi
done