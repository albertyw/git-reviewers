CHANGELOG.md
============

v0.13.0 (2019-03-25)
--------------------

 - Add ability to configure base branch with `-b`
 - Optimizes git shortlog to be faster
 - Dependency updates


v0.12.2 (2019-02-22)
--------------------

 - Optimizes FindHistoricalReviewers to look over the entire repository at once
   (Fixes https://github.com/albertyw/git-reviewers/issues/40)


v0.12.1 (2019-02-05)
--------------------

 - Fixed a bug where too many usernames would cause arc to lock up querying phabricator
 - Updated README
 - Removed support for python 3.4 and 3.5
 - Dependency updates


v0.12.0 (2019-02-03)
--------------------

 - Changed entrypoint from git_reviewers to git-reviewers
 - Added support for reading the default config file of the current user
 - Refactors to reading configs
 - Backfilled some mypy type annotations
 - Updated dependencies


v0.11.1 (2018-12-26)
--------------------

 - Make phabricator user activation check faster
 - Add documentation in readme about configuration file
 - Fix package description syntax
 - Dependency updates


v0.11.0 (2018-11-26)
--------------------

 - Add json config files
 - Updates to test dependencies


v0.10.0 (2018-10-14)
--------------------

 - Add ability to look at entire repository history when computing reviewers


v0.9.0 (2018-07-03)
-------------------

 - Add verbose mode
 - Fixes for copying data to clipboard
 - Update test dependencies


v0.8.0 (2018-03-27)
-------------------

 - Refactors and optimizations


v0.7.0 (2018-03-24)
-------------------

 - Add homebrew
 - Be able to work with deleted files
 - Prune users that are disabled in phabricator
 - Update test dependencies


v0.6.1 (2017-12-25)
-------------------

 - Make install.sh accept a path for reviewers.py


v0.6.0 (2017-12-17)
-------------------

 - Remove `FindDiffLogReviewers` because it overlaps with `FindLogReviewers`
 - Remove `--path` from installation script and readme
 - Update readme
 - Update mypy dependency


v0.5.0 (2017-11-18)
-------------------

 - Add `--copy` flag to copy reviewers to OS clipboard
 - Various refactors and minor fixes


v0.4.0 (2017-11-13)
-------------------

 - Remove no-op `--path` argument
 - Add an `--ignore` argument for ignoring possible reviewers
 - Weight reviewers by the frequency they show up in previous git history


v0.3.1 (2017-11-12)
-------------------

 - Limit to 7 reviewers
 - Support weighting/sorting reviewers
 - Add PEP-484 type annotations for mypy


v0.3.0 (2017-10-30)
-------------------

 - Get reviewers based on arcanist reviewers in commit messages
 - Remove uber-specific logic
 - Add `-v` to read git-reviewer version


v0.2.0 (2017-10-23)
-------------------

 - Be able to gather reviewers based on the changed files compared to master branch
 - Updated testing dependencies
 - Lots of refactors, fixes


v0.1.2 (2017-10-20)
-------------------

 - Lots of refactors, fixes


v0.1.1 (2017-10-17)
-------------------

 - Reformat README to RST
 - Add installation script


v0.1.0 (2017-06-24)
-------------------

 - Make uber behavior be toggleable and off by default
 - Select reviewers based on the files that were changed


v0.0.2 (2017-06-20)
-------------------

 - Add initial support for finding repository committers as a list of reviewers
