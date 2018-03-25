CHANGELOG.md
============

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
