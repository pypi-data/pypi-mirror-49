#require clang-format

Test that the defaults configurations for known tools are working correctly

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

Testing clang-format tool
=========================

  $ hg up -Cq 0

  $ cat << EOF >> hello-world.cpp
  > #include <iostream>
  > 
  > int main() 
  > {
  >     std::cout << "Hello, World!";
  >     return 0;
  > }
  > EOF

  $ cat << EOF >> hello-world.c
  > #include<stdio.h>
  > 
  > int main(void) {
  >     printf("Hello World\n");
  >     return 0;
  > }
  > EOF

  $ hg add *
  ROOT already tracked!

  $ hg commit -q -m "Add clang-format test file"

  $ hg format-source --date '0 0' clang-format glob:hello-world.cpp -m 'format using clang-format'

  $ hg export . --git -T "{diff}"
  diff --git a/.hg-format-source b/.hg-format-source
  new file mode 100644
  --- /dev/null
  +++ b/.hg-format-source
  @@ -0,0 +1,1 @@
  +{"configpaths": [".clang-format", ".clang-format-ignore"], "pattern": "glob:hello-world.cpp", "tool": "clang-format", "version": "*"} (glob)
  diff --git a/hello-world.cpp b/hello-world.cpp
  --- a/hello-world.cpp
  +++ b/hello-world.cpp
  @@ -1,7 +1,6 @@
   #include <iostream>
   
  -int main() 
  -{
  -    std::cout << "Hello, World!";
  -    return 0;
  +int main() {
  +  std::cout << "Hello, World!";
  +  return 0;
   }

  $ hg format-source --date '0 0' clang-format glob:hello-world.c -m 'format using clang-format'

  $ hg export . --git -T "{diff}"
  diff --git a/.hg-format-source b/.hg-format-source
  --- a/.hg-format-source
  +++ b/.hg-format-source
  @@ -1,1 +1,2 @@
   {"configpaths": [".clang-format", ".clang-format-ignore"], "pattern": "glob:hello-world.cpp", "tool": "clang-format", "version": "*"} (glob)
  +{"configpaths": [".clang-format", ".clang-format-ignore"], "pattern": "glob:hello-world.c", "tool": "clang-format", "version": "*"} (glob)
  diff --git a/hello-world.c b/hello-world.c
  --- a/hello-world.c
  +++ b/hello-world.c
  @@ -1,6 +1,6 @@
  -#include<stdio.h>
  +#include <stdio.h>
   
   int main(void) {
  -    printf("Hello World\n");
  -    return 0;
  +  printf("Hello World\n");
  +  return 0;
   }

Make some changes
=================

  $ cat << EOF > hello-world.cpp
  > #include <iostream>
  > 
  > int main() {
  >   std::cout << "Hello, FooBar!";
  >   return 0;
  > }
  > EOF

  $ cat << EOF > hello-world.c
  > #include <stdio.h>
  > 
  > int main(void) {
  >   printf("Hello FooBar\n");
  >   return 0;
  > }
  > EOF

  $ hg commit -q -m "Hello Foobar"

  $ hg export . --git -T "{diff}"
  diff --git a/hello-world.c b/hello-world.c
  --- a/hello-world.c
  +++ b/hello-world.c
  @@ -1,6 +1,6 @@
   #include <stdio.h>
   
   int main(void) {
  -  printf("Hello World\n");
  +  printf("Hello FooBar\n");
     return 0;
   }
  diff --git a/hello-world.cpp b/hello-world.cpp
  --- a/hello-world.cpp
  +++ b/hello-world.cpp
  @@ -1,6 +1,6 @@
   #include <iostream>
   
   int main() {
  -  std::cout << "Hello, World!";
  +  std::cout << "Hello, FooBar!";
     return 0;
   }

Add another change on another branch
====================================

  $ hg up -Cq 3

  $ cat << EOF > hello-world.cpp
  > #include <iostream>
  > 
  > int main() {
  >   std::cout << "Hello, World!";
  >   return 0;
  > }
  > 
  > int answer() {
  >   return 42
  > }
  > EOF

  $ cat << EOF > hello-world.c
  > #include <stdio.h>
  > 
  > int main(void) {
  >   printf("Hello World\n");
  >   return 0;
  > }
  > 
  > int answer() {
  >   return 42
  > }
  > EOF

  $ hg commit -m "Exit 1"
  created new head

  $ hg export . --git -T "{diff}"
  diff --git a/hello-world.c b/hello-world.c
  --- a/hello-world.c
  +++ b/hello-world.c
  @@ -4,3 +4,7 @@
     printf("Hello World\n");
     return 0;
   }
  +
  +int answer() {
  +  return 42
  +}
  diff --git a/hello-world.cpp b/hello-world.cpp
  --- a/hello-world.cpp
  +++ b/hello-world.cpp
  @@ -4,3 +4,7 @@
     std::cout << "Hello, World!";
     return 0;
   }
  +
  +int answer() {
  +  return 42
  +}

Add a config file
=================

  $ cat << EOF >> .clang-format
  > ---
  > IndentWidth:     4
  > ...
  > EOF

  $ hg add .clang-format

  $ clang-format -i hello-world.*

  $ hg commit -m "Add clang-format config file"

  $ hg export . --git -T "{diff}"
  diff --git a/.clang-format b/.clang-format
  new file mode 100644
  --- /dev/null
  +++ b/.clang-format
  @@ -0,0 +1,3 @@
  +---
  +IndentWidth:     4
  +...
  diff --git a/hello-world.c b/hello-world.c
  --- a/hello-world.c
  +++ b/hello-world.c
  @@ -1,10 +1,8 @@
   #include <stdio.h>
   
   int main(void) {
  -  printf("Hello World\n");
  -  return 0;
  +    printf("Hello World\n");
  +    return 0;
   }
   
  -int answer() {
  -  return 42
  -}
  +int answer() { return 42 }
  diff --git a/hello-world.cpp b/hello-world.cpp
  --- a/hello-world.cpp
  +++ b/hello-world.cpp
  @@ -1,10 +1,8 @@
   #include <iostream>
   
   int main() {
  -  std::cout << "Hello, World!";
  -  return 0;
  +    std::cout << "Hello, World!";
  +    return 0;
   }
   
  -int answer() {
  -  return 42
  -}
  +int answer() { return 42 }


Test merge
==========

  $ hg log -G -T compact
  @  6[tip]   *   1970-01-01 00:00 +0000   test (glob)
  |    Add clang-format config file
  |
  o  5:3   *   1970-01-01 00:00 +0000   test (glob)
  |    Exit 1
  |
  | o  4   *   1970-01-01 00:00 +0000   test (glob)
  |/     Hello Foobar
  |
  o  3   *   1970-01-01 00:00 +0000   test (glob)
  |    format using clang-format
  |
  o  2   *   1970-01-01 00:00 +0000   test (glob)
  |    format using clang-format
  |
  o  1   a7685500a404   1970-01-01 00:00 +0000   test
  |    Add clang-format test file
  |
  o  0   b00443a54871   1970-01-01 00:00 +0000   test
       Root
  

  $ hg merge
  .clang-format-ignore: No such file or directory
  .clang-format-ignore: No such file or directory
  merging hello-world.c
  merging hello-world.cpp
  0 files updated, 2 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)

  $ hg commit -m "Merge"

  $ hg export . --git -T "{diff}"
  diff --git a/hello-world.c b/hello-world.c
  --- a/hello-world.c
  +++ b/hello-world.c
  @@ -1,7 +1,7 @@
   #include <stdio.h>
   
   int main(void) {
  -    printf("Hello World\n");
  +    printf("Hello FooBar\n");
       return 0;
   }
   
  diff --git a/hello-world.cpp b/hello-world.cpp
  --- a/hello-world.cpp
  +++ b/hello-world.cpp
  @@ -1,7 +1,7 @@
   #include <iostream>
   
   int main() {
  -    std::cout << "Hello, World!";
  +    std::cout << "Hello, FooBar!";
       return 0;
   }
   

  $ hg export . --git -T "{diff}" --switch-parent
  diff --git a/.clang-format b/.clang-format
  new file mode 100644
  --- /dev/null
  +++ b/.clang-format
  @@ -0,0 +1,3 @@
  +---
  +IndentWidth:     4
  +...
  diff --git a/hello-world.c b/hello-world.c
  --- a/hello-world.c
  +++ b/hello-world.c
  @@ -1,6 +1,8 @@
   #include <stdio.h>
   
   int main(void) {
  -  printf("Hello FooBar\n");
  -  return 0;
  +    printf("Hello FooBar\n");
  +    return 0;
   }
  +
  +int answer() { return 42 }
  diff --git a/hello-world.cpp b/hello-world.cpp
  --- a/hello-world.cpp
  +++ b/hello-world.cpp
  @@ -1,6 +1,8 @@
   #include <iostream>
   
   int main() {
  -  std::cout << "Hello, FooBar!";
  -  return 0;
  +    std::cout << "Hello, FooBar!";
  +    return 0;
   }
  +
  +int answer() { return 42 }

Test that default configuration doesn't overwrite the user-defined one
######################################################################

  $ hg format-source --date '0 0' clang-format --config "format-source.clang-format=clang-format ---" glob:hello-world.cpp -m 'format using clang-format'
  abort: clang-format: clang-format exited with status 1
  [255]
