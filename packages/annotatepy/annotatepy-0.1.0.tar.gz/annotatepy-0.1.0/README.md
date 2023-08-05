annotatepy
==========

Scans Pytohn source code and emits an annotation graph for
[git.sr.ht](https://git.sr.ht/)'s code [annotations
feature](https://man.sr.ht/git.sr.ht/annotations.md).

Work in progress, currently annotates only function calls.

Resources
---------

* Homepage: https://git.sr.ht/~ihabunek/annotatepy/
* Issues: https://todo.sr.ht/~ihabunek/annotatepy/

Usage
-----

```
annotatepy [-h] [-o OUTPUT] [-r ROOT] [source_paths [source_paths ...]]

Generate sourcehut annotations

positional arguments:
  source_paths          one or more paths within the project containing the
                        code to be annotated (defaults to project root)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file (default: annotations.json)
  -r ROOT, --root ROOT  project root (defaults to working dir)

https://git.sr.ht/~ihabunek/annotatepy/
```
