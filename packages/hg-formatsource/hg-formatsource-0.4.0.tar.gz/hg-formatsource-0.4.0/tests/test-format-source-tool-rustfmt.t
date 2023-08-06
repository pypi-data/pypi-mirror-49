#require rustfmt

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

Add rust file
=============

  $ hg up -Cq 0

  $ cat << EOF >> rustfmt-test-file.rust
  > fn main() {
  > println!("Hello World!");
  >  }
  > EOF

  $ hg add rustfmt-test-file.rust

  $ hg commit -q -m "Add rustfmt test file"

  $ hg format-source --date '0 0' rustfmt glob:rustfmt-test-file.rust -m 'format using rustfmt'

  $ hg export . --git -T "{diff}"
  diff --git a/.hg-format-source b/.hg-format-source
  new file mode 100644
  --- /dev/null
  +++ b/.hg-format-source
  @@ -0,0 +1,1 @@
  +{"configpaths": ["rustfmt.toml", ".rustfmt.toml"], "pattern": "glob:rustfmt-test-file.rust", "tool": "rustfmt", "version": "*"} (glob)
  diff --git a/rustfmt-test-file.rust b/rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust
  +++ b/rustfmt-test-file.rust
  @@ -1,3 +1,3 @@
   fn main() {
  -println!("Hello World!");
  - }
  +    println!("Hello World!");
  +}

Make some changes
=================

  $ cat << EOF > rustfmt-test-file.rust
  > fn main() {
  >     println!("Hello Foobar!");
  > }
  > EOF

  $ hg commit -q -m "Hello Foobar"

  $ hg export . --git -T "{diff}"
  diff --git a/rustfmt-test-file.rust b/rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust
  +++ b/rustfmt-test-file.rust
  @@ -1,3 +1,3 @@
   fn main() {
  -    println!("Hello World!");
  +    println!("Hello Foobar!");
   }

Add another change on another branch
====================================

  $ hg up -Cq 2

  $ cat << EOF > rustfmt-test-file.rust
  > fn main() {
  >     println!("Hello World!");
  > }
  > 
  > pub fn answer(i:isize, j:isize, k:isize, l:isize, m:isize, n:isize, o:isize) -> isize {
  >     return i+j+k+l+m+n+o;
  > }
  > EOF

  $ hg commit -m "Add answer"
  created new head

  $ hg export . --git -T "{diff}"
  diff --git a/rustfmt-test-file.rust b/rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust
  +++ b/rustfmt-test-file.rust
  @@ -1,3 +1,7 @@
   fn main() {
       println!("Hello World!");
   }
  +
  +pub fn answer(i:isize, j:isize, k:isize, l:isize, m:isize, n:isize, o:isize) -> isize {
  +    return i+j+k+l+m+n+o;
  +}

Add a config file
=================

  $ cat << EOF > .rustfmt.toml
  > hard_tabs = true
  > EOF

  $ hg add .rustfmt.toml

  $ rustfmt rustfmt-test-file.rust

  $ hg commit -m "Add rustfmt config file"

  $ hg export . --git -T "{diff}"
  diff --git a/.rustfmt.toml b/.rustfmt.toml
  new file mode 100644
  --- /dev/null
  +++ b/.rustfmt.toml
  @@ -0,0 +1,1 @@
  +hard_tabs = true
  diff --git a/rustfmt-test-file.rust b/rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust
  +++ b/rustfmt-test-file.rust
  @@ -1,7 +1,7 @@
   fn main() {
  -    println!("Hello World!");
  +	println!("Hello World!");
   }
   
  -pub fn answer(i:isize, j:isize, k:isize, l:isize, m:isize, n:isize, o:isize) -> isize {
  -    return i+j+k+l+m+n+o;
  +pub fn answer(i: isize, j: isize, k: isize, l: isize, m: isize, n: isize, o: isize) -> isize {
  +	return i + j + k + l + m + n + o;
   }


Test merge
==========

  $ hg log -G -T compact
  @  5[tip]   *   1970-01-01 00:00 +0000   test (glob)
  |    Add rustfmt config file
  |
  o  4:2   *   1970-01-01 00:00 +0000   test (glob)
  |    Add answer
  |
  | o  3   *   1970-01-01 00:00 +0000   test (glob)
  |/     Hello Foobar
  |
  o  2   *   1970-01-01 00:00 +0000   test (glob)
  |    format using rustfmt
  |
  o  1   c48b5f3d107c   1970-01-01 00:00 +0000   test
  |    Add rustfmt test file
  |
  o  0   b00443a54871   1970-01-01 00:00 +0000   test
       Root
  

  $ hg merge
  rustfmt.toml: No such file or directory
  merging rustfmt-test-file.rust
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

  $ hg diff --git
  diff --git a/rustfmt-test-file.rust b/rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust
  +++ b/rustfmt-test-file.rust
  @@ -1,5 +1,5 @@
   fn main() {
  -	println!("Hello World!");
  +	println!("Hello Foobar!");
   }
   
   pub fn answer(i: isize, j: isize, k: isize, l: isize, m: isize, n: isize, o: isize) -> isize {

  $ hg commit -m "Merge"

  $ hg export . --git -T "{diff}"
  diff --git a/rustfmt-test-file.rust b/rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust
  +++ b/rustfmt-test-file.rust
  @@ -1,5 +1,5 @@
   fn main() {
  -	println!("Hello World!");
  +	println!("Hello Foobar!");
   }
   
   pub fn answer(i: isize, j: isize, k: isize, l: isize, m: isize, n: isize, o: isize) -> isize {

  $ hg export . --git -T "{diff}" --switch-parent
  diff --git a/.rustfmt.toml b/.rustfmt.toml
  new file mode 100644
  --- /dev/null
  +++ b/.rustfmt.toml
  @@ -0,0 +1,1 @@
  +hard_tabs = true
  diff --git a/rustfmt-test-file.rust b/rustfmt-test-file.rust
  --- a/rustfmt-test-file.rust
  +++ b/rustfmt-test-file.rust
  @@ -1,3 +1,7 @@
   fn main() {
  -    println!("Hello Foobar!");
  +	println!("Hello Foobar!");
   }
  +
  +pub fn answer(i: isize, j: isize, k: isize, l: isize, m: isize, n: isize, o: isize) -> isize {
  +	return i + j + k + l + m + n + o;
  +}
