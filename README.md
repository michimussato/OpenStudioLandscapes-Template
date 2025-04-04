[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/_images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

---

<!-- TOC -->
* [OpenStudioLandscapes Template Module](#openstudiolandscapes-template-module)
  * [Guide: How to use the template](#guide-how-to-use-the-template)
* [Install](#install)
* [PyScaffold](#pyscaffold)
  * [Create Module](#create-module)
    * [PyScaffold Command](#pyscaffold-command)
    * [`pyproject.toml`](#pyprojecttoml)
    * [`setup.cfg`](#setupcfg)
<!-- TOC -->

---

# OpenStudioLandscapes Template Module

Source template version: [`2.0.1`](https://github.com/michimussato/OpenStudioLandscapes-Template/tree/2.0.1)

## Guide: How to use the template

1. Create your new Git repo on Github, 
   i.e. yourlogin/OpenStudioLandscapes-YourModule
2. Clone OpenStudioLandscapes-Template
   ```shell
   git clone https://github.com/michimussato/OpenStudioLandscapes-Template.git OpenStudioLandscapes-Your-New-Module
   ```
3. Rename Git remote
   1. ```shell
      cd OpenStudioLandscapes-Your-New-Module
      rm -rf .venv
      rm -rf .idea
      rm -rf .git && git init --initial-branch=main
      ```
   2. Rename src directory
      ```shell
      mv src/OpenStudioLandscapes/Template src/OpenStudioLandscapes/Your_New_Module
      ```
   3. ```shell
      git remote add origin https://github.com/yourlogin/OpenStudioLandscapes-Your-New-Module.git
      git branch -M main
      ```
   4. Create initial commit
      ```shell
      git add --all
      git commit -m "initial commit"
      ```
   5. Initial Push
      ```shell
      git push -u origin main
      ```
4. Rename Template
   1. OpenStudioLandscapes-Template -> OpenStudioLandscapes-Your-New-Module
      - `mv OpenStudioTemplates-Temkplate OpenStudioLandscapes-Your-New-Module`
   2. All occurrences of `<Your-New-Module>` -> `Your-Module`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/<Your-New-Module>/Your-Module/g'`
   3. All occurrences of `<Your_New_Module>` -> `Your_Module`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/<Your_New_Module>/Your_Module/g'`
   4. All occurrences of `John Doe` -> `Your Name`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/John Doe/Your Name/g'`
   5. All occurrences of `john.doe@acme.com` -> `your.name@email.com`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/john.doe@acme.com/your.name@email.com/g'`
   6. All occurrences of `20XX` -> `2025`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/20XX/$(date +%Y)/g'`
   7. All occurrences of `YourLogin` -> `your_github_login`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/YourLogin/your_github_login/g'`
   8. All occurrences of `GROUP = "Template"` -> `GROUP = "Your_New_Module"`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/GROUP = "Template"/GROUP = "Your_New_Module"/g'`
   9. All occurrences of `<USERNAME>` -> `your_github_login`
      - `Ctrl+Shift+R` in PyCharm
      - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/<USERNAME>/your_github_login/g'`
   10. All occurrences of `"compose_template"` -> `"compose_your_new_module"`
       - `Ctrl+Shift+R` in PyCharm
       - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/"compose_template"/"compose_your_new_module"/g'`
   11. All occurrences of `service_name = "template"` -> `service_name = "your_new_module"`
       - `Ctrl+Shift+R` in PyCharm
       - `find OpenStudioLandscapes-Your-New-Module/ -type f | xargs sed -i 's/<USERNAME>/your_github_login/g'`
   12. Revert `README.md`
       - `git checkout -f README.md`
   13. Commit changes
       ```shell
       git add --all
       git commit -m "Initial Changes"
       ```
   14. Initial Push
       ```shell
       git push -u origin main
       ```

# Install

Installation instructions will be generated automatically. Once all
preliminary steps were executed, the following command will generate
the new `READMD.md` for `Your-New-Module`:

Todo: Create CLI package

```
python3.11 src/OpenStudioLandscapes/Your_New_Module/utils/generate_readme.py
```

# PyScaffold

If you want to start from scratch, a good starting point would be to create
a new package using `PyScaffold`

## Create Module

### PyScaffold Command

```
pip install PyScaffold
putup --package Your_New_Module --force --namespace OpenStudioLandscapes --no-skeleton OpenStudioLandscapes-Your-New-Module
```

### `pyproject.toml`

```
[build-system]
# AVOID CHANGING REQUIRES: IT WILL BE UPDATED BY PYSCAFFOLD!
requires = ["setuptools>=46.1.0", "setuptools_scm[toml]>=5"]
build-backend = "setuptools.build_meta"

[tool.setuptools_scm]
# For smarter version schemes and other configuration options,
# check out https://github.com/pypa/setuptools_scm
version_scheme = "no-guess-dev"

[tool.dagster]
module_name = "OpenStudioLandscapes.Your_New_Module.definitions"
code_location_name = "OpenStudioLandscapes-Your-New-Module"
```

### `setup.cfg`

```
# This file is used to configure your project.
# Read more about the various options under:
# https://setuptools.pypa.io/en/latest/userguide/declarative_config.html
# https://setuptools.pypa.io/en/latest/references/keywords.html

[metadata]
name = OpenStudioLandscapes-Your-New-Module
description = Add a short description here!
author = John Doe
author_email = john.doe@acme.com
license = MIT
license_files = LICENSE.txt
long_description = file: README.rst
long_description_content_type = text/x-rst; charset=UTF-8
url = https://github.com/pyscaffold/pyscaffold/
# Add here related links, for example:
project_urls =
    Documentation = https://pyscaffold.org/
#    Source = https://github.com/pyscaffold/pyscaffold/
#    Changelog = https://pyscaffold.org/en/latest/changelog.html
#    Tracker = https://github.com/pyscaffold/pyscaffold/issues
#    Conda-Forge = https://anaconda.org/conda-forge/pyscaffold
#    Download = https://pypi.org/project/PyScaffold/#files
#    Twitter = https://twitter.com/PyScaffold

# Change if running only on Windows, Mac or Linux (comma-separated)
platforms = Linux

# Add here all kinds of additional classifiers as defined under
# https://pypi.org/classifiers/
classifiers =
    Development Status :: 4 - Beta
    Programming Language :: Python


[options]
zip_safe = False
packages = find_namespace:
include_package_data = True
package_dir =
    =src

# Require a min/specific Python version (comma-separated conditions)
python_requires = >=3.11

# Add here dependencies of your project (line-separated), e.g. requests>=2.2,<3.0.
# Version specifiers like >=2.2,<3.0 avoid problems due to API changes in
# new major versions. This works if the required packages follow Semantic Versioning.
# For more information, check out https://semver.org/.
install_requires =
    importlib-metadata; python_version<"3.8"
    dagster==1.9.11
    gitpython
    PyYAML
    python-on-whales
    # yaml_tags.overrides:
    docker-compose-graph @ git+https://github.com/michimussato/docker-compose-graph.git
    # Todo: Will work when released:
    # OpenStudioLandscapes @ git+https://github.com/michimussato/OpenStudioLandscapes


[options.packages.find]
where = src
exclude =
    tests

[options.extras_require]
# Add here additional requirements for extra features, to install with:
# `pip install OpenStudioLandscapes-Your-New-Module[PDF]` like:
# PDF = ReportLab; RXP

# Add here test requirements (semicolon/line-separated)
testing =
    setuptools
    pytest
    pytest-cov

graphviz =
    graphviz
    pipdeptree

docs =
    sphinx
    myst_parser
    OpenStudioLandscapes-Your-New-Module[graphviz]
    # https://github.com/omnilib/sphinx-mdinclude
    # sphinx-mdinclude @ git+https://github.com/michimussato/sphinx-mdinclude.git
    sphinx-mdinclude @ git+https://github.com/omnilib/sphinx-mdinclude.git

sbom =
    OpenStudioLandscapes-Your-New-Module[graphviz]
    cyclonedx-bom

lint =
    black
    isort
    pre-commit
    pylint

coverage =
    coverage
    pytest

nox =
    OpenStudioLandscapes-Your-New-Module[testing]
    nox

dev =
    OpenStudioLandscapes-Your-New-Module[testing]
    OpenStudioLandscapes-Your-New-Module[docs]
    OpenStudioLandscapes-Your-New-Module[lint]
    OpenStudioLandscapes-Your-New-Module[nox]
    OpenStudioLandscapes-Your-New-Module[sbom]
    OpenStudioLandscapes-Your-New-Module[coverage]
    dagster-webserver==1.9.11
    snakemd

[options.entry_points]
# Add here console scripts like:
# console_scripts =
#     script_name = OpenStudioLandscapes.Your_New_Module.module:function
# For example:
# console_scripts =
#     fibonacci = OpenStudioLandscapes.Your_New_Module.skeleton:run
# And any other entry points, for example:
# pyscaffold.cli =
#     awesome = pyscaffoldext.awesome.extension:AwesomeExtension

[tool:pytest]
# Specify command line options as you would do when invoking pytest directly.
# e.g. --cov-report html (or xml) for html/xml output or --junitxml junit.xml
# in order to write a coverage file that can be read by Jenkins.
# CAUTION: --cov flags may prohibit setting breakpoints while debugging.
#          Comment those flags to avoid this pytest issue.
addopts =
    --cov OpenStudioLandscapes.Your_New_Module --cov-report term-missing
    --verbose
norecursedirs =
    dist
    build
    .nox
testpaths = tests
# Use pytest markers to select/deselect specific tests
# markers =
#     slow: mark tests as slow (deselect with '-m "not slow"')
#     system: mark end-to-end system tests

[devpi:upload]
# Options for the devpi: PyPI server and packaging tool
# VCS export must be deactivated since we are using setuptools-scm
no_vcs = 1
formats = bdist_wheel

[flake8]
# Some sane defaults for the code style checker flake8
max_line_length = 88
extend_ignore = E203, W503
# ^  Black-compatible
#    E203 and W503 have edge cases handled by black
exclude =
    .nox
    .svg
    build
    dist
    .eggs
    docs/conf.py

[pyscaffold]
# PyScaffold's parameters when the project was created.
# This will be used when updating. Do not change!
version = 4.6
package = Your-New-Module
extensions =
    namespace
namespace = OpenStudioLandscapes
```
