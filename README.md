# Work in progress. Not yet open for distribution

vim-nose
========

Plugin wrapping `nosetests` command line tool to execute python tests inside Vim. All in the name of productivity!

Requirements
============

- [vim-dispatch](<https://github.com/tpope/vim-dispatch>) Vim plugin is installed. `vim-nose` leverage the work done by Tim Pope (a.k.a **tpope**). It is built on top of `vim-dispatch`.
- [nose](https://nose.readthedocs.org/en/latest/) installed in your python (virtual) environment.

Features
========

- Expose commands to run python tests inside Vim (run current test, run current test case, ...)
- Run tests asynchronously (thank you `vim-dispatch`!).
- Output tests results in `quickfix` window for easy navigation.
- `VirtualEnv` configuration and/or auto detection.

Usage
=====

TBD

License
=======

Copyright © Pascal Lalancette. Distributed under the same terms as Vim itself. See :help license.