
Basic init

  $ code_root=`dirname $TESTDIR`

  $ cat >> json_format.py <<EOF
  > """ Auto-format the JSON file passed as a command-line argument and output
  > the formatted code in stdout
  > """
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

  $ hg init test_repo
  $ cd test_repo

Commit various json file

  $ cat << EOF > root-file.json
  > {"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  > EOF
  $ mkdir dir-1
  $ cat << EOF > dir-1/file-1.json
  > {"key1": [42,53,78], "key2": [9,3,8,1], "key3": ["London", "Paris", "Tokyo"]}
  > EOF
  $ cat << EOF > dir-1/file-2.json
  > {"key1": 1, "key2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key3": [54]}
  > EOF
  $ mkdir dir-2
  $ cat << EOF > dir-2/file-1.json
  > {"key1": [44,50,82], "key2": [4, 8, -4, 5], "key3": ["Asia", "Europe"]}
  > EOF
  $ cat << EOF > dir-2/file-2.json
  > {"key1": 6,
  > "key2": [3, 5, -2, 3, 4, 11, 10, -4, 8, 9],
  > "key3": [898, 32543, 2342]}
  > EOF
  $ cat << EOF > "dir-2/file 3.json"
  > {"key1": "hello", "key2": [3, 1, 8, -1, 19, 2], "key3": "babar"}
  > EOF
  $ hg add .
  adding dir-1/file-1.json
  adding dir-1/file-2.json
  adding dir-2/file 3.json
  adding dir-2/file-1.json
  adding dir-2/file-2.json
  adding root-file.json
  $ hg commit --message 'initial commit'

format them (in multiple steps)

  $ hg format-source --date '0 0' json glob:root-file.json -m 'format the root-file'
  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 37aedc05b31aaabe47210edf1692ab0a175479ec
  # Parent  bdc6e1fea62561308c0f00624b17fe3d25667f66
  format the root-file
  
  diff -r bdc6e1fea625 -r 37aedc05b31a .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +{"pattern": "glob:root-file.json", "tool": "json"}
  diff -r bdc6e1fea625 -r 37aedc05b31a root-file.json
  --- a/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/root-file.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,14 @@
  -{"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  +{
  +    "key1": 1,
  +    "key2": [
  +        5,
  +        6,
  +        7,
  +        8
  +    ],
  +    "key3": [
  +        "arthur",
  +        "babar",
  +        "celeste"
  +    ]
  +}
  $ hg format-source --date '0 0' json 'glob:dir-1/**' -m 'format dir1 as a whole'
  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 7a251aee7fec4d496195baf42708da1feb1fbb1d
  # Parent  37aedc05b31aaabe47210edf1692ab0a175479ec
  format dir1 as a whole
  
  diff -r 37aedc05b31a -r 7a251aee7fec .hg-format-source
  --- a/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,2 @@
   {"pattern": "glob:root-file.json", "tool": "json"}
  +{"pattern": "glob:dir-1/**", "tool": "json"}
  diff -r 37aedc05b31a -r 7a251aee7fec dir-1/file-1.json
  --- a/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,18 @@
  -{"key1": [42,53,78], "key2": [9,3,8,1], "key3": ["London", "Paris", "Tokyo"]}
  +{
  +    "key1": [
  +        42,
  +        53,
  +        78
  +    ],
  +    "key2": [
  +        9,
  +        3,
  +        8,
  +        1
  +    ],
  +    "key3": [
  +        "London",
  +        "Paris",
  +        "Tokyo"
  +    ]
  +}
  diff -r 37aedc05b31a -r 7a251aee7fec dir-1/file-2.json
  --- a/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-2.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,18 @@
  -{"key1": 1, "key2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key3": [54]}
  +{
  +    "key1": 1,
  +    "key2": [
  +        0,
  +        1,
  +        2,
  +        3,
  +        4,
  +        5,
  +        6,
  +        7,
  +        8,
  +        9
  +    ],
  +    "key3": [
  +        54
  +    ]
  +}
  $ hg format-source --date '0 0' json glob:dir-2/file-1.json "glob:dir-2/file 3.json" -m 'format some dir2 with explicite pattern'
  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 7e4070817d0b27dae5c40d99799adeca684a5e4c
  # Parent  7a251aee7fec4d496195baf42708da1feb1fbb1d
  format some dir2 with explicite pattern
  
  diff -r 7a251aee7fec -r 7e4070817d0b .hg-format-source
  --- a/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,2 +1,4 @@
   {"pattern": "glob:root-file.json", "tool": "json"}
   {"pattern": "glob:dir-1/**", "tool": "json"}
  +{"pattern": "glob:dir-2/file-1.json", "tool": "json"}
  +{"pattern": "glob:dir-2/file 3.json", "tool": "json"}
  diff -r 7a251aee7fec -r 7e4070817d0b dir-2/file 3.json
  --- a/dir-2/file 3.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-2/file 3.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,12 @@
  -{"key1": "hello", "key2": [3, 1, 8, -1, 19, 2], "key3": "babar"}
  +{
  +    "key1": "hello",
  +    "key2": [
  +        3,
  +        1,
  +        8,
  +        -1,
  +        19,
  +        2
  +    ],
  +    "key3": "babar"
  +}
  diff -r 7a251aee7fec -r 7e4070817d0b dir-2/file-1.json
  --- a/dir-2/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-2/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,17 @@
  -{"key1": [44,50,82], "key2": [4, 8, -4, 5], "key3": ["Asia", "Europe"]}
  +{
  +    "key1": [
  +        44,
  +        50,
  +        82
  +    ],
  +    "key2": [
  +        4,
  +        8,
  +        -4,
  +        5
  +    ],
  +    "key3": [
  +        "Asia",
  +        "Europe"
  +    ]
  +}
  $ hg log -G
  @  changeset:   3:7e4070817d0b
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     format some dir2 with explicite pattern
  |
  o  changeset:   2:7a251aee7fec
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     format dir1 as a whole
  |
  o  changeset:   1:37aedc05b31a
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     format the root-file
  |
  o  changeset:   0:bdc6e1fea625
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     initial commit
  

Test formatting them in-place without commiting
===============================================

  $ cat << EOF > root-file.json
  > {"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  > EOF
  $ cat << EOF > dir-1/file-1.json
  > {"key1": [42,53,78], "key2": [9,3,8,1], "key3": ["London", "Paris", "Tokyo"]}
  > EOF
  $ cat << EOF > dir-1/file-2.json
  > {"key1": 1, "key2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key3": [54]}
  > EOF
  $ cat << EOF > dir-2/file-1.json
  > {"key1": [44,50,82], "key2": [4, 8, -4, 5], "key3": ["Asia", "Europe"]}
  > EOF
  $ cat << EOF > dir-2/file-2.json
  > {"key1": 6,
  > "key2": [3, 5, -2, 3, 4, 11, 10, -4, 8, 9],
  > "key3": [898, 32543, 2342]}
  > EOF
  $ cat << EOF > "dir-2/file 3.json"
  > {"key1": "hello", "key2": [3, 1, 8, -1, 19, 2], "key3": "babar"}
  > EOF
  $ hg st
  M dir-1/file-1.json
  M dir-1/file-2.json
  M dir-2/file 3.json
  M dir-2/file-1.json
  M root-file.json
  $ hg id -r .
  7e4070817d0b tip

Format all files in-place without commiting

  $ hg format-source --current

  $ hg st

  $ hg id -r .
  7e4070817d0b tip

  $ hg up -C
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved

Format a specific file in-place without commiting

  $ cat << EOF > root-file.json
  > {"key1": 1, "key2": [5,6,7,8], "key3": ["arthur", "babar", "celeste"]}
  > EOF
  $ cat << EOF > dir-1/file-1.json
  > {"key1": [42,53,78], "key2": [9,3,8,1], "key3": ["London", "Paris", "Tokyo"]}
  > EOF

  $ hg st
  M dir-1/file-1.json
  M root-file.json

  $ hg format-source --current dir-1/file-1.json

  $ hg st
  M root-file.json

  $ hg id -r .
  7e4070817d0b tip
