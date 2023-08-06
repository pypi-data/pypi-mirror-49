
Initial init

  $ code_root=`dirname $TESTDIR`

  $ cat >> json_format.py <<EOF
  > """ Auto-format the JSON file passed as a command-line argument and output
  > the formatted code in stdout
  > """
  > from __future__ import print_function
  > import sys
  > import json
  > with open(sys.argv[1], 'rb') as infile:
  >     obj = json.load(infile)
  > with sys.stdout:
  >     json.dump(obj, sys.stdout, sort_keys=True, indent=4, separators=(',', ': '))
  >     sys.stdout.write("\n")
  > EOF

  $ cat << EOF >> $HGRCPATH
  > [extensions]
  > formatsource=${code_root}/hgext3rd/formatsource.py
  > rebase =
  > strip =
  > [format-source]
  > json = python $TESTTMP/json_format.py
  > json:mode.input = file
  > json:mode.output = pipe
  > [default]
  > format-source=--date '0 0'
  > [ui]
  > merge=:merge3
  > EOF
  $ HGMERGE=:merge3



  $ cat << EOF > root-file-orig.json
  > {"key1": 1, "key2": [5,6,7,8],
  > "key3":
  > ["arthur", "babar", "celeste"]}
  > EOF
  $ cat << EOF > root-file-blue.json
  > {"key1": 2, "key2": [5,6,7,8],
  > "key3":
  > ["arthur", "babar", "celeste"]}
  > EOF
  $ cat << EOF > root-file-red.json
  > {"key1": 1, "key2": [5,6,7,8],
  > "key3":
  > ["Arthur", "Babar", "Celeste"]}
  > EOF

Commit various json file

  $ hg init test_repo
  $ cd test_repo
  $ cp ../root-file-orig.json root-file.json

(file used to easily trigger commits)

  $ echo > base
  $ hg add .
  adding base
  adding root-file.json
  $ hg commit --message 'initial commit'

  $ echo a > base
  $ hg ci -m 'no-base'

  $ cp ../root-file-blue.json root-file.json
  $ hg ci -m 'no-no-blue'

  $ hg up 'desc("no-base")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cp ../root-file-red.json root-file.json
  $ hg ci -m 'no-no-red'
  created new head

  $ hg up 'desc("no-base")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg format-source json root-file.json -m "no-yes-red"
  created new head

  $ hg up 'desc("no-base")'
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg format-source json root-file.json -m "no-yes-blue"
  created new head

  $ hg up 'desc("initial commit")'
  2 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg format-source json root-file.json -m "yes-base"
  created new head

  $ python $TESTTMP/json_format.py ../root-file-blue.json > root-file.json
  $ hg ci -m 'yes-yes-blue'

  $ hg up 'desc("yes-base")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ python $TESTTMP/json_format.py ../root-file-red.json > root-file.json
  $ hg ci -m 'yes-yes-red'
  created new head

  $ hg up 'desc("yes-base")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cp ../root-file-blue.json root-file.json
  $ hg ci -m 'yes-no-blue'
  created new head

  $ hg up 'desc("yes-base")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cp ../root-file-red.json root-file.json
  $ hg ci -m 'yes-no-red'
  created new head

  $ hg log -Gp
  @  changeset:   10:85df8cb5bb73
  |  tag:         tip
  |  parent:      6:d7c617ed603e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     yes-no-red
  |
  |  diff -r d7c617ed603e -r 85df8cb5bb73 root-file.json
  |  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -1,14 +1,3 @@
  |  -{
  |  -    "key1": 1,
  |  -    "key2": [
  |  -        5,
  |  -        6,
  |  -        7,
  |  -        8
  |  -    ],
  |  -    "key3": [
  |  -        "arthur",
  |  -        "babar",
  |  -        "celeste"
  |  -    ]
  |  -}
  |  +{"key1": 1, "key2": [5,6,7,8],
  |  +"key3":
  |  +["Arthur", "Babar", "Celeste"]}
  |
  | o  changeset:   9:58b0442845f1
  |/   parent:      6:d7c617ed603e
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    summary:     yes-no-blue
  |
  |    diff -r d7c617ed603e -r 58b0442845f1 root-file.json
  |    --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -1,14 +1,3 @@
  |    -{
  |    -    "key1": 1,
  |    -    "key2": [
  |    -        5,
  |    -        6,
  |    -        7,
  |    -        8
  |    -    ],
  |    -    "key3": [
  |    -        "arthur",
  |    -        "babar",
  |    -        "celeste"
  |    -    ]
  |    -}
  |    +{"key1": 2, "key2": [5,6,7,8],
  |    +"key3":
  |    +["arthur", "babar", "celeste"]}
  |
  | o  changeset:   8:c7d2aef56535
  |/   parent:      6:d7c617ed603e
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    summary:     yes-yes-red
  |
  |    diff -r d7c617ed603e -r c7d2aef56535 root-file.json
  |    --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -7,8 +7,8 @@
  |             8
  |         ],
  |         "key3": [
  |    -        "arthur",
  |    -        "babar",
  |    -        "celeste"
  |    +        "Arthur",
  |    +        "Babar",
  |    +        "Celeste"
  |         ]
  |     }
  |
  | o  changeset:   7:31a4db03d8a8
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    summary:     yes-yes-blue
  |
  |    diff -r d7c617ed603e -r 31a4db03d8a8 root-file.json
  |    --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -1,5 +1,5 @@
  |     {
  |    -    "key1": 1,
  |    +    "key1": 2,
  |         "key2": [
  |             5,
  |             6,
  |
  o  changeset:   6:d7c617ed603e
  |  parent:      0:bdc543ba98a9
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     yes-base
  |
  |  diff -r bdc543ba98a9 -r d7c617ed603e .hg-format-source
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +{"pattern": "root-file.json", "tool": "json"}
  |  diff -r bdc543ba98a9 -r d7c617ed603e root-file.json
  |  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -1,3 +1,14 @@
  |  -{"key1": 1, "key2": [5,6,7,8],
  |  -"key3":
  |  -["arthur", "babar", "celeste"]}
  |  +{
  |  +    "key1": 1,
  |  +    "key2": [
  |  +        5,
  |  +        6,
  |  +        7,
  |  +        8
  |  +    ],
  |  +    "key3": [
  |  +        "arthur",
  |  +        "babar",
  |  +        "celeste"
  |  +    ]
  |  +}
  |
  | o  changeset:   5:a2cc62ad2293
  | |  parent:      1:a2239f50a527
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     no-yes-blue
  | |
  | |  diff -r a2239f50a527 -r a2cc62ad2293 .hg-format-source
  | |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  | |  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  | |  @@ -0,0 +1,1 @@
  | |  +{"pattern": "root-file.json", "tool": "json"}
  | |  diff -r a2239f50a527 -r a2cc62ad2293 root-file.json
  | |  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  | |  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  | |  @@ -1,3 +1,14 @@
  | |  -{"key1": 1, "key2": [5,6,7,8],
  | |  -"key3":
  | |  -["arthur", "babar", "celeste"]}
  | |  +{
  | |  +    "key1": 1,
  | |  +    "key2": [
  | |  +        5,
  | |  +        6,
  | |  +        7,
  | |  +        8
  | |  +    ],
  | |  +    "key3": [
  | |  +        "arthur",
  | |  +        "babar",
  | |  +        "celeste"
  | |  +    ]
  | |  +}
  | |
  | | o  changeset:   4:39dba2715eea
  | |/   parent:      1:a2239f50a527
  | |    user:        test
  | |    date:        Thu Jan 01 00:00:00 1970 +0000
  | |    summary:     no-yes-red
  | |
  | |    diff -r a2239f50a527 -r 39dba2715eea .hg-format-source
  | |    --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  | |    +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  | |    @@ -0,0 +1,1 @@
  | |    +{"pattern": "root-file.json", "tool": "json"}
  | |    diff -r a2239f50a527 -r 39dba2715eea root-file.json
  | |    --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  | |    +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  | |    @@ -1,3 +1,14 @@
  | |    -{"key1": 1, "key2": [5,6,7,8],
  | |    -"key3":
  | |    -["arthur", "babar", "celeste"]}
  | |    +{
  | |    +    "key1": 1,
  | |    +    "key2": [
  | |    +        5,
  | |    +        6,
  | |    +        7,
  | |    +        8
  | |    +    ],
  | |    +    "key3": [
  | |    +        "arthur",
  | |    +        "babar",
  | |    +        "celeste"
  | |    +    ]
  | |    +}
  | |
  | | o  changeset:   3:4c299cd93463
  | |/   parent:      1:a2239f50a527
  | |    user:        test
  | |    date:        Thu Jan 01 00:00:00 1970 +0000
  | |    summary:     no-no-red
  | |
  | |    diff -r a2239f50a527 -r 4c299cd93463 root-file.json
  | |    --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  | |    +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  | |    @@ -1,3 +1,3 @@
  | |     {"key1": 1, "key2": [5,6,7,8],
  | |     "key3":
  | |    -["arthur", "babar", "celeste"]}
  | |    +["Arthur", "Babar", "Celeste"]}
  | |
  | | o  changeset:   2:06d61003dc5c
  | |/   user:        test
  | |    date:        Thu Jan 01 00:00:00 1970 +0000
  | |    summary:     no-no-blue
  | |
  | |    diff -r a2239f50a527 -r 06d61003dc5c root-file.json
  | |    --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  | |    +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  | |    @@ -1,3 +1,3 @@
  | |    -{"key1": 1, "key2": [5,6,7,8],
  | |    +{"key1": 2, "key2": [5,6,7,8],
  | |     "key3":
  | |     ["arthur", "babar", "celeste"]}
  | |
  | o  changeset:   1:a2239f50a527
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    summary:     no-base
  |
  |    diff -r bdc543ba98a9 -r a2239f50a527 base
  |    --- a/base	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/base	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -1,1 +1,1 @@
  |    -
  |    +a
  |
  o  changeset:   0:bdc543ba98a9
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     initial commit
  
     diff -r 000000000000 -r bdc543ba98a9 base
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/base	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,1 @@
     +
     diff -r 000000000000 -r bdc543ba98a9 root-file.json
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,3 @@
     +{"key1": 1, "key2": [5,6,7,8],
     +"key3":
     +["arthur", "babar", "celeste"]}
  

Test the behavior of the merge
==============================

Merging not involving format-source at all
------------------------------------------

normal run should not involve format source and merge fine

  $ hg up -C 'desc("no-no-blue")'
  2 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg merge 'desc("no-no-red")'
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

run-mode=auto should be a normal run

  $ hg up -C 'desc("no-no-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("no-no-red")' --config format-source.run-mode=auto
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

run-mode=off should no involve format source and merge fine

  $ hg up -C 'desc("no-no-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("no-no-red")' --config format-source.run-mode=off
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

run-mode=on should no involve format source and merge fine
(since these file are not formatted at all)

  $ hg up -C 'desc("no-no-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("no-no-red")' --config format-source.run-mode=on
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)


Merging with format source on the local side only
-------------------------------------------------

normal run should involve format source and merge fine

  $ hg up -C 'desc("no-yes-blue")'
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("no-no-red")'
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

run-mode=auto should be the same as a normal run

  $ hg up -C 'desc("no-yes-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("no-no-red")' --config format-source.run-mode=auto
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

run-mode=off skips the formatter and will to conflicts

  $ hg up -C 'desc("no-yes-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("no-no-red")' --config format-source.run-mode=off
  merging root-file.json
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges or 'hg merge --abort' to abandon
  [1]

run-mode=on will use the formatter

  $ hg up -C 'desc("no-yes-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("no-no-red")' --config format-source.run-mode=on
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

Merging with format source on the other side only
-------------------------------------------------

normal run should involve format source and merge fine

  $ hg up -C 'desc("no-no-blue")'
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg merge 'desc("no-yes-red")'
  merging root-file.json
  1 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

run-mode=off skips the formatter and will lead to conflicts

  $ hg up -C 'desc("no-no-blue")'
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg merge 'desc("no-yes-red")' --config format-source.run-mode=off
  merging root-file.json
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  1 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges or 'hg merge --abort' to abandon
  [1]

run-mode=on

  $ hg up -C 'desc("no-no-blue")'
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg merge 'desc("no-yes-red")' --config format-source.run-mode=on
  merging root-file.json
  1 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

Merging with format source on both side
---------------------------------------

normal run should involve format source and merge fine

  $ hg up -C 'desc("no-yes-blue")'
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("no-yes-red")'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

run-mode=off skip the formatting and lead to conflicts
(even if both local and remote are formatted, the base is not and the change
tracking can't make ssense of the changes on each side).

  $ hg up -C 'desc("no-no-blue")'
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg merge 'desc("no-yes-red")' --config format-source.run-mode=off
  merging root-file.json
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  1 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges or 'hg merge --abort' to abandon
  [1]

run-mode=on

  $ hg up -C 'desc("no-no-blue")'
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg merge 'desc("no-yes-red")' --config format-source.run-mode=on
  merging root-file.json
  1 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

Merging with format source "rolled back" on both side
-----------------------------------------------------

normal run should merge fine
(format source is not involved but "rolling back" is a bit of a grey area)

  $ hg up -C 'desc("yes-no-blue")'
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-no-red")'
  merging root-file.json
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges or 'hg merge --abort' to abandon
  [1]

run-mode=off have no effect since the formatter was already not running.

  $ hg up -C 'desc("yes-no-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-no-red")' --config format-source.run-mode=off
  merging root-file.json
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges or 'hg merge --abort' to abandon
  [1]

run-mode=on force the formatter to run and the "fix" the rollback.

  $ hg up -C 'desc("yes-no-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-no-red")' --config format-source.run-mode=on
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

Merging with format source "rolled back" on the remote side
-----------------------------------------------------------

normal run should raise conflict
(format source is not involved but "rolling back" is a bit of a grey area)

  $ hg up -C 'desc("yes-yes-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-no-red")'
  merging root-file.json
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges or 'hg merge --abort' to abandon
  [1]

run-mode=off have no effect since the formatter was already not running.

  $ hg up -C 'desc("yes-no-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-no-red")' --config format-source.run-mode=off
  merging root-file.json
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges or 'hg merge --abort' to abandon
  [1]

run-mode=on force the formatter to run and the "fix" the rollback.

  $ hg up -C 'desc("yes-no-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-no-red")' --config format-source.run-mode=on
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

Merging with format source "rolled back" on the local side
----------------------------------------------------------

normal run should raise conflict
(format source is not involved but "rolling back" is a bit of a grey area)

  $ hg up -C 'desc("yes-no-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-yes-red")'
  merging root-file.json
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges or 'hg merge --abort' to abandon
  [1]

run-mode=off have no effect since the formatter was already not running.

  $ hg up -C 'desc("yes-no-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-yes-red")' --config format-source.run-mode=off
  merging root-file.json
  warning: conflicts while merging root-file.json! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  use 'hg resolve' to retry unresolved file merges or 'hg merge --abort' to abandon
  [1]

run-mode=on force the formatter to run and the "fix" the rollback.

  $ hg up -C 'desc("yes-no-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-yes-red")' --config format-source.run-mode=on
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

Merging with format source used on both side
--------------------------------------------

normal run should work fine
format source is not involved since the formatting did not changed.

  $ hg up -C 'desc("yes-yes-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-yes-red")' --debug
  resolving manifests
   branchmerge: True, force: False, partial: False
   ancestor: d7c617ed603e, local: 31a4db03d8a8+, remote: c7d2aef56535
   preserving root-file.json for resolve of root-file.json
   root-file.json: versions differ -> m (premerge)
  picked tool ':merge3' for root-file.json (binary False symlink False changedelete False)
  merging root-file.json
  my root-file.json@31a4db03d8a8+ other root-file.json@c7d2aef56535 ancestor root-file.json@d7c617ed603e
   premerge successful
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)


run-mode=auto should be the same as normal run

  $ hg up -C 'desc("yes-yes-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-yes-red")' --config format-source.run-mode=auto --debug
  resolving manifests
   branchmerge: True, force: False, partial: False
   ancestor: d7c617ed603e, local: 31a4db03d8a8+, remote: c7d2aef56535
   preserving root-file.json for resolve of root-file.json
   root-file.json: versions differ -> m (premerge)
  picked tool ':merge3' for root-file.json (binary False symlink False changedelete False)
  merging root-file.json
  my root-file.json@31a4db03d8a8+ other root-file.json@c7d2aef56535 ancestor root-file.json@d7c617ed603e
   premerge successful
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

run-mode=off get the same result at the normal run since the formatter was already skipped
(both side are already detected as formatted)

  $ hg up -C 'desc("yes-yes-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-yes-red")' --config format-source.run-mode=off --debug
  resolving manifests
   branchmerge: True, force: False, partial: False
   ancestor: d7c617ed603e, local: 31a4db03d8a8+, remote: c7d2aef56535
   preserving root-file.json for resolve of root-file.json
   root-file.json: versions differ -> m (premerge)
  picked tool ':merge3' for root-file.json (binary False symlink False changedelete False)
  merging root-file.json
  my root-file.json@31a4db03d8a8+ other root-file.json@c7d2aef56535 ancestor root-file.json@d7c617ed603e
   premerge successful
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg diff
  diff -r 31a4db03d8a8 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -7,8 +7,8 @@
           8
       ],
       "key3": [
  -        "arthur",
  -        "babar",
  -        "celeste"
  +        "Arthur",
  +        "Babar",
  +        "Celeste"
       ]
   }

run-mode=on ran the formatter, which was a no-op since the file are already formatted

  $ hg up -C 'desc("yes-yes-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-yes-red")' --config format-source.run-mode=on --debug
  resolving manifests
   branchmerge: True, force: False, partial: False
   ancestor: d7c617ed603e, local: 31a4db03d8a8+, remote: c7d2aef56535
   preserving root-file.json for resolve of root-file.json
   root-file.json: versions differ -> m (premerge)
  running python $TESTTMP/json_format.py * (glob)
  running python $TESTTMP/json_format.py * (glob)
  running python $TESTTMP/json_format.py * (glob)
  picked tool ':merge3' for root-file.json (binary False symlink False changedelete False)
  merging root-file.json
  my root-file.json@31a4db03d8a8+ other root-file.json@c7d2aef56535 ancestor root-file.json@d7c617ed603e
   premerge successful
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg diff
  diff -r 31a4db03d8a8 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -7,8 +7,8 @@
           8
       ],
       "key3": [
  -        "arthur",
  -        "babar",
  -        "celeste"
  +        "Arthur",
  +        "Babar",
  +        "Celeste"
       ]
   }

Running the formatter again with a altered version of the formatter
===================================================================

(this apply for the version without version tracking)

updating the indent to "2"

  $ cat > "$TESTTMP"/json_format.py <<EOF
  > """ Auto-format the JSON file passed as a command-line argument and output
  > the formatted code in stdout
  > """
  > from __future__ import print_function
  > import sys
  > import json
  > with open(sys.argv[1], 'rb') as infile:
  >     obj = json.load(infile)
  > with sys.stdout:
  >     json.dump(obj, sys.stdout, sort_keys=True, indent=2, separators=(',', ': '))
  >     sys.stdout.write("\n")
  > EOF

auto run will not see the change

  $ hg up -C 'desc("yes-yes-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-yes-red")' --config format-source.run-mode=auto
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg diff
  diff -r 31a4db03d8a8 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -7,8 +7,8 @@
           8
       ],
       "key3": [
  -        "arthur",
  -        "babar",
  -        "celeste"
  +        "Arthur",
  +        "Babar",
  +        "Celeste"
       ]
   }

forced run will apply it

  $ hg up -C 'desc("yes-yes-blue")'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge 'desc("yes-yes-red")' --config format-source.run-mode=on
  merging root-file.json
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg diff
  diff -r 31a4db03d8a8 root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,14 +1,14 @@
   {
  -    "key1": 2,
  -    "key2": [
  -        5,
  -        6,
  -        7,
  -        8
  -    ],
  -    "key3": [
  -        "arthur",
  -        "babar",
  -        "celeste"
  -    ]
  +  "key1": 2,
  +  "key2": [
  +    5,
  +    6,
  +    7,
  +    8
  +  ],
  +  "key3": [
  +    "Arthur",
  +    "Babar",
  +    "Celeste"
  +  ]
   }
