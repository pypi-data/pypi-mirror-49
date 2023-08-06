#require black

Basic init

  $ code_root=`dirname $TESTDIR`

  $ cat << EOF >> $HGRCPATH
  > [extensions]
  > formatsource=${code_root}/hgext3rd/formatsource.py
  > [default]
  > format-source=--date '0 0'
  > [ui]
  > merge=:merge3
  > EOF
  $ HGMERGE=:merge3

  $ hg init default-io-modes

  $ cd default-io-modes

  $ touch ROOT

  $ hg commit -Aq -m "Root"

Add python file
===============

  $ hg up -Cq 0

  $ cat << EOF >> black-test-file.py
  > 
  > l = [1,
  >      2,
  >      3,
  > ]
  > EOF

  $ hg add black-test-file.py

  $ hg commit -q -m "Add black test file"

Black is tacky
==============

  $ export LC_ALL=C.UTF-8
  $ export LANG=C.UTF-8

  $ hg format-source --date '0 0' black glob:black-test-file.py -m 'format using black'

  $ hg export . --git -T "{diff}"
  diff --git a/.hg-format-source b/.hg-format-source
  new file mode 100644
  --- /dev/null
  +++ b/.hg-format-source
  @@ -0,0 +1,1 @@
  +{"configpaths": ["pyproject.toml"], "pattern": "glob:black-test-file.py", "tool": "black", "version": "*"} (glob)
  diff --git a/black-test-file.py b/black-test-file.py
  --- a/black-test-file.py
  +++ b/black-test-file.py
  @@ -1,5 +1,1 @@
  -
  -l = [1,
  -     2,
  -     3,
  -]
  +l = [1, 2, 3]

Make some changes
=================

  $ cat << EOF > black-test-file.py
  > l = [1, 2, 3, 4,5,6,7,8,9,10]
  > EOF

  $ hg commit -q -m "Update black test file"

  $ hg export . --git -T "{diff}"
  diff --git a/black-test-file.py b/black-test-file.py
  --- a/black-test-file.py
  +++ b/black-test-file.py
  @@ -1,1 +1,1 @@
  -l = [1, 2, 3]
  +l = [1, 2, 3, 4,5,6,7,8,9,10]

Add another change on another branch
====================================

  $ hg up -Cq 2

  $ cat << EOF > black-test-file.py
  > l = [1, 2, 3]
  > 
  > d = {"key": "value"}
  > EOF

  $ hg commit -m "Add dict"
  created new head

  $ hg export . --git -T "{diff}"
  diff --git a/black-test-file.py b/black-test-file.py
  --- a/black-test-file.py
  +++ b/black-test-file.py
  @@ -1,1 +1,3 @@
   l = [1, 2, 3]
  +
  +d = {"key": "value"}


Add a config file
=================

  $ cat << EOF >> pyproject.toml
  > [tool.black]
  > line-length = 10
  > EOF

  $ hg add pyproject.toml

  $ black black-test-file.py
  reformatted black-test-file.py
  All done! \xe2\x9c\xa8 \xf0\x9f\x8d\xb0 \xe2\x9c\xa8 (esc)
  1 file reformatted.

  $ hg commit -m "Add black config file"

  $ hg export . --git -T "{diff}"
  diff --git a/black-test-file.py b/black-test-file.py
  --- a/black-test-file.py
  +++ b/black-test-file.py
  @@ -1,3 +1,9 @@
  -l = [1, 2, 3]
  +l = [
  +    1,
  +    2,
  +    3,
  +]
   
  -d = {"key": "value"}
  +d = {
  +    "key": "value"
  +}
  diff --git a/pyproject.toml b/pyproject.toml
  new file mode 100644
  --- /dev/null
  +++ b/pyproject.toml
  @@ -0,0 +1,2 @@
  +[tool.black]
  +line-length = 10


Test merge
==========

  $ hg log -G -T compact
  @  5[tip]   *   1970-01-01 00:00 +0000   test (glob)
  |    Add black config file
  |
  o  4:2   *   1970-01-01 00:00 +0000   test (glob)
  |    Add dict
  |
  | o  3   *   1970-01-01 00:00 +0000   test (glob)
  |/     Update black test file
  |
  o  2   *   1970-01-01 00:00 +0000   test (glob)
  |    format using black
  |
  o  1   c2cba438e30a   1970-01-01 00:00 +0000   test
  |    Add black test file
  |
  o  0   b00443a54871   1970-01-01 00:00 +0000   test
       Root
  

  $ hg merge
  merging black-test-file.py
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

  $ hg commit -m "Merge"

  $ hg export . --git -T "{diff}"
  diff --git a/black-test-file.py b/black-test-file.py
  --- a/black-test-file.py
  +++ b/black-test-file.py
  @@ -2,6 +2,13 @@
       1,
       2,
       3,
  +    4,
  +    5,
  +    6,
  +    7,
  +    8,
  +    9,
  +    10,
   ]
   
   d = {

  $ hg export . --git -T "{diff}" --switch-parent
  diff --git a/black-test-file.py b/black-test-file.py
  --- a/black-test-file.py
  +++ b/black-test-file.py
  @@ -1,1 +1,16 @@
  -l = [1, 2, 3, 4,5,6,7,8,9,10]
  +l = [
  +    1,
  +    2,
  +    3,
  +    4,
  +    5,
  +    6,
  +    7,
  +    8,
  +    9,
  +    10,
  +]
  +
  +d = {
  +    "key": "value"
  +}
  diff --git a/pyproject.toml b/pyproject.toml
  new file mode 100644
  --- /dev/null
  +++ b/pyproject.toml
  @@ -0,0 +1,2 @@
  +[tool.black]
  +line-length = 10
