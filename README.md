<!-- TOC -->
* [OpenStudioLandscapes Template Module](#openstudiolandscapes-template-module)
  * [Guide: How to use the template](#guide-how-to-use-the-template)
* [Install](#install)
  * [Create venv](#create-venv)
  * [Install OpenStudioLandscapes-Your-New-Module into venv](#install-openstudiolandscapes-your-new-module-into-venv)
  * [Install OpenStudioLandscapes-Your-New-Module into OpenStudioLandscapes venv](#install-openstudiolandscapes-your-new-module-into-openstudiolandscapes-venv)
  * [OpenStudioLandscapes/src/OpenStudioLandscapes/engine](#openstudiolandscapessrcopenstudiolandscapesengine)
    * [constants.py](#constantspy)
* [PyScaffold](#pyscaffold)
  * [Create Module](#create-module)
    * [PyScaffold](#pyscaffold-1)
    * [`pyproject.toml`](#pyprojecttoml)
    * [`setup.cfg`](#setupcfg)
<!-- TOC -->

---

# OpenStudioLandscapes Template Module

Source template version: [`1.8.0`](https://github.com/michimussato/OpenStudioLandscapes-Template/tree/1.8.0)

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

## Create venv

```shell
cd OpenStudioLandscapes-Your-New-Module
python3.11 -m venv .venv
pip install -U setuptools
```

## Install OpenStudioLandscapes-Your-New-Module into venv

```shell
cd OpenStudioLandscapes-Your-New-Module
pip install -e .[dev]
```

## Install OpenStudioLandscapes-Your-New-Module into OpenStudioLandscapes venv

```shell
cd OpenStudioLandscapes
pip install -e ../OpenStudioLandscapes-Your-New-Module[dev]
```

## OpenStudioLandscapes/src/OpenStudioLandscapes/engine

### constants.py

```python
THIRD_PARTY.append(
   {
      "enabled": True,
      "module": "OpenStudioLandscapes.Your_New_Module.definitions",
      "compose_scope": ComposeScope.DEFAULT,
   }
)
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
[tool.dagster]
module_name = "OpenStudioLandscapes.Your_New_Module.definitions"
code_location_name = "OpenStudioLandscapes-Your-New-Module"
```

### `setup.cfg`

```
[metadata]
platforms = Linux

[options]
python_requires = >=3.11

install_requires =
    [...]
    dagster==1.9.11
    gitpython
    PyYAML
    python-on-whales
    # yaml_tags.overrides:
    docker-compose-graph @ git+https://github.com/michimussato/docker-compose-graph.git
    # Todo: Will work when released:
    # OpenStudioLandscapes @ git+https://github.com/michimussato/OpenStudioLandscapes
    [...]

[options.extras_require]

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
    
    
dev =
    dagster-webserver==1.9.11
    OpenStudioLandscapes-Your-New-Module[testing]

[tool:pytest]
norecursedirs =
    dist
    build
    .nox

[flake8]
exclude =
    .nox
    .svg
    build
    dist
    .eggs
    docs/conf.py

[pyscaffold]
package = Your-New-Module
extensions =
    namespace
namespace = OpenStudioLandscapes
```
