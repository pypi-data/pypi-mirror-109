<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED IN THE NAMESPACE ROOT PACKAGE. CHANGES HAVE TO BE DONE THERE.
-->
# valid portion of ae namespace package

[![GitLabPipeline](https://img.shields.io/gitlab/pipeline/ae-group/ae_valid/master?logo=python)](
    https://gitlab.com/ae-group/ae_valid)
[![PyPIVersion](https://img.shields.io/pypi/v/ae_valid)](
    https://pypi.org/project/ae-valid/#history)

>The portions (modules and sub-packages) of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes to develop
full-featured applications with Python.

[![Coverage](https://ae-group.gitlab.io/ae_valid/coverage.svg)](
    https://ae-group.gitlab.io/ae_valid/coverage/ae_valid_py.html)
[![MyPyPrecision](https://ae-group.gitlab.io/ae_valid/mypy.svg)](
    https://ae-group.gitlab.io/ae_valid/lineprecision.txt)
[![PyLintScore](https://ae-group.gitlab.io/ae_valid/pylint.svg)](
    https://ae-group.gitlab.io/ae_valid/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_valid)](
    https://pypi.org/project/ae-valid/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_valid)](
    https://pypi.org/project/ae-valid/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_valid)](
    https://pypi.org/project/ae-valid/)
[![PyPIFormat](https://img.shields.io/pypi/format/ae_valid)](
    https://pypi.org/project/ae-valid/)
[![PyPIStatus](https://img.shields.io/pypi/status/ae_valid)](
    https://libraries.io/pypi/ae-valid)
[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_valid)](
    https://pypi.org/project/ae-valid/#files)


## installation


execute the following command to use the ae.valid module in your
application. it will install ae.valid into your python (virtual) environment:
 
```shell script
pip install ae-valid
```

if you instead want to contribute to this portion then first fork
[the ae_valid repository at GitLab](https://gitlab.com/ae-group/ae_valid "ae.valid code repository"),
then pull it to your machine and finally execute the following command in the root folder
of this repository (ae_valid):

```shell script
pip install -e .[dev]
```

the last command will install this module portion into your virtual environment, along with
the tools you need to develop and run tests or to extend the portion documentation.
to contribute only to the unit tests or to the documentation of this portion replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

more info on the features and usage of this portion are available at
[ReadTheDocs](https://ae.readthedocs.io/en/latest/_autosummary/ae.valid.html#module-ae.valid
"ae_valid documentation").

<!-- common files version 0.2.77 deployed version 0.2.2 (with 0.2.77)
     to https://gitlab.com/ae-group as ae_valid module as well as
     to https://ae-group.gitlab.io with CI check results as well as
     to https://pypi.org/project/ae-valid as namespace portion ae-valid.
-->
