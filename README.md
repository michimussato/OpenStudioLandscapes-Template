[![ Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://github.com/michimussato/OpenStudioLandscapes)

***

1. [Feature: OpenStudioLandscapes-Template](#feature-openstudiolandscapes-template)
   1. [Brief](#brief)
   2. [Install](#install)
   3. [Configure](#configure)
      1. [Default Configuration](#default-configuration)
2. [Create new Feature from this Template](#create-new-feature-from-this-template)
   1. [Create a new repository from this Template](#create-a-new-repository-from-this-template)
   2. [Clone new Feature to your local drive](#clone-new-feature-to-your-local-drive)
   3. [Replace `Template` occurrences in `OpenStudioLandscapes-NewFeature`](#replace-template-occurrences-in-openstudiolandscapes-newfeature)
   4. [Create `pyproject.toml`](#create-pyprojecttoml)
   5. [Commit your initial Setup](#commit-your-initial-setup)
   6. [Tag `OpenStudioLandscapesUtil` Repos](#tag-openstudiolandscapesutil-repos)
   7. [Enable OpenStudioLandscapes-NewFeature in the Engine](#enable-openstudiolandscapes-newfeature-in-the-engine)
   8. [Known Issues](#known-issues)
      1. [`no command specified`](#no-command-specified)
3. [Community](#community)

***

This `README.md` was dynamically created with [OpenStudioLandscapesUtil-ReadmeGenerator](https://github.com/michimussato/OpenStudioLandscapesUtil-ReadmeGenerator).

***

# Feature: OpenStudioLandscapes-Template

## Brief

This is an extension to the OpenStudioLandscapes ecosystem. The full documentation of OpenStudioLandscapes is available [here](https://github.com/michimussato/OpenStudioLandscapes).

> [!NOTE]
> 
> You feel like writing your own Feature? Go and check out the 
> [OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template).

## Install

Clone this repository into `OpenStudioLandscapes/.features` (assuming the current working directory to be the Git repository root `./OpenStudioLandscapes`):

```shell
git -C ./.features clone https://github.com/michimussato/OpenStudioLandscapes-Template.git
# Check out a specific branch with:
# List branches: 
# git -C ./.features/OpenStudioLandscapes-Template branch -a
# Checkout branch: 
# git -C ./.features/OpenStudioLandscapes-Template checkout <branch>
```

Install into OpenStudioLandscapes `venv` (`./OpenStudioLandscapes/.venv`):

```shell
source .venv/bin/activate
# python -m pip install --upgrade pip setuptools
# the following removes the `openstudiolandscapes` executable for now (will be fixed soon)
pip install -e "./.features/OpenStudioLandscapes-Template"
# so, re-install `OpenStudioLandscapes` engine:
pip install -e "."
```

For more info on `pip` see [VCS Support of `pip`](https://pip.pypa.io/en/stable/topics/vcs-support/).

## Configure

OpenStudioLandscapes will search for a local config store. The default location is `~/.config/OpenStudioLandscapes/config-store/` but you can specify a different location if you need to.

A local config store location will be created if it doesn't exist, together with the `config.yml` files for each individual Feature.

> [!TIP]
> 
> The config store root will be initialized as a local Git
> controlled repository. This makes it easy to track changes
> you made to the `config.yml`.

> [!TIP]
> 
> To specify a config store location different than
> the default, you can do so be setting the environment variable
> `OPENSTUDIOLANDSCAPES__CONFIGSTORE_ROOT`:
> 
> ```shell
> OPENSTUDIOLANDSCAPES__CONFIGSTORE_ROOT="~/.config/OpenStudioLandscapes/my-custom-config-store"
> ```

The following settings are available in `OpenStudioLandscapes-Template` and are based on [`OpenStudioLandscapes-Template/tree/main/OpenStudioLandscapes/Template/config/models.py`](https://github.com/michimussato/OpenStudioLandscapes-Template/tree/main/OpenStudioLandscapes/Template/config/models.py).

### Default Configuration


<details>
<summary><code>config.yml</code></summary>


```yaml
# ===
# env
# ---
#
# Type: typing.Dict
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# =============
# config_engine
# -------------
#
# Type: <class 'OpenStudioLandscapes.engine.config.models.ConfigEngine'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# =============
# config_parent
# -------------
#
# Type: <class 'OpenStudioLandscapes.engine.config.models.FeatureBaseModel'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ============
# distribution
# ------------
#
# Type: <class 'importlib.metadata.Distribution'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         None
# Description:
#     None
# Required:
#     False
# Examples:
#     None


# ==========
# group_name
# ----------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         True
#     Description:
#         Dagster Group name. This will represent the group node name. See https://docs.dagster.io/api/dagster/assets for more information
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
group_name: OpenStudioLandscapes_Template


# ============
# key_prefixes
# ------------
#
# Type: typing.List[str]
# Base Class Info:
#     Required:
#         True
#     Description:
#         Dagster Asset key prefixes. This will be reflected in the nesting (directory structure) of the Asset. See https://docs.dagster.io/api/dagster/assets for more information
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
key_prefixes:
- OpenStudioLandscapes_Template


# =======
# enabled
# -------
#
# Type: <class 'bool'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         Whether the Feature is enabled or not.
#     Default value:
#         True
# Description:
#     None
# Required:
#     False
# Examples:
#     None
enabled: false


# =============
# compose_scope
# -------------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         None
#     Default value:
#         default
# Description:
#     None
# Required:
#     False
# Examples:
#     ['default', 'license_server', 'worker']


# ============
# feature_name
# ------------
#
# Type: <class 'str'>
# Base Class Info:
#     Required:
#         True
#     Description:
#         The name of the feature. It is derived from the `OpenStudioLandscapes.<Feature>.dist` attribute.
#     Default value:
#         PydanticUndefined
# Description:
#     None
# Required:
#     False
# Examples:
#     None
feature_name: OpenStudioLandscapes-Template


# ==============
# docker_compose
# --------------
#
# Type: <class 'pathlib.Path'>
# Base Class Info:
#     Required:
#         False
#     Description:
#         The path to the `docker-compose.yml` file.
#     Default value:
#         {DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/docker_compose/docker-compose.yml
# Description:
#     The path to the `docker-compose.yml` file.
# Required:
#     False
# Examples:
#     None


# =================
# ENV_VAR_PORT_HOST
# -----------------
#
# Type: <class 'int'>
# Description:
#     The host port.
# Required:
#     False
# Examples:
#     None
ENV_VAR_PORT_HOST: 1234


# ======================
# ENV_VAR_PORT_CONTAINER
# ----------------------
#
# Type: <class 'int'>
# Description:
#     The Ayon container port.
# Required:
#     False
# Examples:
#     None
ENV_VAR_PORT_CONTAINER: 2345


# ==============
# MOUNTED_VOLUME
# --------------
#
# Type: <class 'pathlib.Path'>
# Description:
#     The host side mounted volume.
# Required:
#     False
# Examples:
#     None
MOUNTED_VOLUME: '{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/volume'
```


</details>


***

# Create new Feature from this Template

[![Logo OpenStudioLandscapes ](https://github.com/michimussato/OpenStudioLandscapes/raw/main/media/images/logo128.png)](https://www.url.com)

## Create a new repository from this Template

Click `Use this template` and select `Create a new repository`

![Create a new repository ](media/images/use_template.png)

And fill in information as needed by specifying the `Repository name *` of the OpenStudioLandscapes Feature (i.e. `OpenStudioLandscapes-NewFeature`):

![Create a new repository ](media/images/create_repository.png)

## Clone new Feature to your local drive

Clone the new Feature into the `.features` directory of your local `OpenStudioLandscapes` clone:

```generic
cd /to/your/git/repos/OpenStudioLandscapes/.features
git clone <GIT_REPOSITORY_URL>
```

## Replace `Template` occurrences in `OpenStudioLandscapes-NewFeature`

Rename the package directory from `Template` to `NewFeature`:

```generic
NEW_FEATURE="NewFeature"

cd /to/your/git/repos/OpenStudioLandscapes/.features/OpenStudioLandscapes-${NEW_FEATURE}
mv src/OpenStudioLandscapes/Template src/OpenStudioLandscapes/${NEW_FEATURE}
```

Rename all occurrences of `template` in your new Feature with the correct name in the following files:

- update [`./pyproject.toml`](./pyproject.toml)
- update `./pyproject_layer.yaml`
- update `./src/OpenStudioLandscapes/${NEW_FEATURE}/__init__.py`
- update `./src/OpenStudioLandscapes/${NEW_FEATURE}/assets.py`
- update `./src/OpenStudioLandscapes/${NEW_FEATURE}/constants.py`
- update `./src/OpenStudioLandscapes/${NEW_FEATURE}/definitions.py`
- update `./src/OpenStudioLandscapes/${NEW_FEATURE}/readme_feature.py` [`snakemd` Documentation](https://www.snakemd.io/en/latest/)
- update `/.coveragerc`
- remove media `rm ./media/images/*.*`
- remove nox reports `rm ./.nox/*.*`
- remove sbom reports `rm ./.sbom/*.*`

## Create `pyproject.toml`

```generic
nox -session "readme(OpenStudioLandscapes-<FEATURE>)"
```

## Commit your initial Setup

Commit all changes to Git:

```generic
git add *
git commit -m "Initial Setup"
git push
```

## Tag `OpenStudioLandscapesUtil` Repos

- [OpenStudioLandscapesUtil-HarborCLI](https://github.com/michimussato/OpenStudioLandscapesUtil-HarborCLI?tab=readme-ov-file#tagging)
- [OpenStudioLandscapesUtil-ReadmeGenerator](https://github.com/michimussato/OpenStudioLandscapesUtil-ReadmeGenerator?tab=readme-ov-file#tagging)

## Enable OpenStudioLandscapes-NewFeature in the Engine

Commit all changes to Git:

```generic
cd /to/your/git/repos/OpenStudioLandscapes
source .venv/bin/activate
pip install --editable .features/OpenStudioLandscapes-${NEW_FEATURE}[dev]
pip install --editable .[dev]
```

Edit the `OpenStudioLandscapes.engine` to use your new Feature:

- update `OpenStudioLandscapes/.env`
- update `OpenStudioLandscapes/src/OpenStudioLandscapes/engine/features.py`
- update `OpenStudioLandscapes/README.md#current-feature-statuses`

## Known Issues

### `no command specified`

`OpenStudioLandscapes-Template` can't be launched as a Feature in a Landscape. If you do, this is the error message you will be presented with:

```shell
$ /home/michael/git/repos/OpenStudioLandscapes/.landscapes/2025-10-20-12-51-39-68351d36801042cb943f1675e611e3c0/ComposeScope_default__ComposeScope_default/ComposeScope_default__DOCKER_COMPOSE/docker_compose/docker_compose_up.sh
~/git/repos/OpenStudioLandscapes/.landscapes/2025-10-20-12-51-39-68351d36801042cb943f1675e611e3c0/ComposeScope_default__ComposeScope_default/ComposeScope_default__DOCKER_COMPOSE/docker_compose ~
Working Directory: /home/michael/git/repos/OpenStudioLandscapes/.landscapes/2025-10-20-12-51-39-68351d36801042cb943f1675e611e3c0/ComposeScope_default__ComposeScope_default/ComposeScope_default__DOCKER_COMPOSE/docker_compose
Sourcing ../../../../2025-10-20-12-51-39-68351d36801042cb943f1675e611e3c0/.overrides file...
Sourced successfully.
 Container hbbs--2025-10-20-12-51-39-68351d36801042cb943f1675e611e3c0  Creating
 Container dagster--2025-10-20-12-51-39-68351d36801042cb943f1675e611e3c0  Creating
 Container template--2025-10-20-12-51-39-68351d36801042cb943f1675e611e3c0  Creating
 Container mongo-express-10-2--2025-10-20-12-51-39-68351d36801042cb943f1675e611e3c0  Creating
 Container repository-installer-10-2--2025-10-20-12-51-39-68351d36801042cb943f1675e611e3c0  Creating
 Container ayon-server--2025-10-20-12-51-39-68351d36801042cb943f1675e611e3c0  Creating
 Container opencue-flyway--2025-10-20-12-51-39-68351d36801042cb943f1675e611e3c0  Creating
 Container kitsu--2025-10-20-12-51-39-68351d36801042cb943f1675e611e3c0  Creating
 Container template--2025-10-20-12-51-39-68351d36801042cb943f1675e611e3c0  Error response from daemon: no command specified
Error response from daemon: no command specified
~
```

***

# Community

| Feature                                   | GitHub                                                                                                                                                 | Discord                                                                      |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| OpenStudioLandscapes                      | [https://github.com/michimussato/OpenStudioLandscapes](https://github.com/michimussato/OpenStudioLandscapes)                                           | [# openstudiolandscapes-general](https://discord.gg/F6bDRWsHac)              |
| OpenStudioLandscapes-Ayon                 | [https://github.com/michimussato/OpenStudioLandscapes-Ayon](https://github.com/michimussato/OpenStudioLandscapes-Ayon)                                 | [# openstudiolandscapes-ayon](https://discord.gg/gd6etWAF3v)                 |
| OpenStudioLandscapes-Dagster              | [https://github.com/michimussato/OpenStudioLandscapes-Dagster](https://github.com/michimussato/OpenStudioLandscapes-Dagster)                           | [# openstudiolandscapes-dagster](https://discord.gg/jwB3DwmKvs)              |
| OpenStudioLandscapes-Deadline-10-2        | [https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2)               | [# openstudiolandscapes-deadline-10-2](https://discord.gg/p2UjxHk4Y3)        |
| OpenStudioLandscapes-Deadline-10-2-Worker | [https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2-Worker](https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2-Worker) | [# openstudiolandscapes-deadline-10-2-worker](https://discord.gg/ttkbfkzUmf) |
| OpenStudioLandscapes-Flamenco             | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco](https://github.com/michimussato/OpenStudioLandscapes-Flamenco)                         | [# openstudiolandscapes-flamenco](https://discord.gg/EPrX5fzBCf)             |
| OpenStudioLandscapes-Flamenco-Worker      | [https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker](https://github.com/michimussato/OpenStudioLandscapes-Flamenco-Worker)           | [# openstudiolandscapes-flamenco-worker](https://discord.gg/Sa2zFqSc4p)      |
| OpenStudioLandscapes-Grafana              | [https://github.com/michimussato/OpenStudioLandscapes-Grafana](https://github.com/michimussato/OpenStudioLandscapes-Grafana)                           | [# openstudiolandscapes-grafana](https://discord.gg/gEDQ8vJWDb)              |
| OpenStudioLandscapes-Kitsu                | [https://github.com/michimussato/OpenStudioLandscapes-Kitsu](https://github.com/michimussato/OpenStudioLandscapes-Kitsu)                               | [# openstudiolandscapes-kitsu](https://discord.gg/6cc6mkReJ7)                |
| OpenStudioLandscapes-LikeC4               | [https://github.com/michimussato/OpenStudioLandscapes-LikeC4](https://github.com/michimussato/OpenStudioLandscapes-LikeC4)                             | [# openstudiolandscapes-likec4](https://discord.gg/qAYYsKYF6V)               |
| OpenStudioLandscapes-OpenCue              | [https://github.com/michimussato/OpenStudioLandscapes-OpenCue](https://github.com/michimussato/OpenStudioLandscapes-OpenCue)                           | [# openstudiolandscapes-opencue](https://discord.gg/3DdCZKkVyZ)              |
| OpenStudioLandscapes-OpenCue-Worker       | [https://github.com/michimussato/OpenStudioLandscapes-OpenCue-Worker](https://github.com/michimussato/OpenStudioLandscapes-OpenCue-Worker)             | [# openstudiolandscapes-opencue-worker](https://discord.gg/n9fxxhHa3V)       |
| OpenStudioLandscapes-RustDeskServer       | [https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer](https://github.com/michimussato/OpenStudioLandscapes-RustDeskServer)             | [# openstudiolandscapes-rustdeskserver](https://discord.gg/nJ8Ffd2xY3)       |
| OpenStudioLandscapes-Syncthing            | [https://github.com/michimussato/OpenStudioLandscapes-Syncthing](https://github.com/michimussato/OpenStudioLandscapes-Syncthing)                       | [# openstudiolandscapes-syncthing](https://discord.gg/upb9MCqb3X)            |
| OpenStudioLandscapes-Template             | [https://github.com/michimussato/OpenStudioLandscapes-Template](https://github.com/michimussato/OpenStudioLandscapes-Template)                         | [# openstudiolandscapes-template](https://discord.gg/J59GYp3Wpy)             |
| OpenStudioLandscapes-VERT                 | [https://github.com/michimussato/OpenStudioLandscapes-VERT](https://github.com/michimussato/OpenStudioLandscapes-VERT)                                 | [# openstudiolandscapes-vert](https://discord.gg/EPrX5fzBCf)                 |
| OpenStudioLandscapes-filebrowser          | [https://github.com/michimussato/OpenStudioLandscapes-filebrowser](https://github.com/michimussato/OpenStudioLandscapes-filebrowser)                   | [# openstudiolandscapes-filebrowser](https://discord.gg/stzNsZBmwk)          |

To follow up on the previous LinkedIn publications, visit:

- [OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/company/106731439/).
- [Search for tag #OpenStudioLandscapes on LinkedIn](https://www.linkedin.com/search/results/all/?keywords=%23openstudiolandscapes).

***

Last changed: **2025-12-30 01:27:25 UTC**