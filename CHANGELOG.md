CHANGELOG.md
============

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
