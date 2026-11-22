#!/bin/zsh
# Reruns the triage-bug eval kit (NightJar lesson/test-it-again) on three models,
# 5 evals x 2 configurations x 3 runs each, six at a time. Results: material/results/<model>/
H=${0:A:h}; KIT=${KIT:?set KIT to the NightJar checkout on lesson/test-it-again}
for m in claude-sonnet-5-5 claude-haiku-5-5 claude-opus-5-5; do
  for e in 1 2 3 4 5; do for c in with_skill without_skill; do for n in 1 2 3; do
    echo "$m $e $c $n"; done; done; done
done | xargs -P 6 -L 1 zsh -c 'cd $0 && MODEL=$1 zsh skill-tests/triage-bug/run.sh $2 $3 $4 '$H'/results/$1' $KIT
