# git-reviewers

[ ![Codeship Status for albertyw/git-reviewers](https://app.codeship.com/projects/17913cd0-3524-0135-2853-7e1f21584d06/status?branch=master)](https://app.codeship.com/projects/227040)
[![Dependency Status](https://gemnasium.com/badges/github.com/albertyw/git-reviewers.svg)](https://gemnasium.com/github.com/albertyw/git-reviewers)
[![Code Climate](https://codeclimate.com/github/albertyw/git-reviewers/badges/gpa.svg)](https://codeclimate.com/github/albertyw/git-reviewers)
[![Test Coverage](https://codeclimate.com/github/albertyw/git-reviewers/badges/coverage.svg)](https://codeclimate.com/github/albertyw/git-reviewers/coverage)

Tool to suggest code reviewers for your code depending on your diff

Development
-----------

```bash
pip install -r requirements-test.txt
coverage run setup.py test
coverage report
flake8
```

Publishing
----------

```bash
sudo apt-get install pandoc
pip install twine pypandoc
python setup.py sdist bdist_wheel
twine upload dist/*
```
