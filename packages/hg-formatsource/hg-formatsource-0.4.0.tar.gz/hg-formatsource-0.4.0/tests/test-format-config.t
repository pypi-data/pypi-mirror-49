
Basic init

  $ code_root=`dirname $TESTDIR`

  $ cat << EOF >> $HGRCPATH
  > [extensions]
  > formatsource=${code_root}/hgext3rd/formatsource.py
  > rebase =
  > strip =
  > [format-source]
  > json = python $TESTDIR/testlib/json-pretty.py
  > json:configpaths = .json-indent
  > [default]
  > format-source=--date '0 0'
  > [ui]
  > merge=:merge3
  > EOF
  $ HGMERGE=:merge3

  $ hg init test_repo
  $ cd test_repo

Commit various json file

  $ mkdir dir-1
  $ cat << EOF > dir-1/file-1.json
  > {"key1": [42,53,78], "key2": [9,3,8,1], "key3": ["London", "Paris", "Tokyo"]}
  > EOF
  $ cat << EOF > dir-1/file-2.json
  > {"key1": 1, "key2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key3": [54]}
  > EOF
  $ hg add .
  adding dir-1/file-1.json
  adding dir-1/file-2.json
  $ hg commit --message 'initial commit'

format them (in multiple steps)

  $ hg format-source --date '0 0' json glob:*/file-1.json -m 'format without config' --debug
  running python */testlib/json-pretty.py dir-1/file-1.json (glob)
  format-source: [json] input file, output pipe mode
  adding .hg-format-source
  committing files:
  .hg-format-source
  dir-1/file-1.json
  committing manifest
  committing changelog
  updating the branch cache
  committed changeset 1:fb63bdd6edbf60d86f7aeaf0d806ecf6555c02eb
  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID fb63bdd6edbf60d86f7aeaf0d806ecf6555c02eb
  # Parent  103bbf4a41e9e9010c27ab49c158f99b176d4f3e
  format without config
  
  diff -r 103bbf4a41e9 -r fb63bdd6edbf .hg-format-source
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +{"configpaths": [".json-indent"], "pattern": "glob:*/file-1.json", "tool": "json"}
  diff -r 103bbf4a41e9 -r fb63bdd6edbf dir-1/file-1.json
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
  $ echo 2 > .json-indent
  $ hg add .json-indent
  $ python $TESTDIR/testlib/json-pretty.py < dir-1/file-1.json > tmp
  full pipe mode
  $ mv tmp dir-1/file-1.json
  $ hg diff
  diff -r fb63bdd6edbf .json-indent
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.json-indent	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +2
  diff -r fb63bdd6edbf dir-1/file-1.json
  --- a/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,18 +1,18 @@
   {
  -    "key1": [
  -        42,
  -        53,
  -        78
  -    ],
  -    "key2": [
  -        9,
  -        3,
  -        8,
  -        1
  -    ],
  -    "key3": [
  -        "London",
  -        "Paris",
  -        "Tokyo"
  -    ]
  +  "key1": [
  +    42,
  +    53,
  +    78
  +  ],
  +  "key2": [
  +    9,
  +    3,
  +    8,
  +    1
  +  ],
  +  "key3": [
  +    "London",
  +    "Paris",
  +    "Tokyo"
  +  ]
   }
  $ hg commit -m 'reformat with indent=2'
  $ echo 1 > .json-indent
  $ python $TESTDIR/testlib/json-pretty.py < dir-1/file-1.json > tmp
  full pipe mode
  $ mv tmp dir-1/file-1.json
  $ hg diff
  diff -r bacb7be97453 .json-indent
  --- a/.json-indent	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.json-indent	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,1 @@
  -2
  +1
  diff -r bacb7be97453 dir-1/file-1.json
  --- a/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,18 +1,18 @@
   {
  -  "key1": [
  -    42,
  -    53,
  -    78
  -  ],
  -  "key2": [
  -    9,
  -    3,
  -    8,
  -    1
  -  ],
  -  "key3": [
  -    "London",
  -    "Paris",
  -    "Tokyo"
  -  ]
  + "key1": [
  +  42,
  +  53,
  +  78
  + ],
  + "key2": [
  +  9,
  +  3,
  +  8,
  +  1
  + ],
  + "key3": [
  +  "London",
  +  "Paris",
  +  "Tokyo"
  + ]
   }
  $ hg commit -m 'reformat with indent=1'

Add changes on another branch

  $ hg up 0
  1 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ cat << EOF > dir-1/file-1.json
  > {"key1": [42,53,78,66], "key2": [9,3,8,1], "key3": ["London", "Paris", "Tokyo"]}
  > EOF
  $ cat << EOF > dir-1/file-2.json
  > {"key1": 1, "key2": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key3": [54, 55]}
  > EOF
  $ hg commit -m 'some editions'
  created new head

Merge with "format without config"

  $ hg log -G
  @  changeset:   4:360af76de133
  |  tag:         tip
  |  parent:      0:103bbf4a41e9
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     some editions
  |
  | o  changeset:   3:fa670ec0f89c
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     reformat with indent=1
  | |
  | o  changeset:   2:bacb7be97453
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     reformat with indent=2
  | |
  | o  changeset:   1:fb63bdd6edbf
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    summary:     format without config
  |
  o  changeset:   0:103bbf4a41e9
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     initial commit
  
  $ f --md5 dir-1/file-2.json
  dir-1/file-2.json: md5=19be5044f37a12515b1bf92e2becf702
  $ hg merge 1
  merging dir-1/file-1.json
  1 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ f --md5 dir-1/file-2.json
  dir-1/file-2.json: md5=19be5044f37a12515b1bf92e2becf702
  $ hg diff -r 'p2()' dir-1/file-1.json
  diff -r fb63bdd6edbf dir-1/file-1.json
  --- a/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -2,7 +2,8 @@
       "key1": [
           42,
           53,
  -        78
  +        78,
  +        66
       ],
       "key2": [
           9,
  $ hg commit -m 'merge #1'

Merge with "format with indent=2"

  $ hg merge 2
  merging dir-1/file-1.json
  1 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ f --md5 dir-1/file-2.json
  dir-1/file-2.json: md5=19be5044f37a12515b1bf92e2becf702
  $ hg diff -r 'p2()' dir-1/file-1.json
  diff -r bacb7be97453 dir-1/file-1.json
  --- a/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -2,7 +2,8 @@
     "key1": [
       42,
       53,
  -    78
  +    78,
  +    66
     ],
     "key2": [
       9,
  $ hg commit -m 'merge #2'

Merge with indent=1

  $ hg merge 3
  merging dir-1/file-1.json
  1 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ f --md5 dir-1/file-2.json
  dir-1/file-2.json: md5=19be5044f37a12515b1bf92e2becf702
  $ hg diff -r 'p2()' dir-1/file-1.json
  diff -r fa670ec0f89c dir-1/file-1.json
  --- a/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-1.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -2,7 +2,8 @@
    "key1": [
     42,
     53,
  -  78
  +  78,
  +  66
    ],
    "key2": [
     9,
  $ hg commit -m 'merge #3'

Test recording additional config path

Create an additional file
  $ cat << EOF > dir-1/file-3.json
  > {"key4": 1, "key5": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key6": [54]}
  > EOF

  $ hg add dir-1/file-3.json

  $ hg commit -m "Add new file"

And two additional config files
  $ touch my-extra-config-file

  $ hg format-source --extra-config-file my-extra-config-file --extra-config-file my-extra-config-file-2 --date '0 0' json glob:*/file-3.json -m "Formatting with additional config file"

  $ hg st
  ? my-extra-config-file

  $ hg export .
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID a00be7817b19de6f61f41bfeb232bc08ae857420
  # Parent  f83f591e0d528a2c78f60fee2fa561665ef83489
  Formatting with additional config file
  
  diff -r f83f591e0d52 -r a00be7817b19 .hg-format-source
  --- a/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  +++ b/.hg-format-source	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,2 @@
   {"configpaths": [".json-indent"], "pattern": "glob:*/file-1.json", "tool": "json"}
  +{"configpaths": [".json-indent", "my-extra-config-file", "my-extra-config-file-2"], "pattern": "glob:*/file-3.json", "tool": "json"}
  diff -r f83f591e0d52 -r a00be7817b19 dir-1/file-3.json
  --- a/dir-1/file-3.json	Thu Jan 01 00:00:00 1970 +0000
  +++ b/dir-1/file-3.json	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,18 @@
  -{"key4": 1, "key5": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], "key6": [54]}
  +{
  + "key4": 1,
  + "key5": [
  +  0,
  +  1,
  +  2,
  +  3,
  +  4,
  +  5,
  +  6,
  +  7,
  +  8,
  +  9
  + ],
  + "key6": [
  +  54
  + ]
  +}
