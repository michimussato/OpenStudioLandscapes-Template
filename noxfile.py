import json
import shlex
import shutil
import os
import nox
import re
import pathlib
import requests
import logging
import tarfile
import platform
from typing import Tuple

import yaml

logging.basicConfig(level=logging.DEBUG)


DOCKER_PROGRESS = [
    "auto",
    "quiet",
    "plain",
    "tty",
    "rawjson",
][2]


def _get_terminal_size() -> Tuple[int, int]:
    # https://stackoverflow.com/a/14422538
    # https://stackoverflow.com/a/18243550
    cols, rows = shutil.get_terminal_size((80, 20))
    return cols, rows


def download(
    url: str,
    dest_folder: pathlib.Path,
) -> pathlib.Path:
    if not dest_folder.exists():
        dest_folder.mkdir(
            parents=True, exist_ok=True
        )  # create folder if it does not exist

    filename = url.split("/")[-1].replace(" ", "_")  # be careful with file names
    file_path = dest_folder / filename

    r = requests.get(url, stream=True)
    if r.ok:
        logging.info("Saving to %s" % file_path.absolute().as_posix())
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
        return file_path
    else:  # HTTP status code 4XX/5XX
        raise Exception(
            "Download failed: status code {}\n{}".format(r.status_code, r.text)
        )


# nox Configuration & API
# https://nox.thea.codes/en/stable/config.html
# # nox.sessions.Session.run
# https://nox.thea.codes/en/stable/config.html#nox.sessions.Session.run


# https://www.youtube.com/watch?v=ImBvrDvK-1U&ab_channel=HynekSchlawack
# https://codewitholi.com/_posts/python-nox-automation/


# reuse_existing_virtualenvs:
# global: nox.options.reuse_existing_virtualenvs = True
nox.options.reuse_existing_virtualenvs = False
# per session: @nox.session(reuse_venv=True)

SESSION_INSTALL_SILENT = False
SESSION_RUN_SILENT = False

# default sessions when none is specified
# nox --session [SESSION] [SESSION] [...]
# or
# nox --tag [TAG] [TAG] [...]
nox.options.sessions = [
    "coverage",  # Todo
    "sbom",
    "lint",
    "readme",
    "release",  # Todo
    "testing",  # Todo
]

BATCH_EXCLUDED = []

# Python versions to test against
# dagster==1.9.11 needs >=3.9 but 3.13 does not seem to be working
PYTHON_TEST_VERSIONS = [
    "3.11",
    # "3.12",
    # "3.13",
]

PYTHON_VERSION_MAIN = PYTHON_TEST_VERSIONS[0]

ENV = {}


GIT_MAIN_BRANCH = "main"


# Semantic Versioning
# https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
# RE_SEMVER = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
RE_SEMVER = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


#######################################################################################################################
# Parameterized Features
engine_dir: pathlib.Path = pathlib.Path(__file__).parent
features_dir: pathlib.Path = engine_dir / ".features"
FEATURES_PARAMETERIZED: list[pathlib.Path] = []

for dir_ in features_dir.iterdir():
    # dir_ is always the full path
    if any(dir_.name == i for i in BATCH_EXCLUDED):
        logging.info(f"Skipped: {dir_ = }")
        continue
    if dir_.is_dir():
        if pathlib.Path(dir_ / ".git").exists():
            FEATURES_PARAMETERIZED.append(dir_.relative_to(engine_dir.parent))


#######################################################################################################################
# Feature Template
# Todo:
#  - [ ] Maybe create a Feature from Template via `nox`?


#######################################################################################################################


#######################################################################################################################
# Git

# # REPOSITORY ENGINE

REPO_ENGINE = "OpenStudioLandscapes"


# # REPOSITORIES FEATURES
REPOS_FEATURE = {
    "https": {
        # Testing a few Features in public
        "OpenStudioLandscapes-Ayon": "https://github.com/michimussato/OpenStudioLandscapes-Ayon.git",
        "OpenStudioLandscapes-Dagster": "https://github.com/michimussato/OpenStudioLandscapes-Dagster.git",
        # "OpenStudioLandscapes-Deadline-10-2": "https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2.git",
        # "OpenStudioLandscapes-Deadline-10-2-Worker": "https://github.com/michimussato/OpenStudioLandscapes-Deadline-10-2-Worker.git",
        # "OpenStudioLandscapes-filebrowser": "https://github.com/michimussato/OpenStudioLandscapes-filebrowser.git",
        # "OpenStudioLandscapes-Grafana": "https://github.com/michimussato/OpenStudioLandscapes-Grafana.git",
        "OpenStudioLandscapes-Kitsu": "https://github.com/michimussato/OpenStudioLandscapes-Kitsu.git",
        # "OpenStudioLandscapes-LikeC4": "https://github.com/michimussato/OpenStudioLandscapes-LikeC4.git",
        # "OpenStudioLandscapes-NukeRLM-8": "https://github.com/michimussato/OpenStudioLandscapes-NukeRLM-8.git",
        # "OpenStudioLandscapes-OpenCue": "https://github.com/michimussato/OpenStudioLandscapes-OpenCue.git",
        # "OpenStudioLandscapes-SESI-gcc-9-3-Houdini-20": "https://github.com/michimussato/OpenStudioLandscapes-SESI-gcc-9-3-Houdini-20.git",
        # "OpenStudioLandscapes-Syncthing": "https://github.com/michimussato/OpenStudioLandscapes-Syncthing.git",
        # "OpenStudioLandscapes-Watchtower": "https://github.com/michimussato/OpenStudioLandscapes-Watchtower.git",
    },
    "ssh": {
        # This is for testing while repository is private
        "OpenStudioLandscapes-Ayon": "git@github.com:michimussato/OpenStudioLandscapes-Ayon.git",
        "OpenStudioLandscapes-Dagster": "git@github.com:michimussato/OpenStudioLandscapes-Dagster.git",
        "OpenStudioLandscapes-Deadline-10-2": "git@github.com:michimussato/OpenStudioLandscapes-Deadline-10-2.git",
        "OpenStudioLandscapes-Deadline-10-2-Worker": "git@github.com:michimussato/OpenStudioLandscapes-Deadline-10-2-Worker.git",
        "OpenStudioLandscapes-filebrowser": "git@github.com:michimussato/OpenStudioLandscapes-filebrowser.git",
        "OpenStudioLandscapes-Grafana": "git@github.com:michimussato/OpenStudioLandscapes-Grafana.git",
        "OpenStudioLandscapes-Kitsu": "git@github.com:michimussato/OpenStudioLandscapes-Kitsu.git",
        "OpenStudioLandscapes-LikeC4": "git@github.com:michimussato/OpenStudioLandscapes-LikeC4.git",
        "OpenStudioLandscapes-NukeRLM-8": "git@github.com:michimussato/OpenStudioLandscapes-NukeRLM-8.git",
        "OpenStudioLandscapes-OpenCue": "git@github.com:michimussato/OpenStudioLandscapes-OpenCue.git",
        "OpenStudioLandscapes-SESI-gcc-9-3-Houdini-20": "git@github.com:michimussato/OpenStudioLandscapes-SESI-gcc-9-3-Houdini-20.git",
        "OpenStudioLandscapes-Syncthing": "git@github.com:michimussato/OpenStudioLandscapes-Syncthing.git",
        "OpenStudioLandscapes-Watchtower": "git@github.com:michimussato/OpenStudioLandscapes-Watchtower.git",
    },
}["https"]

# # MAIN BRANCH
MAIN_BRANCH = "main"

# # clone_features
@nox.session(python=None, tags=["clone_features"])
def clone_features(session):
    """
    `git clone` all listed (REPOS_FEATURE) Features into .features.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Todo
    #  - [ ] create pull_features() session?

    # Ex:
    # nox --session clone_features
    # nox --tags clone_features

    # git -C .features clone https://github.com/michimussato/OpenStudioLandscapes-<Feature>

    OPENSTUDIOLANDSCAPES_VERSION_TAG: str = os.environ.get(
        "OPENSTUDIOLANDSCAPES_VERSION_TAG", None
    )

    if OPENSTUDIOLANDSCAPES_VERSION_TAG is None:
        print(
            f"OPENSTUDIOLANDSCAPES_VERSION_TAG is not set, checking out {MAIN_BRANCH} branch."
        )

    sudo = False

    for name, repo in REPOS_FEATURE.items():

        logging.info("Cloning %s" % name)

        # Todo
        #  - [ ] git clone fatal if directory exists

        # if cd repo; then git pull; else git clone https://server/repo repo; fi

        repo_dest = pathlib.Path.cwd() / ".features" / name

        if repo_dest.exists():
            raise FileExistsError(
                "The repo %s already exists. Please remove it before cloning."
                % repo_dest.as_posix()
            )

        else:
            logging.info("Cloning %s" % name)

            # Clone the repository
            cmd_clone = [
                shutil.which("git"),
                "-C",
                repo_dest.parent.as_posix(),
                "clone",
                "--tags",
                repo,
            ]

            if OPENSTUDIOLANDSCAPES_VERSION_TAG is not None:
                # Checkout a specifig Git tag
                cmd_checkout = [
                    shutil.which("git"),
                    "-C",
                    repo_dest.as_posix(),
                    "checkout",
                    f"tags/{OPENSTUDIOLANDSCAPES_VERSION_TAG}",
                    "-B",
                    OPENSTUDIOLANDSCAPES_VERSION_TAG,
                ]

        if sudo:
            cmd_clone.insert(0, shutil.which("sudo"))
            cmd_clone.insert(1, "--reset-timestamp")

            cmd_checkout.insert(0, shutil.which("sudo"))
            cmd_checkout.insert(1, "--reset-timestamp")

        logging.info(f"{cmd_clone = }")

        session.run(
            *cmd_clone,
            external=True,
            silent=SESSION_RUN_SILENT,
        )

        logging.info(f"{cmd_checkout = }")

        session.run(
            *cmd_checkout,
            external=True,
            silent=SESSION_RUN_SILENT,
        )


# # # pull_features
# @nox.session(python=None, tags=["pull_features"])
# def pull_features(session):
#     """
#     `git pull` all listed (REPOS_FEATURE) Features.
#
#     Scope:
#     - [x] Engine
#     - [ ] Features
#     """
#     # Ex:
#     # nox --session pull_features
#     # nox --tags pull_features
#
#     for name, repo in REPOS_FEATURE.items():
#
#         logging.info("Pulling %s" % name)
#
#         session.run(
#             shutil.which("git"),
#             "-C",
#             pathlib.Path.cwd() / ".features" / name,
#             "pull",
#             "--verbose",
#             "origin",
#             MAIN_BRANCH,
#             "--rebase=true",
#             "--tags",
#             external=True,
#         )


# # stash_features
@nox.session(python=None, tags=["stash_features"])
def stash_features(session):
    """
    `git stash` all listed (REPOS_FEATURE) Features.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session stash_features
    # nox --tags stash_features

    sudo = False

    for name, repo in REPOS_FEATURE.items():

        logging.info("Stashing %s" % name)

        cmd = [
            shutil.which("git"),
            "-C",
            pathlib.Path.cwd() / ".features" / name,
            "stash",
        ]

        if sudo:
            cmd.insert(0, shutil.which("sudo"))
            cmd.insert(1, "--reset-timestamp")
            # cmd.insert(2, "--stdin")

        logging.info(f"{cmd = }")

        session.run(
            *cmd,
            external=True,
            silent=SESSION_RUN_SILENT,
        )


# # stash_apply_features
@nox.session(python=None, tags=["stash_apply_features"])
def stash_apply_features(session):
    """
    `git stash apply` all listed (REPOS_FEATURE) Features.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session stash_apply_features
    # nox --tags stash_apply_features

    sudo = False

    for name, repo in REPOS_FEATURE.items():

        logging.info("Stashing %s" % name)

        cmd = [
            shutil.which("git"),
            "-C",
            pathlib.Path.cwd() / ".features" / name,
            "stash",
            "apply",
        ]

        if sudo:
            cmd.insert(0, shutil.which("sudo"))
            cmd.insert(1, "--reset-timestamp")
            # cmd.insert(2, "--stdin")

        logging.info(f"{cmd = }")

        session.run(
            *cmd,
            external=True,
            silent=SESSION_RUN_SILENT,
        )


# # pull_engine
@nox.session(python=None, tags=["pull_engine"])
def pull_engine(session):
    """
    `git pull` engine.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session pull_engine
    # nox --tags pull_engine

    sudo = False

    logging.info("Pulling %s" % REPO_ENGINE)

    cmd = [
        shutil.which("git"),
        "pull",
        "--verbose",
        "origin",
        MAIN_BRANCH,
        "--rebase=true",
        "--tags",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        external=True,
        silent=SESSION_RUN_SILENT,
    )


# # stash_engine
@nox.session(python=None, tags=["stash_engine"])
def stash_engine(session):
    """
    `git stash` engine.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session stash_engine
    # nox --tags stash_engine

    sudo = False

    logging.info("Stashing %s" % REPO_ENGINE)

    cmd = [
        shutil.which("git"),
        "stash",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        external=True,
        silent=SESSION_RUN_SILENT,
    )


# # stash_apply_engine
@nox.session(python=None, tags=["stash_apply_engine"])
def stash_apply_engine(session):
    """
    `git stash apply` engine.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session stash_apply_engine
    # nox --tags stash_apply_engine

    sudo = False

    logging.info("Stashing %s" % REPO_ENGINE)

    cmd = [
        shutil.which("git"),
        "stash",
        "apply",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        external=True,
        silent=SESSION_RUN_SILENT,
    )


#######################################################################################################################


#######################################################################################################################
# venv

# This will probably not work...
# we can't run `nox` before the `venv` is even
# present in the first place.

# # # create_venv_engine
# @nox.session(python=None, tags=["create_venv_engine"])
# def create_venv_engine(session):
#     """
#     Create a `venv` after cloning OpenStudioLandscapes engine and install
#     the package into it.
#
#     Scope:
#     - [x] Engine
#     - [ ] Features
#     """
#     # Ex:
#     # nox --session create_venv_engine
#     # nox --tags create_venv_engine
#
#     session.run(
#         shutil.which("python3.11"),
#         "-m",
#         "venv",
#         ".venv",
#         external=True,
#     )
#
#     session.run(
#         ".venv/bin/python",
#         "-m",
#         "pip",
#         "install",
#         "--upgrade",
#         "pip",
#         "setuptools",
#         external=True,
#     )
#
#     session.run(
#         ".venv/bin/python",
#         "-m",
#         "pip",
#         "install",
#         "--editable",
#         ".[dev]",
#         external=True,
#     )


# # create_venv_features
@nox.session(python=None, tags=["create_venv_features"])
def create_venv_features(session):
    """
    Create a `venv`s in .features/<Feature> after `nox --session clone_features` and installing the Feature into its own `.venv`.

    ```
    cd .features/<Feature>
    python3.11 -m venv .venv
    source .venv/bin/activate
    pip install -e .[dev]
    ```

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session create_venv_features
    # nox --tags create_venv_features

    sudo = False

    features_dir = pathlib.Path.cwd() / ".features"

    for dir_ in features_dir.iterdir():
        # dir_ is always the full path
        if dir_.is_dir():
            if pathlib.Path(dir_ / ".git").exists():
                with session.chdir(dir_):

                    cmd1 = [
                        shutil.which("python3.11"),
                        "-m",
                        "venv",
                        ".venv",
                    ]

                    if sudo:
                        cmd1.insert(0, shutil.which("sudo"))
                        cmd1.insert(1, "--reset-timestamp")
                        # cmd.insert(2, "--stdin")

                    logging.info(f"{cmd1 = }")

                    session.run(
                        *cmd1,
                        external=True,
                        silent=SESSION_RUN_SILENT,
                    )

                    cmd2 = [
                        ".venv/bin/python",
                        "-m",
                        "pip",
                        "install",
                        "--upgrade",
                        "pip",
                        "setuptools",
                    ]

                    if sudo:
                        cmd2.insert(0, shutil.which("sudo"))
                        cmd2.insert(1, "--reset-timestamp")
                        # cmd.insert(2, "--stdin")

                    logging.info(f"{cmd2 = }")

                    session.run(
                        *cmd2,
                        external=True,
                        silent=SESSION_RUN_SILENT,
                    )

                    cmd3 = [
                        ".venv/bin/python",
                        "-m",
                        "pip",
                        "install",
                        "--editable",
                        ".[dev]",
                    ]

                    if sudo:
                        cmd3.insert(0, shutil.which("sudo"))
                        cmd3.insert(1, "--reset-timestamp")
                        # cmd.insert(2, "--stdin")

                    logging.info(f"{cmd3 = }")

                    session.run(
                        *cmd3,
                        external=True,
                        silent=SESSION_RUN_SILENT,
                    )


# # install_features_into_engine
@nox.session(python=None, tags=["install_features_into_engine"])
def install_features_into_engine(session):
    """
    Installs the Features after `nox --session clone_features` into the engine `.venv`.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session install_features_into_engine
    # nox --tags install_features_into_engine

    sudo = False

    features_dir = pathlib.Path.cwd() / ".features"

    session.run(
        ".venv/bin/python",
        "-m",
        "pip",
        "install",
        "--upgrade",
        # "--force-reinstall",
        "pip",
        "setuptools",
        external=True,
        silent=SESSION_RUN_SILENT,
    )

    for dir_ in features_dir.iterdir():
        # dir_ is always the full path
        if dir_.is_dir():
            if pathlib.Path(dir_ / ".git").exists():
                logging.info("Installing features from %s" % dir_)

                cmd = [
                    ".venv/bin/python",
                    "-m",
                    "pip",
                    "install",
                    "--editable",
                    f"{dir_}[dev]",
                ]

                if sudo:
                    cmd.insert(0, shutil.which("sudo"))
                    cmd.insert(1, "--reset-timestamp")
                    # cmd.insert(2, "--stdin")

                logging.info(f"{cmd = }")

                session.run(
                    *cmd,
                    external=True,
                    silent=SESSION_RUN_SILENT,
                )


#######################################################################################################################


#######################################################################################################################
# Hard Links

LINKED_FILES = [
    ".obsidian/plugins/obsidian-excalidraw-plugin/main.js",
    ".obsidian/plugins/obsidian-excalidraw-plugin/manifest.json",
    ".obsidian/plugins/obsidian-excalidraw-plugin/styles.css",
    ".obsidian/plugins/templater-obsidian/data.json",
    ".obsidian/plugins/templater-obsidian/main.js",
    ".obsidian/plugins/templater-obsidian/manifest.json",
    ".obsidian/plugins/templater-obsidian/styles.css",
    ".obsidian/app.json",
    ".obsidian/appearance.json",
    ".obsidian/canvas.json",
    ".obsidian/community-plugins.json",
    ".obsidian/core-plugins.json",
    ".obsidian/core-plugins-migration.json",
    ".obsidian/daily-notes.json",
    ".obsidian/graph.json",
    # ".obsidian/hotkeys.json",
    ".obsidian/templates.json",
    ".obsidian/types.json",
    # ".obsidian/workspace.json",
    # ".obsidian/workspaces.json",
    ".gitattributes",
    ".sbom/.gitkeep",
    ".payload/bin/.gitkeep",
    ".payload/config/.gitkeep",
    ".payload/data/.gitkeep",
    "media/images/.gitkeep",
    ".gitignore",
    ".pre-commit-config.yaml",
    "noxfile.py",
    "LICENSE.txt",
]

# # fix_hardlinks_in_features
@nox.session(python=None, tags=["fix_hardlinks_in_features"])
def fix_hardlinks_in_features(session):
    """
    See https://github.com/michimussato/OpenStudioLandscapes?tab=readme-ov-file#hard-links-sync-files-and-directories-across-repositories-de-duplication

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session fix_hardlinks_in_features
    # nox --tags fix_hardlinks_in_features

    # ln -f ../../../OpenStudioLandscapes/noxfile.py  noxfile.py

    sudo = False

    cwd = pathlib.Path.cwd()
    features_dir = cwd / ".features"

    for dir_ in features_dir.iterdir():
        # dir_ is always the full path
        if dir_.is_dir():
            if pathlib.Path(dir_ / ".git").exists():
                for file_ in LINKED_FILES:

                    file_ = pathlib.Path(file_)

                    file_path = file_.parent
                    link_name = file_.name

                    with session.chdir(dir_ / file_path):

                        logging.info(
                            "Working director is %s" % pathlib.Path.cwd().as_posix()
                        )

                        logging.info("Fixing hardlink for file %s" % file_)

                        # Target can be absolute
                        target = pathlib.Path(cwd / file_)

                        logging.info("Target: %s" % target.as_posix())
                        logging.info("Link name: %s" % link_name)

                        if platform.system() == "Linux":

                            cmd = [
                                shutil.which("ln"),
                                "--force",
                                "--backup=numbered",
                                target.as_posix(),
                                link_name,
                            ]

                        elif platform.system() == "Darwin":

                            cmd = [
                                shutil.which("ln"),
                                "-f",
                                target.as_posix(),
                                link_name,
                            ]

                        if sudo:
                            cmd.insert(0, shutil.which("sudo"))
                            cmd.insert(1, "--reset-timestamp")
                            # cmd.insert(2, "--stdin")

                        logging.info(f"{cmd = }")

                        session.run(
                            *cmd,
                            external=True,
                            silent=SESSION_RUN_SILENT,
                        )


#######################################################################################################################


#######################################################################################################################
# Pi-hole

# # ENVIRONMENT
ENVIRONMENT_PI_HOLE = {
    "ROOT_DOMAIN": "farm.evil",
    "PIHOLE_USE_UNBOUND": True,
    "PIHOLE_WEB_PORT_HOST": "81",
    "PIHOLE_WEB_PASSWORD": "myp4ssword",
    "PIHOLE_TIMEZONE": "Europe/Zurich",
    "PIHOLE_REV_SERVER": "false",
    "PIHOLE_DNS_DNSSEC": "true",
    "PIHOLE_DNS_LISTENING_MODE": [
        "all",
        "single",
    ][0],
    "PIHOLE_WEB_THEME": [
        "default-dark",
        "default-darker",
        "default-light",
        "default-auto",
        "lcars",
    ][0],
    "PI_HOLE_ROOT_DIR": pathlib.Path.cwd() / ".pi-hole",
    "PI_HOLE_ETC_PI_HOLE": "etc-pihole",
    "PI_HOLE_ETC_DNSMASQ": "etc-dnsmasq",
}

compose_pi_hole = ENVIRONMENT_PI_HOLE["PI_HOLE_ROOT_DIR"] / "docker-compose.yml"

cmd_pi_hole = [
    # sudo = False
    shutil.which("docker"),
    "compose",
    "--progress",
    DOCKER_PROGRESS,
    "--file",
    compose_pi_hole.as_posix(),
    "--project-name",
    "openstudiolandscapes-pi-hole",
]


def write_pi_hole_yml(
    # yaml_out: pathlib.Path,
) -> pathlib.Path:

    pi_hole_root_dir: pathlib.Path = ENVIRONMENT_PI_HOLE["PI_HOLE_ROOT_DIR"]
    pi_hole_root_dir.mkdir(parents=True, exist_ok=True)

    harbor_etc_pi_hole_dir = (
        pi_hole_root_dir / ENVIRONMENT_PI_HOLE["PI_HOLE_ETC_PI_HOLE"]
    )
    harbor_etc_pi_hole_dir.mkdir(parents=True, exist_ok=True)

    harbor_etc_dnsmasq_dir = (
        pi_hole_root_dir / ENVIRONMENT_PI_HOLE["PI_HOLE_ETC_DNSMASQ"]
    )
    harbor_etc_dnsmasq_dir.mkdir(parents=True, exist_ok=True)

    service_name = "pihole-unbound"
    network_name = "pi-hole"
    container_name = service_name
    host_name = ".".join([service_name, ENVIRONMENT_PI_HOLE["ROOT_DOMAIN"]])

    pi_hole_dict = {
        "networks": {
            network_name: {
                "name": f"network_{network_name}",
            },
        },
        "services": {
            service_name: {
                "container_name": container_name,
                "hostname": host_name,
                "domainname": ENVIRONMENT_PI_HOLE["ROOT_DOMAIN"],
                "restart": "unless-stopped",
                "image": "docker.io/mpgirro/pihole-unbound:latest",
                "volumes": [
                    # For persisting Pi-hole's databases and common configuration file
                    f"{harbor_etc_pi_hole_dir.as_posix()}:/etc/pihole:rw",
                    f"{harbor_etc_dnsmasq_dir.as_posix()}:/etc/dnsmasq.d:rw",
                    # Uncomment the below if you have custom dnsmasq config files that you want to persist. Not needed for most starting fresh with Pi-hole v6. If you're upgrading from v5 you and have used this directory before, you should keep it enabled for the first v6 container start to allow for a complete migration. It can be removed afterwards. Needs environment variable FTLCONF_misc_etc_dnsmasq_d: 'true'
                    # f"./etc-dnsmasq.d:/etc/dnsmasq.d"
                ],
                "networks": [network_name],
                "ports": [
                    # DNS Ports
                    "53:53/tcp",
                    "53:53/udp",
                    # Default HTTP Port
                    f"{ENVIRONMENT_PI_HOLE['PIHOLE_WEB_PORT_HOST']}:80/tcp",
                    # Default HTTPs Port. FTL will generate a self-signed certificate
                    "443:443/tcp",
                    # Uncomment the line below if you are using Pi-hole as your DHCP server
                    # - "67:67/udp"
                    # Uncomment the line below if you are using Pi-hole as your NTP server
                    # - "123:123/udp"
                ],
                "environment": {
                    # Set the appropriate timezone for your location (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones), e.g:
                    "TZ": ENVIRONMENT_PI_HOLE["PIHOLE_TIMEZONE"],
                    # Set a password to access the web interface. Not setting one will result in a random password being assigned
                    "FTLCONF_webserver_api_password": ENVIRONMENT_PI_HOLE[
                        "PIHOLE_WEB_PASSWORD"
                    ],
                    # If using Docker's default `bridge` network setting the dns listening mode should be set to 'all'
                    # Unbound
                    # "FTLCONF_LOCAL_IPV4": "0.0.0.0",
                    "FTLCONF_webserver_interface_theme": ENVIRONMENT_PI_HOLE[
                        "PIHOLE_WEB_THEME"
                    ],
                    # "FTLCONF_dns_revServers": "${REV_SERVER:-false},${REV_SERVER_CIDR},${REV_SERVER_TARGET},${REV_SERVER_DOMAIN}",
                    "FTLCONF_dns_upstreams": "127.0.0.1#5335",
                    "FTLCONF_dns_dnssec": ENVIRONMENT_PI_HOLE["PIHOLE_DNS_DNSSEC"],
                    "FTLCONF_dns_listeningMode": ENVIRONMENT_PI_HOLE[
                        "PIHOLE_DNS_LISTENING_MODE"
                    ],
                    # "FTLCONF_webserver_port": "82",
                    "REV_SERVER": ENVIRONMENT_PI_HOLE["PIHOLE_REV_SERVER"],
                    # If REV_SERVER is "false", these are not necessary:
                    # "REV_SERVER_CIDR": "",
                    # "REV_SERVER_TARGET": "",
                    # "REV_SERVER_DOMAIN": "",
                },
                "cap_add": [
                    # Todo
                    # See https://github.com/pi-hole/docker-pi-hole#note-on-capabilities
                    # Required if you are using Pi-hole as your DHCP server, else not needed
                    # "NET_ADMIN",
                    # Required if you are using Pi-hole as your NTP client to be able to set the host's system time
                    # "SYS_TIME",
                    # Optional, if Pi-hole should get some more processing time
                    # "SYS_NICE",
                ]
                # "healthcheck": {
                # },
                # "command": [
                # ],
            },
        },
    }

    harbor_yml: str = yaml.dump(
        pi_hole_dict,
        indent=2,
    )

    with open(compose_pi_hole.as_posix(), "w") as fw:
        fw.write(harbor_yml)

    logging.debug("Contents Pi-hole docker-compose.yml: \n%s" % harbor_yml)

    return compose_pi_hole


# # pi_hole_up
@nox.session(python=None, tags=["pi_hole_up"])
def pi_hole_up(session):
    """
    Start Pi-hole in attached mode.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session pi_hole_up
    # nox --tags pi_hole_up

    # /usr/bin/docker \
    #     compose \
    #     --file /home/michael/git/repos/OpenStudioLandscapes/.landscapes/.pi-hole/docker_compose/docker-compose.yml \
    #     --project-name openstudiolandscapes-pi-hole up --remove-orphans

    sudo = False

    if not compose_pi_hole.exists():
        raise FileNotFoundError(
            f"Compose file not found: {compose_pi_hole}. "
            f"Execute `Compose_pi_hole / compose` in "
            f"Dagster to create it."
        )

    cmd = [
        *cmd_pi_hole,
        "up",
        "--remove-orphans",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        env=ENV,
        external=True,
        silent=SESSION_RUN_SILENT,
    )


# # pi_hole_prepare
@nox.session(python=None, tags=["pi_hole_prepare"])
def pi_hole_prepare(session):
    """
    Prepare Pi-hole in attached mode.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session pi_hole_prepare
    # nox --tags pi_hole_prepare

    if compose_pi_hole.exists():
        logging.info(
            "`docker-compose.yml` already present in. Use that or start fresh by "
            "issuing `nox --session pi_hole_clear` first."
        )
        return 0

    docker_compose: pathlib.Path = write_pi_hole_yml()

    logging.debug("docker-compose.yml created: \n%s" % docker_compose.as_posix())

    return 0


# # pi_hole_clear
@nox.session(python=None, tags=["pi_hole_clear"])
def pi_hole_clear(session):
    """
    Clear Pi-hole with `sudo`. WARNING: DATA LOSS!

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session pi_hole_clear
    # nox --tags pi_hole_clear

    sudo = True

    pi_hole_root_dir: pathlib.Path = ENVIRONMENT_PI_HOLE["PI_HOLE_ROOT_DIR"]

    logging.debug("Clearing Pi-hole...")

    cmd = [
        shutil.which("git"),
        "clean",
        "-x",
        "--force",
        pi_hole_root_dir.as_posix(),
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    if pi_hole_root_dir.exists():
        logging.warning("Clearing out Pi-hole...\nContinue? Type `yes` to confirm.")
        answer = input()
        if answer.lower() == "yes":

            logging.info(f"{cmd = }")

            session.run(
                *cmd,
                env=ENV,
                external=True,
                silent=SESSION_RUN_SILENT,
            )
        else:
            logging.info("Clearing %s was aborted." % pi_hole_root_dir.as_posix())
            return 1

    logging.debug("%s removed" % pi_hole_root_dir.as_posix())

    return 0


# # pi_hole_up_detach
@nox.session(python=None, tags=["pi_hole_up_detach"])
def pi_hole_up_detach(session):
    """
    Start Pi-hole in detached mode.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session pi_hole_up_detach
    # nox --tags pi_hole_up_detach

    # /usr/bin/docker \
    #     compose \
    #     --file /home/michael/git/repos/OpenStudioLandscapes/.landscapes/.pi-hole/docker_compose/docker-compose.yml \
    #     --project-name openstudiolandscapes-pi-hole up --remove-orphans --detach

    sudo = False

    if not compose_pi_hole.exists():
        raise FileNotFoundError(
            f"Compose file not found: {compose_pi_hole}. "
            f"Execute `Compose_pi_hole / compose` in "
            f"Dagster to create it."
        )

    cmd = [
        *cmd_pi_hole,
        "up",
        "--remove-orphans",
        "--detach",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        env=ENV,
        external=True,
        silent=SESSION_RUN_SILENT,
    )


# # pi_hole_down
@nox.session(python=None, tags=["pi_hole_down"])
def pi_hole_down(session):
    """
    Shut down Pi-hole.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session pi_hole_down
    # nox --tags pi_hole_down

    # /usr/bin/docker \
    #     compose \
    #     --file /home/michael/git/repos/OpenStudioLandscapes/.landscapes/.pi-hole/docker_compose/docker-compose.yml \
    #     --project-name openstudiolandscapes-pi-holw down

    sudo = False

    if not compose_pi_hole.exists():
        raise FileNotFoundError(
            f"Compose file not found: {compose_pi_hole}. "
            f"Execute `Compose_pi_hole / compose` in "
            f"Dagster to create it."
        )

    cmd = [
        *cmd_pi_hole,
        "down",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        env=ENV,
        external=True,
        silent=SESSION_RUN_SILENT,
    )


#######################################################################################################################


#######################################################################################################################
# Harbor

# # ENVIRONMENT
ENVIRONMENT_HARBOR = {
    "HARBOR_HOSTNAME": "harbor.farm.evil",
    "HARBOR_ADMIN": "admin",
    "HARBOR_PASSWORD": "Harbor12345",
    # Todo:
    #  - [ ] Try with:
    # "HARBOR_ADMIN": "harbor@openstudiolandscapes.org",
    # "HARBOR_PASSWORD": "0penstudiolandscapes",
    "HARBOR_PORT": 80,
    "HARBOR_RELEASE": [
        "v2.12.2",
        "v2.13.0",
    ][0],
    "HARBOR_INSTALLER": {
        "online": "https://github.com/goharbor/harbor/releases/download/{HARBOR_RELEASE}/harbor-online-installer-{HARBOR_RELEASE}.tgz",
        "offline": "https://github.com/goharbor/harbor/releases/download/{HARBOR_RELEASE}/harbor-offline-installer-{HARBOR_RELEASE}.tgz",
    }["online"],
    "HARBOR_ROOT_DIR": pathlib.Path.cwd() / ".harbor",
    "HARBOR_BIN_DIR": "bin",
    "HARBOR_DOWNLOAD_DIR": "download",
    "HARBOR_DATA_DIR": "data",
}

compose_harbor = (
    ENVIRONMENT_HARBOR["HARBOR_ROOT_DIR"]
    / ENVIRONMENT_HARBOR["HARBOR_BIN_DIR"]
    / "docker-compose.yml"
)

cmd_harbor = [
    # sudo = True
    # shutil.which("sudo"),
    shutil.which("docker"),
    "compose",
    "--progress",
    DOCKER_PROGRESS,
    "--file",
    compose_harbor.as_posix(),
    "--project-name",
    "openstudiolandscapes-harbor",
]


# Query for existence of `openstudiolandscapes`:
# WORKS:
# curl -X 'GET' \
#   'http://harbor.farm.evil/api/v2.0/projects/openstudiolandscapes' \
#   -H 'accept: application/json'

# Query for existence of `library`:
# WORKS:
# curl -X 'GET' \
#   'http://harbor.farm.evil/api/v2.0/projects/library' \
#   -H 'accept: application/json'

# Create `openstudiolandscapes`:
# WORKS:
# curl -X 'POST' \
#   'http://harbor.farm.evil/api/v2.0/projects' \
#   -H 'accept: application/json' \
#   -H 'X-Resource-Name-In-Location: false' \
#   -H 'authorization: Basic YWRtaW46SGFyYm9yMTIzNDU=' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "project_name": "openstudiolandscapes5432",
#   "public": true
# }'
# WORKS:
# curl -X 'POST' \
#   'http://harbor.farm.evil/api/v2.0/projects' \
#   -H 'accept: application/json' \
#   -H 'X-Resource-Name-In-Location: false' \
#   -H 'authorization: Basic YWRtaW46SGFyYm9yMTIzNDU=' \
#   -H 'Content-Type: application/json' \
#   -H 'X-Harbor-CSRF-Token: fBZWDC+hFFRGC1VE/hUId3Dn5OJXHJXelHEwfGyUHwSwmoxa22QrmqsBtUXeHCZI6toiE/qLAfBMVhfwk6Yz7Q==' \
#   -d '{
#   "project_name": "openstudiolandscapes",
#   "public": true
# }'

# Authorization:
# import base64
# base64.b64encode("admin:Harbor12345".encode("utf-8")).decode("ascii")
# # -> 'YWRtaW46SGFyYm9yMTIzNDU='

# Delete `library`:
# curl -X 'DELETE' \
#   'http://192.168.1.160/api/v2.0/projects/library' \
#   -H 'accept: application/json' \
#   -H 'X-Is-Resource-Name: false' \
#   -H 'authorization: Basic YWRtaW46SGFyYm9yMTIzNDU=' \
#   -H 'X-Harbor-CSRF-Token: Io8FR6UF0ESNAWHX+fGy2FVqCB/jqY4xTECrRZ4KZ5OmEnpQMGdYxGg0gPR6UaB1EZcoaLtSTrz6rgZZ+7xcwA=='


def setup_harbor(
    harbor_download_dir: pathlib.Path,
) -> pathlib.Path:

    file_path: pathlib.Path = download(
        url=f"{ENVIRONMENT_HARBOR['HARBOR_INSTALLER']}".format(
            **ENVIRONMENT_HARBOR,
        ),
        dest_folder=harbor_download_dir,
    )

    logging.info("File successfully downloaded to %s" % file_path.as_posix())

    return file_path


def write_harbor_yml(
    yaml_out: pathlib.Path,
) -> pathlib.Path:

    harbor_root_dir: pathlib.Path = ENVIRONMENT_HARBOR["HARBOR_ROOT_DIR"]
    harbor_root_dir.mkdir(parents=True, exist_ok=True)

    harbor_data_dir = harbor_root_dir / ENVIRONMENT_HARBOR["HARBOR_DATA_DIR"]
    harbor_data_dir.mkdir(parents=True, exist_ok=True)

    harbor_dict = {
        "hostname": ENVIRONMENT_HARBOR["HARBOR_HOSTNAME"],
        "http": {"port": ENVIRONMENT_HARBOR["HARBOR_PORT"]},
        "harbor_admin_password": ENVIRONMENT_HARBOR["HARBOR_PASSWORD"],
        "database": {
            "password": "root123",
            "max_idle_conns": 100,
            "max_open_conns": 900,
            "conn_max_idle_time": 0,
        },
        "data_volume": harbor_data_dir.as_posix(),
        "trivy": {
            "ignore_unfixed": False,
            "skip_update": False,
            "skip_java_db_update": False,
            "offline_scan": False,
            "security_check": "vuln",
            "insecure": False,
            "timeout": "5m0s",
        },
        "jobservice": {
            "max_job_workers": 10,
            "job_loggers": ["STD_OUTPUT", "FILE"],
            "logger_sweeper_duration": 1,
        },
        "notification": {
            "webhook_job_max_retry": 3,
            "webhook_job_http_client_timeout": 3,
        },
        "log": {
            "level": "info",
            "local": {
                "rotate_count": 50,
                "rotate_size": "200M",
                "location": "/var/log/harbor",
            },
        },
        "_version": "2.12.0",
        "proxy": {
            "http_proxy": None,
            "https_proxy": None,
            "no_proxy": None,
            "components": ["core", "jobservice", "trivy"],
        },
        "upload_purging": {
            "enabled": True,
            "age": "168h",
            "interval": "24h",
            "dryrun": False,
        },
        "cache": {"enabled": False, "expire_hours": 24},
    }

    logging.debug(
        "Harbor Configuration = %s"
        % json.dumps(
            obj=harbor_dict,
            sort_keys=True,
            indent=2,
        )
    )

    harbor_yml: str = yaml.dump(
        harbor_dict,
        indent=2,
    )

    with open(yaml_out, "w") as fw:
        fw.write(harbor_yml)

    logging.debug("Contents harbor.yml: \n%s" % harbor_yml)

    return yaml_out


# # harbor_prepare
@nox.session(python=None, tags=["harbor_prepare"])
def harbor_prepare(session):
    """
    Prepare Harbor with `sudo`.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session harbor_prepare
    # nox --tags harbor_prepare

    # Todo
    #  - [ ] Maybe use env var HARBOR_BUNDLE_DIR for prepare

    sudo = False

    harbor_root_dir: pathlib.Path = ENVIRONMENT_HARBOR["HARBOR_ROOT_DIR"]
    harbor_root_dir.mkdir(parents=True, exist_ok=True)

    harbor_bin_dir: pathlib.Path = (
        harbor_root_dir / ENVIRONMENT_HARBOR["HARBOR_BIN_DIR"]
    )
    harbor_bin_dir.mkdir(parents=True, exist_ok=True)

    prepare: pathlib.Path = harbor_bin_dir / "prepare"

    if prepare.exists():
        logging.info(
            "`prepare` already present in. Use that or start fresh by "
            "issuing `nox --session harbor_clear` first."
        )
        return

    harbor_download_dir = harbor_root_dir / ENVIRONMENT_HARBOR["HARBOR_DOWNLOAD_DIR"]
    harbor_download_dir.mkdir(parents=True, exist_ok=True)

    tar_file = setup_harbor(
        harbor_download_dir=harbor_download_dir,
    )

    # equivalent to tar --strip-components=1
    # Credits: https://stackoverflow.com/a/78461535
    strip1 = lambda member, path: member.replace(
        name=pathlib.Path(*pathlib.Path(member.path).parts[1:])
    )

    logging.debug("Extracting tar file...")
    with tarfile.open(tar_file, "r:gz") as tar:
        tar.extractall(
            path=harbor_bin_dir,
            filter=strip1,
        )
    logging.debug("All files extracted to %s" % harbor_bin_dir.as_posix())

    harbor_yml: pathlib.Path = write_harbor_yml(
        yaml_out=harbor_bin_dir / "harbor.yml",
    )

    if not harbor_yml.exists():
        raise FileNotFoundError("`harbor.yml` file not found. " "Not able to continue.")

    prepare: pathlib.Path = harbor_bin_dir / "prepare"

    if not prepare.exists():
        raise FileNotFoundError("`prepare` file not found. " "Not able to continue.")

    logging.debug("Preparing Harbor...")

    cmd = [
        shutil.which("bash"),
        prepare.as_posix(),
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        env=ENV,
        external=True,
        silent=SESSION_RUN_SILENT,
    )


# # harbor_clear
@nox.session(python=None, tags=["harbor_clear"])
def harbor_clear(session):
    """
    Clear Harbor with `sudo`.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session harbor_clear
    # nox --tags harbor_clear

    sudo = True

    harbor_root_dir: pathlib.Path = ENVIRONMENT_HARBOR["HARBOR_ROOT_DIR"]

    logging.debug("Clearing Harbor...")
    logging.debug("Resetting Dir %s" % harbor_root_dir.as_posix())

    cmd = [
        shutil.which("git"),
        "clean",
        "-x",
        "--force",
        harbor_root_dir.as_posix(),
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    if harbor_root_dir.exists():
        logging.warning("Clearing out Harbor...\nContinue? Type `yes` to confirm.")
        answer = input()
        if answer.lower() == "yes":

            logging.info(f"{cmd = }")

            session.run(
                *cmd,
                env=ENV,
                external=True,
                silent=SESSION_RUN_SILENT,
            )
        else:
            logging.info("Clearing %s was aborted." % harbor_root_dir.as_posix())
            return 1

    logging.debug("%s removed" % harbor_root_dir.as_posix())

    return 0


# # Harbor up
@nox.session(python=None, tags=["harbor_up"])
def harbor_up(session):
    """
    Start Harbor with `sudo` in attached mode.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session harbor_up
    # nox --tags harbor_up

    # /usr/bin/sudo \
    #     /usr/bin/docker \
    #     compose \
    #     --file /home/michael/git/repos/OpenStudioLandscapes/.harbor/bin/docker-compose.yml \
    #     --project-name openstudiolandscapes-harbor up --remove-orphans

    sudo = True

    cmd = [
        *cmd_harbor,
        "up",
        "--remove-orphans",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        env=ENV,
        external=True,
        silent=SESSION_RUN_SILENT,
    )


# # Harbor detach
@nox.session(python=None, tags=["harbor_up_detach"])
def harbor_up_detach(session):
    """
    Start Harbor with `sudo` in detached mode.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session harbor_up_detach
    # nox --tags harbor_up_detach

    # /usr/bin/sudo \
    #     /usr/bin/docker \
    #     compose \
    #     --file /home/michael/git/repos/OpenStudioLandscapes/.harbor/bin/docker-compose.yml \
    #     --project-name openstudiolandscapes-harbor up --remove-orphans --detach

    sudo = True

    cmd = [
        *cmd_harbor,
        "up",
        "--remove-orphans",
        "--detach",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        env=ENV,
        external=True,
        silent=SESSION_RUN_SILENT,
    )


# # Harbor Down
@nox.session(python=None, tags=["harbor_down"])
def harbor_down(session):
    """
    Stop Harbor with `sudo`.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session harbor_down
    # nox --tags harbor_down

    # /usr/bin/sudo \
    #     /usr/bin/docker \
    #     compose \
    #     --file /home/michael/git/repos/OpenStudioLandscapes/.harbor/bin/docker-compose.yml \
    #     --project-name openstudiolandscapes-harbor down

    sudo = True

    cmd = [
        *cmd_harbor,
        "down",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        env=ENV,
        external=True,
        silent=SESSION_RUN_SILENT,
    )


#######################################################################################################################


#######################################################################################################################
# Dagster

# # ENVIRONMENT
ENVIRONMENT_DAGSTER = {
    "ROOT_DOMAIN": "farm.evil",
    # Todo:
    #  - [ ] move these two into `.landscapes`
    "DAGSTER_POSTGRES_ROOT_DIR": pathlib.Path.cwd() / ".dagster-postgres",
    "DAGSTER_MYSQL_ROOT_DIR": pathlib.Path.cwd() / ".dagster",
    "DAGSTER_POSTGRES_DB_DIR_DIR": ".postgres",
    "DAGSTER_POSTGRES_DB_USERNAME": "postgres",
    "DAGSTER_POSTGRES_DB_PASSWORD": "mysecretpassword",
    "DAGSTER_POSTGRES_DB_NAME": "postgres",
    "DAGSTER_POSTGRES_DB_PORT_CONTAINER": 5432,
    # Make sure DAGSTER_POSTGRES_DB_PORT_HOST does not clash with other Postgres instances (i.e. OpenCue)
    #
    # - kitsu-init-db--2025-04-24-16-22-05-ec4f3f438cfa4f2bb252e83f78356a39                          |    ...done.
    #   kitsu-init-db--2025-04-24-16-22-05-ec4f3f438cfa4f2bb252e83f78356a39                          | Stopping redis-server: redis-server.
    #   syncthing--2025-04-24-16-22-05-ec4f3f438cfa4f2bb252e83f78356a39                              | [YVSC6] 2025/04/24 14:56:11 INFO: Failed to acquire [::]:22000/TCP open port on NAT-PMP@172.27.0.1: getting new lease on NAT-PMP@172.27.0.1 (external port 35113 -> internal port 22000): read udp 172.27.0.2:48310->172.27.0.1:5351: recvfrom: connection refused
    #   syncthing--2025-04-24-16-22-05-ec4f3f438cfa4f2bb252e83f78356a39                              | [YVSC6] 2025/04/24 14:56:11 INFO: Detected 1 NAT service
    #   kitsu-init-db--2025-04-24-16-22-05-ec4f3f438cfa4f2bb252e83f78356a39 exited with code 0
    #   Gracefully stopping... (press Ctrl+C again to force)
    #   Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint opencue-db (b0598f47d9cf106a2cabb934f07e7f4a732aac61c298c9a54bd1bc8081fa0a1a): Bind for 0.0.0.0:5432 failed: port is already allocated
    # - repository-installer-10-2--2025-04-24-16-22-05-ec4f3f438cfa4f2bb252e83f78356a39 exited with code 0
    #   Gracefully stopping... (press Ctrl+C again to force)
    #   Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint opencue-db (c779b0000eddcd26175adb69cc4e405131ce93f8a37825c7386e47dba9eb92ed): Bind for 0.0.0.0:5432 failed: port is already allocated
    "DAGSTER_POSTGRES_DB_PORT_HOST": 2345,
}

yml_dagster_postgres = ENVIRONMENT_DAGSTER["DAGSTER_POSTGRES_ROOT_DIR"] / "dagster.yaml"
compose_dagster_postgres = (
    ENVIRONMENT_DAGSTER["DAGSTER_POSTGRES_ROOT_DIR"] / "docker-compose.yml"
)

cmd_dagster_postgres = [
    shutil.which("docker"),
    "compose",
    "--progress",
    DOCKER_PROGRESS,
    "--file",
    compose_dagster_postgres.as_posix(),
    "--project-name",
    "openstudiolandscapes-dagster-postgres",
]


def write_dagster_postgres_yml(
    # yaml_out: pathlib.Path,
) -> pathlib.Path:

    # Example:
    # https://github.com/docker-library/docs/blob/master/postgres/README.md#-via-docker-compose-or-docker-stack-deploy

    dagster_postgres_root_dir: pathlib.Path = ENVIRONMENT_DAGSTER[
        "DAGSTER_POSTGRES_ROOT_DIR"
    ]
    dagster_postgres_root_dir.mkdir(parents=True, exist_ok=True)

    service_name = "postgres-dagster"
    network_name = service_name
    container_name = service_name
    host_name = ".".join([service_name, ENVIRONMENT_DAGSTER["ROOT_DOMAIN"]])

    # https://docs.dagster.io/guides/limiting-concurrency-in-data-pipelines
    dagster_postgres_dict = {
        "run_queue": {
            "max_concurrent_runs": 1,
            "block_op_concurrency_limited_runs": {
                "enabled": True,
            },
        },
        "telemetry": {
            "enabled": False,
        },
        "auto_materialize": {
            "enabled": True,
            "use_sensors": True,
        },
        "storage": {
            "postgres": {
                "postgres_db": {
                    "username": ENVIRONMENT_DAGSTER["DAGSTER_POSTGRES_DB_USERNAME"],
                    "password": ENVIRONMENT_DAGSTER["DAGSTER_POSTGRES_DB_PASSWORD"],
                    "hostname": host_name,
                    "db_name": ENVIRONMENT_DAGSTER["DAGSTER_POSTGRES_DB_NAME"],
                    # Todo:
                    #  - [ ] Which one is it?
                    # "port": ENVIRONMENT_DAGSTER["DAGSTER_POSTGRES_DB_PORT_CONTAINER"],
                    "port": ENVIRONMENT_DAGSTER["DAGSTER_POSTGRES_DB_PORT_HOST"],
                },
            },
        },
        # run_monitoring:
        #  enabled: true
        #  free_slots_after_run_end_seconds: 300
        # concurrency:
        #  default_op_concurrency_limit: 1
    }

    dagster_postgres_yml: str = yaml.dump(
        dagster_postgres_dict,
        indent=2,
    )

    with open(yml_dagster_postgres.as_posix(), "w") as fw:
        fw.write(dagster_postgres_yml)

    logging.debug(
        "Contents Dagster-Postgres `dagster.yaml`: \n%s" % dagster_postgres_yml
    )

    return yml_dagster_postgres


def write_dagster_postgres_compose() -> pathlib.Path:

    dagster_postgres_root_dir: pathlib.Path = ENVIRONMENT_DAGSTER[
        "DAGSTER_POSTGRES_ROOT_DIR"
    ]
    dagster_postgres_root_dir.mkdir(parents=True, exist_ok=True)

    dagster_postgres_db_dir: pathlib.Path = (
        dagster_postgres_root_dir / ENVIRONMENT_DAGSTER["DAGSTER_POSTGRES_DB_DIR_DIR"]
    )
    dagster_postgres_db_dir.mkdir(parents=True, exist_ok=True)

    service_name = "postgres-dagster"
    network_name = service_name
    container_name = service_name
    host_name = ".".join([service_name, ENVIRONMENT_DAGSTER["ROOT_DOMAIN"]])

    dagster_postgres_dict = {
        "networks": {
            network_name: {
                "name": f"network_{network_name}",
            },
        },
        "services": {
            service_name: {
                "container_name": container_name,
                "hostname": host_name,
                "domainname": ENVIRONMENT_DAGSTER["ROOT_DOMAIN"],
                "restart": "unless-stopped",
                "image": "docker.io/postgres",
                "volumes": [
                    f"{dagster_postgres_db_dir.as_posix()}:/var/lib/postgresql/data:rw",
                ],
                "networks": [network_name],
                "ports": [
                    f"{ENVIRONMENT_DAGSTER['DAGSTER_POSTGRES_DB_PORT_HOST']}:{ENVIRONMENT_DAGSTER['DAGSTER_POSTGRES_DB_PORT_CONTAINER']}",
                ],
                "environment": {
                    "POSTGRES_USER": ENVIRONMENT_DAGSTER[
                        "DAGSTER_POSTGRES_DB_USERNAME"
                    ],
                    "POSTGRES_PASSWORD": ENVIRONMENT_DAGSTER[
                        "DAGSTER_POSTGRES_DB_PASSWORD"
                    ],
                    "POSTGRES_DB": ENVIRONMENT_DAGSTER["DAGSTER_POSTGRES_DB_NAME"],
                    "PGDATA": "/var/lib/postgresql/data/pgdata",
                },
                # "healthcheck": {
                # },
                # "command": [
                # ],
            },
        },
    }

    dagster_postgres_yml: str = yaml.dump(
        dagster_postgres_dict,
        indent=2,
    )

    with open(compose_dagster_postgres.as_posix(), "w") as fw:
        fw.write(dagster_postgres_yml)

    logging.debug(
        "Contents Dagster-Postgres `docker-compose.yml`: \n%s" % dagster_postgres_yml
    )

    return compose_dagster_postgres


#######################################################################################################################
# # Dagster Postgres

# # dagster_postgres_up
@nox.session(python=None, tags=["dagster_postgres_up"])
def dagster_postgres_up(session):
    """
    Start Postgres backend for Dagster in attached mode.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session dagster_postgres_up
    # nox --tags dagster_postgres_up

    sudo = False

    write_dagster_postgres_yml()
    write_dagster_postgres_compose()

    cmd = [
        *cmd_dagster_postgres,
        "up",
        "--remove-orphans",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        env=ENV,
        external=True,
        silent=SESSION_RUN_SILENT,
    )


# # dagster_postgres_clear
@nox.session(python=None, tags=["dagster_postgres_clear"])
def dagster_postgres_clear(session):
    """
    Clear Dagster-Postgres with `sudo`. WARNING: DATA LOSS!

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session dagster_postgres_clear
    # nox --tags dagster_postgres_clear

    sudo = True

    dagster_postgres_root_dir: pathlib.Path = ENVIRONMENT_DAGSTER[
        "DAGSTER_POSTGRES_ROOT_DIR"
    ]

    logging.debug("Clearing Dagster-Postgres...")
    logging.debug("Removing Dir %s" % dagster_postgres_root_dir.as_posix())

    cmd = [
        shutil.which("git"),
        "clean",
        "-x",
        "--force",
        dagster_postgres_root_dir.as_posix(),
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    if dagster_postgres_root_dir.exists():
        logging.warning(
            "Clearing out Dagster-Postgres...\nContinue? Type `yes` to confirm."
        )
        answer = input()
        if answer.lower() == "yes":

            logging.info(f"{cmd = }")

            session.run(
                *cmd,
                env=ENV,
                external=True,
                silent=SESSION_RUN_SILENT,
            )
        else:
            logging.info(
                "Clearing %s was aborted." % dagster_postgres_root_dir.as_posix()
            )
            return 1

    logging.debug("%s removed" % dagster_postgres_root_dir.as_posix())

    return 0


# # dagster_postgres_up_detach
@nox.session(python=None, tags=["dagster_postgres_up_detach"])
def dagster_postgres_up_detach(session):
    """
     Start Postgres backend for Dagster in detached mode.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session dagster_postgres_up_detach
    # nox --tags dagster_postgres_up_detach

    sudo = False

    write_dagster_postgres_yml()
    write_dagster_postgres_compose()

    cmd = [
        *cmd_dagster_postgres,
        "up",
        "--remove-orphans",
        "--detach",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        env=ENV,
        external=True,
        silent=SESSION_RUN_SILENT,
    )


# # dagster_postgres_down
@nox.session(python=None, tags=["dagster_postgres_down"])
def dagster_postgres_down(session):
    """
    Shut down Postgres backend for Dagster.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session dagster_postgres_up
    # nox --tags dagster_postgres_up

    sudo = False

    cmd = [
        *cmd_dagster_postgres,
        "down",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        env=ENV,
        external=True,
        silent=SESSION_RUN_SILENT,
    )


@nox.session(python=None, tags=["dagster_postgres"])
def dagster_postgres(session):
    """
    Start Dagster with Postgres as backend after `nox --session dagster_postgres_up_detach`.

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session dagster_postgres
    # nox --tags dagster_postgres

    sudo = False

    cmd = [
        shutil.which("dagster"),
        "dev",
        "--host",
        "0.0.0.0",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    logging.info(f"{cmd = }")

    session.run(
        *cmd,
        env={
            "DAGSTER_HOME": ENVIRONMENT_DAGSTER["DAGSTER_POSTGRES_ROOT_DIR"],
        },
        external=True,
        silent=SESSION_RUN_SILENT,
    )


# # dagster_mysql_clear
@nox.session(python=None, tags=["dagster_mysql_clear"])
def dagster_mysql_clear(session):
    """
    Clear Dagster-Postgres with `sudo`. WARNING: DATA LOSS!

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session dagster_mysql_clear
    # nox --tags dagster_mysql_clear

    sudo = True

    dagster_mysql_root_dir: pathlib.Path = ENVIRONMENT_DAGSTER["DAGSTER_MYSQL_ROOT_DIR"]

    logging.debug("Clearing Dagster-MySQL...")
    logging.debug("Removing Dir %s" % dagster_mysql_root_dir.as_posix())

    cmd = [
        shutil.which("git"),
        "clean",
        "-x",
        "--force",
        dagster_mysql_root_dir.as_posix(),
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        cmd.insert(1, "--reset-timestamp")
        # cmd.insert(2, "--stdin")

    if dagster_mysql_root_dir.exists():
        logging.warning(
            "Clearing out Dagster-MySQL...\nContinue? Type `yes` to confirm."
        )
        answer = input()
        if answer.lower() == "yes":

            logging.info(f"{cmd = }")

            session.run(
                *cmd,
                env=ENV,
                external=True,
                silent=SESSION_RUN_SILENT,
            )
        else:
            logging.info("Clearing %s was aborted." % dagster_mysql_root_dir.as_posix())
            return 1

    logging.debug("%s removed" % dagster_mysql_root_dir.as_posix())

    return 0


@nox.session(python=None, tags=["dagster_mysql"])
def dagster_mysql(session):
    """
    Start Dagster with MySQL as backend (not recommended).

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session dagster_mysql
    # nox --tags dagster_mysql

    sudo = False

    cmd = [
        shutil.which("dagster"),
        "dev",
        "--host",
        "0.0.0.0",
    ]

    if sudo:
        cmd.insert(0, shutil.which("sudo"))
        # cmd.insert(1, "--stdin")

    session.run(
        *cmd,
        env={
            "DAGSTER_HOME": ENVIRONMENT_DAGSTER["DAGSTER_MYSQL_ROOT_DIR"],
        },
        external=True,
        silent=SESSION_RUN_SILENT,
    )


#######################################################################################################################


# I guess it's better if this is not even implemented because
# MySQL is wonky and Postgres should be the default backend anyway
# #######################################################################################################################
# # # Dagster MySQL
# @nox.session(python=None, tags=["dagster_mysql"])
# def dagster_mysql(session):
#     """
#     Start Dagster with MySQL (default) as backend.
#
#     Scope:
#     - [x] Engine
#     - [ ] Features
#     """
#     # Ex:
#     # nox --session dagster_mysql
#     # nox --tags dagster_mysql
#
#     dagster_mysql_root_dir: pathlib.Path = ENVIRONMENT_DAGSTER["DAGSTER_MYSQL_ROOT_DIR"]
#     dagster_mysql_root_dir.mkdir(parents=True, exist_ok=True)
#
#     # dagster_postgres_db_dir: pathlib.Path = (
#     #     dagster_mysql_root_dir / ENVIRONMENT_DAGSTER_POSTGRES['DAGSTER_POSTGRES_DB_DIR_DIR']
#     # )
#     # dagster_postgres_db_dir.mkdir(parents=True, exist_ok=True)
#
#     session.run(
#         shutil.which("dagster"),
#         "dev",
#         "--host",
#         "0.0.0.0",
#         env={
#             "DAGSTER_HOME": dagster_mysql_root_dir.as_posix(),
#         },
#         external=True,
#     )
#
#
# #######################################################################################################################


#######################################################################################################################
# SBOM
@nox.session(python=PYTHON_TEST_VERSIONS, tags=["sbom"])
@nox.parametrize(
    "working_directory",
    # https://nox.thea.codes/en/stable/config.html#giving-friendly-names-to-parametrized-sessions
    [
        nox.param(engine_dir.name, id=engine_dir.name),
        *[nox.param(i, id=i.name) for i in FEATURES_PARAMETERIZED],
    ],
)
def sbom(session, working_directory):
    """
    Runs Software Bill of Materials (SBOM).

    Scope:
    - [x] Engine
    - [ ]
    """
    # Ex:
    # nox --session sbom
    # nox --tags sbom

    # https://pypi.org/project/pipdeptree/

    sudo = False

    with session.chdir(engine_dir.parent / working_directory):

        session.log(
            f"Current Session Working Directory:\n\t{pathlib.Path.cwd().as_posix()}"
        )

        session.install(
            "--no-cache-dir",
            "-e",
            ".[sbom]",
            silent=SESSION_INSTALL_SILENT,
        )

        sbom_dir = pathlib.Path.cwd() / ".sbom"
        sbom_dir.mkdir(parents=True, exist_ok=True)

        session.run(
            "cyclonedx-py",
            "environment",
            "--output-format",
            "JSON",
            "--output-file",
            sbom_dir / f"cyclonedx-py.{session.python}.json",
            env=ENV,
            # external=True,
            silent=SESSION_RUN_SILENT,
        )

        session.run(
            "bash",
            "-c",
            f"pipdeptree --mermaid > {sbom_dir}/pipdeptree.{session.python}.mermaid",
            env=ENV,
            external=True,
            silent=SESSION_RUN_SILENT,
        )

        session.run(
            "bash",
            "-c",
            f"pipdeptree --graph-output dot > {sbom_dir}/pipdeptree.{session.python}.dot",
            env=ENV,
            external=True,
            silent=SESSION_RUN_SILENT,
        )


#######################################################################################################################


#######################################################################################################################
# Coverage
@nox.session(python=PYTHON_TEST_VERSIONS, tags=["coverage"])
@nox.parametrize(
    "working_directory",
    # https://nox.thea.codes/en/stable/config.html#giving-friendly-names-to-parametrized-sessions
    [
        nox.param(engine_dir.name, id=engine_dir.name),
        *[nox.param(i, id=i.name) for i in FEATURES_PARAMETERIZED],
    ],
)
def coverage(session, working_directory):
    """
    Runs coverage (not implemented).

    Scope:
    - [x] Engine
    - [x] Features
    """
    # Ex:
    # nox --session coverage
    # nox --tags coverage

    session.skip("Not implemented")

    sudo = False

    with session.chdir(engine_dir.parent / working_directory):

        session.log(
            f"Current Session Working Directory:\n\t{pathlib.Path.cwd().as_posix()}"
        )

        session.install(
            "--no-cache-dir",
            "-e",
            ".[coverage]",
            silent=SESSION_INSTALL_SILENT,
        )

        session.run(
            "coverage",
            "run",
            "--source",
            "src",
            "-m",
            "pytest",
            "-sv",
            env=ENV,
            # external=True,
            silent=SESSION_RUN_SILENT,
        )  # ./.coverage
        session.run(
            "coverage",
            "report",
            # external=True,
            silent=SESSION_RUN_SILENT,
        )  # report to console
        # session.run("coverage", "json", "-o", ".coverage", "coverage.json")  # report to json
        session.run(
            "coverage",
            "json",
            "-o",
            "coverage.json",
            # external=True,
            silent=SESSION_RUN_SILENT,
        )  # report to json
        # session.run("coverage", "xml")  # ./coverage.xml
        # session.run("coverage", "html")  # ./htmlcov/


#######################################################################################################################


#######################################################################################################################
# Lint
@nox.session(python=PYTHON_TEST_VERSIONS, tags=["lint"])
@nox.parametrize(
    "working_directory",
    # https://nox.thea.codes/en/stable/config.html#giving-friendly-names-to-parametrized-sessions
    [
        nox.param(engine_dir.name, id=engine_dir.name),
        *[nox.param(i, id=i.name) for i in FEATURES_PARAMETERIZED],
    ],
)
def lint(session, working_directory):
    """
    Runs linters and fixers

    Scope:
    - [x] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session lint
    # nox --tags lint

    sudo = False

    with session.chdir(engine_dir.parent / working_directory):

        session.log(
            f"Current Session Working Directory:\n\t{pathlib.Path.cwd().as_posix()}"
        )

        session.install(
            "--no-cache-dir",
            "-e",
            ".[lint]",
            silent=SESSION_INSTALL_SILENT,
        )

        # exclude = [
        #     # Add one line per exclusion:
        #     # "--extend-exclude '^.ext'",
        #     "--extend-exclude", "'^.svg'",
        # ]

        session.run(
            "black",
            "src",
            *session.posargs,
            # external=True,
            silent=SESSION_RUN_SILENT,
        )
        session.run(
            "isort",
            "--profile",
            "black",
            "src",
            *session.posargs,
            # external=True,
            silent=SESSION_RUN_SILENT,
        )

        if pathlib.PosixPath(".pre-commit-config.yaml").absolute().exists():
            session.run(
                "pre-commit",
                "run",
                "--all-files",
                *session.posargs,
                # external=True,
                silent=SESSION_RUN_SILENT,
            )

        # # nox > Command pylint src failed with exit code 30
        # # nox > Session lint-3.12 failed.
        # session.run("pylint", "src")
        # # https://github.com/actions/starter-workflows/issues/2303#issuecomment-1973743119
        session.run(
            "pylint",
            "--exit-zero",
            "src",
            # external=True,
            silent=SESSION_RUN_SILENT,
        )
        # session.run("pylint", "--disable=C0114,C0115,C0116", "--exit-zero", "src")
        # https://stackoverflow.com/questions/7877522/how-do-i-disable-missing-docstring-warnings-at-a-file-level-in-pylint
        # C0114 (missing-module-docstring)
        # C0115 (missing-class-docstring)
        # C0116 (missing-function-docstring)


#######################################################################################################################


#######################################################################################################################
# Testing
@nox.session(python=PYTHON_TEST_VERSIONS, tags=["testing"])
@nox.parametrize(
    "working_directory",
    # https://nox.thea.codes/en/stable/config.html#giving-friendly-names-to-parametrized-sessions
    [
        nox.param(engine_dir.name, id=engine_dir.name),
        *[nox.param(i, id=i.name) for i in FEATURES_PARAMETERIZED],
    ],
)
def testing(session, working_directory):
    """
    Runs pytests (not implemented).

    Scope:
    - [x] Engine
    - [x] Features
    """
    # Ex:
    # nox --session testing
    # nox --tags testing

    session.skip("Not implemented")

    sudo = False

    with session.chdir(engine_dir.parent / working_directory):

        session.log(
            f"Current Session Working Directory:\n\t{pathlib.Path.cwd().as_posix()}"
        )

        session.install(
            "--no-cache-dir",
            "-e",
            ".[testing]",
            silent=SESSION_INSTALL_SILENT,
        )

        session.run(
            "pytest",
            *session.posargs,
            env=ENV,
            # external=True,
            silent=SESSION_RUN_SILENT,
        )


#######################################################################################################################


#######################################################################################################################
# Readme
@nox.session(python=PYTHON_VERSION_MAIN, tags=["readme"])
@nox.parametrize(
    "working_directory",
    # https://nox.thea.codes/en/stable/config.html#giving-friendly-names-to-parametrized-sessions
    [
        # nox.param(engine_dir.name, id=engine_dir.name),  # readme is not built for OpenStudioLandscapes.engine
        *[nox.param(i, id=i.name) for i in FEATURES_PARAMETERIZED]
    ],
)
def readme(session, working_directory):
    """
    Generate dynamic README.md file for OpenStudioLandscapes modules.

    Scope:
    - [ ] Engine
    - [x] Features
    """
    # Ex:
    # nox --session readme
    # nox --tags readme

    sudo = False

    with session.chdir(engine_dir.parent / working_directory):

        session.log(
            f"Current Session Working Directory:\n\t{pathlib.Path.cwd().as_posix()}"
        )

        session.install(
            "--no-cache-dir",
            "-e",
            ".[readme]",
            silent=SESSION_INSTALL_SILENT,
        )

        session.run(
            "generate-readme",
            "--versions",
            *PYTHON_TEST_VERSIONS,
            # external=True,
            silent=SESSION_RUN_SILENT,
        )


#######################################################################################################################


#######################################################################################################################
# Release
# Todo
@nox.session(python=PYTHON_TEST_VERSIONS, tags=["release"])
@nox.parametrize(
    "working_directory",
    # https://nox.thea.codes/en/stable/config.html#giving-friendly-names-to-parametrized-sessions
    [
        nox.param(engine_dir.name, id=engine_dir.name),
        *[nox.param(i, id=i.name) for i in FEATURES_PARAMETERIZED],
    ],
)
def release(session, working_directory):
    """
    Build and release to a repository (not implemented).

    Scope:
    - [x] Engine
    - [x] Features
    """
    # Ex:
    # nox --session release
    # nox --tags release

    session.skip("Not implemented")

    sudo = False

    with session.chdir(engine_dir.parent / working_directory):

        session.log(
            f"Current Session Working Directory:\n\t{pathlib.Path.cwd().as_posix()}"
        )

        session.install(
            "--no-cache-dir",
            "-e",
            ".[release]",
            silent=SESSION_INSTALL_SILENT,
        )

        pypi_user: str = os.environ.get("PYPI_USER")
        pypi_pass: str = os.environ.get("PYPI_PASS")
        if not pypi_user or not pypi_pass:
            session.error(
                "Environment variables for release: PYPI_USER, PYPI_PASS are missing!",
            )
        session.run("poetry", "install", external=True)
        session.run("poetry", "build", external=True)
        session.run(
            "poetry",
            "publish",
            "-r",
            "testpypi",
            "-u",
            pypi_user,
            "-p",
            pypi_pass,
            external=True,
        )


#######################################################################################################################


#######################################################################################################################
# Tag
@nox.session(python=None, tags=["tag"])
@nox.parametrize(
    "working_directory",
    # https://nox.thea.codes/en/stable/config.html#giving-friendly-names-to-parametrized-sessions
    [
        nox.param(engine_dir.name, id=engine_dir.name),
        *[nox.param(i, id=i.name) for i in FEATURES_PARAMETERIZED],
    ],
)
def tag(session, working_directory):
    """
    Git tag OpenStudioLandscapes modules.
    See wiki/guides/release_strategy.md#main-release

    Scope:
    - [x] Engine
    - [x] Features
    """
    # Ex:
    # nox --session tag
    # nox --tags tag

    # TAG
    tag_ = os.environ.get("TAG", None)
    if tag_ is None:
        input_message = "Version tag:\n"

        input_message += "v"

        user_input = ""

        while not RE_SEMVER.match(user_input):
            user_input = input(input_message)

        tag_ = f"v{user_input}"
        os.environ["TAG"] = tag_

    # RELEASE_TYPE
    release_type = os.environ.get("RELEASE_TYPE", None)
    if release_type is None:
        release_types = ["rc", "main"]

        input_message = "Tag type:\n"

        for index, item in enumerate(release_types):
            input_message += f"{index + 1}) {item}\n"

        input_message += "Choice: "

        user_input = ""

        while user_input not in map(str, range(1, len(release_types) + 1)):
            user_input = input(input_message)

        release_type = release_types[int(user_input) - 1]
        os.environ["RELEASE_TYPE"] = release_type

    # FORCE
    force = os.environ.get("FORCE", None)
    if force is None:
        forced = ["no", "yes"]

        input_message = "Force:\n"

        for index, item in enumerate(forced):
            input_message += f"{index + 1}) {item}\n"

        input_message += "Choice: "

        user_input = ""

        while user_input not in map(str, range(1, len(forced) + 1)):
            user_input = input(input_message)

        force = forced[int(user_input) - 1]
        os.environ["FORCE"] = force

    session.log(f"{tag_ = }")
    session.log(f"{release_type = }")
    session.log(f"{force = }")

    cmds = []

    cmd_fetch = [
        shutil.which("git"),
        "fetch",
        "--tags",
        "--force",
    ]
    cmds.append(cmd_fetch)

    if release_type == "rc":
        msg = f"Release Candidate Version {tag_}"
    elif release_type == "main":
        msg = f"Main Release Version {tag_}"

    cmd_annotate = [
        shutil.which("git"),
        "tag",
        "--annotate",
        tag_,
        "--message",
        msg,
    ]
    if force == "yes":
        cmd_annotate.append("--force")
    cmds.append(cmd_annotate)

    if release_type == "main":

        cmd_annotate_latest = [
            shutil.which("git"),
            "tag",
            "--annotate",
            "latest",
            "--message",
            f"Latest Release Version (pointing to {tag_}",
            "%s^{}" % tag_,
        ]
        if force == "yes":
            cmd_annotate_latest.append("--force")
        cmds.append(cmd_annotate_latest)

    cmd_push = [
        shutil.which("git"),
        "push",
        "--tags",
    ]
    if force == "yes":
        cmd_push.append("--force")
    cmds.append(cmd_push)

    with session.chdir(engine_dir.parent / working_directory):

        session.log(
            f"Current Session Working Directory:\n\t{pathlib.Path.cwd().as_posix()}"
        )

        for cmd in cmds:

            session.log(f"Running Command:\n\t{shlex.join(cmd)}")

            session.run(
                *cmd,
                env=ENV,
                external=True,
                silent=SESSION_RUN_SILENT,
            )


@nox.session(python=None, tags=["tag_delete"])
@nox.parametrize(
    "working_directory",
    # https://nox.thea.codes/en/stable/config.html#giving-friendly-names-to-parametrized-sessions
    [
        nox.param(engine_dir.name, id=engine_dir.name),
        *[nox.param(i, id=i.name) for i in FEATURES_PARAMETERIZED],
    ],
)
def tag_delete(session, working_directory):
    """
    Git tag delete OpenStudioLandscapes modules.
    See wiki/guides/release_strategy.md#delete-tags

    Scope:
    - [x] Engine
    - [x] Features
    """
    # Ex:
    # nox --session tag_delete
    # nox --tags tag_delete

    # TAG
    tag_ = os.environ.get("TAG", None)
    if tag_ is None:
        input_message = "Version tag:\n"

        input_message += "v"

        user_input = ""

        while not RE_SEMVER.match(user_input):
            user_input = input(input_message)

        tag_ = f"v{user_input}"
        os.environ["TAG"] = tag_

    cmds = []

    cmd_fetch = [
        shutil.which("git"),
        "fetch",
        "--tags",
        "--force",
    ]
    cmds.append(cmd_fetch)

    cmd_delete_tag = [
        shutil.which("git"),
        "tag",
        "-d",
        tag_,
    ]
    cmds.append(cmd_delete_tag)

    cmd_push = [
        shutil.which("git"),
        "push",
        "origin",
        f":refs/tags/{tag_}",
    ]
    cmds.append(cmd_push)

    with session.chdir(engine_dir.parent / working_directory):

        session.log(
            f"Current Session Working Directory:\n\t{pathlib.Path.cwd().as_posix()}"
        )

        for cmd in cmds:

            session.log(f"Running Command:\n\t{shlex.join(cmd)}")

            session.run(
                *cmd,
                env=ENV,
                external=True,
                silent=SESSION_RUN_SILENT,
            )


#######################################################################################################################


#######################################################################################################################
# PR
# Todo:
#  - [x] gh_login
#        See wiki/guides/release_strategy.md#pull-requests-gh
#  - [x] gh_pr_create
#        See wiki/guides/release_strategy.md#create-pr
#  - [x] gh_pr_edit
#        See wiki/guides/release_strategy.md#edit-pr
#  - [ ] gh_pr_close
#        See wiki/guides/release_strategy.md#close-pr
#  - [ ] gh_pr_merge
#  - [ ] gh_pr_close


@nox.session(python=None, tags=["gh_login"])
def gh_login(session):
    """
    GitHub CLI Login.
    See wiki/guides/release_strategy.md#pull-requests-gh

    Scope:
    - [ ] Engine
    - [ ] Features
    """
    # Ex:
    # nox --session gh_login
    # nox --tags gh_login

    # sudo = False

    cmds = []

    gh = shutil.which("gh")

    if bool(gh):

        cmd_gh_login = [
            gh,
            "auth",
            "login",
            "--web",
        ]
        cmds.append(cmd_gh_login)

        for cmd in cmds:

            session.log(f"Running Command:\n\t{shlex.join(cmd)}")

            session.run(
                *cmd,
                env=ENV,
                external=True,
                silent=SESSION_RUN_SILENT,
            )

    else:
        msg = "No Github CLI Found."
        session.skip(msg)


@nox.session(python=None, tags=["gh_pr_create"])
@nox.parametrize(
    "working_directory",
    # https://nox.thea.codes/en/stable/config.html#giving-friendly-names-to-parametrized-sessions
    [
        nox.param(engine_dir.name, id=engine_dir.name),
        *[nox.param(i, id=i.name) for i in FEATURES_PARAMETERIZED],
    ],
)
def gh_pr_create(session, working_directory):
    """
    Create PR (draft) for OpenStudioLandscapes modules.
    See wiki/guides/release_strategy.md#create-pr

    Scope:
    - [x] Engine
    - [x] Features
    """
    # Ex:
    # nox --session gh_pr_create
    # nox --tags gh_pr_create

    # BRANCH
    branch = os.environ.get("BRANCH", None)
    if branch is None:
        input_message = "Branch:\n"

        # input_message += "v"

        # user_input = ""

        # while not RE_SEMVER.match(user_input):
        branch = input(input_message)

        # branch = f"v{user_input}"
        os.environ["BRANCH"] = branch

    # DRY_RUN
    dry_run = os.environ.get("DRY_RUN", None)
    if dry_run is None:
        options = ["yes", "no"]

        input_message = "Dry run:\n"

        for index, item in enumerate(options):
            input_message += f"{index + 1}) {item}\n"

        input_message += "Choice: "

        user_input = ""

        while user_input not in map(str, range(1, len(options) + 1)):
            user_input = input(input_message)

        dry_run = options[int(user_input) - 1]
        os.environ["DRY_RUN"] = dry_run

    cmds = []

    gh = shutil.which("gh")

    # body_file = str(os.environ.get("BODY_FILE", ""))
    # session.log(f"{body_file = }")

    if bool(gh):

        cmd_gh_pr_create = [
            gh,
            "pr",
            "create",
            "--draft",
            "--title",
            branch,
            "--head",
            branch,
            "--base",
            GIT_MAIN_BRANCH,
            # Todo
            #  - [ ] --body-file
            "--body",
            "",
        ]
        if dry_run:
            cmd_gh_pr_create.append("--dry-run")
        cmds.append(cmd_gh_pr_create)

        with session.chdir(engine_dir.parent / working_directory):

            session.log(
                f"Current Session Working Directory:\n\t{pathlib.Path.cwd().as_posix()}"
            )

            if dry_run:
                session.warn(f"DRY_RUN is set to {dry_run}")

            for cmd in cmds:

                session.log(f"Running Command:\n\t{shlex.join(cmd)}")

                session.run(
                    *cmd,
                    env=ENV,
                    external=True,
                    silent=SESSION_RUN_SILENT,
                )

    else:
        msg = "No Github CLI Found."
        session.skip(msg)


@nox.session(python=None, tags=["gh_pr_set_mode"])
@nox.parametrize(
    "working_directory",
    # https://nox.thea.codes/en/stable/config.html#giving-friendly-names-to-parametrized-sessions
    [
        nox.param(engine_dir.name, id=engine_dir.name),
        *[nox.param(i, id=i.name) for i in FEATURES_PARAMETERIZED],
    ],
)
def gh_pr_set_mode(session, working_directory):
    """
    Set mode for OpenStudioLandscapes PRs.
    See wiki/guides/release_strategy.md#edit-pr

    Scope:
    - [x] Engine
    - [x] Features
    """
    # Ex:
    # nox --session gh_pr_set_mode
    # nox --tags gh_pr_set_mode

    # BRANCH
    branch = os.environ.get("BRANCH", None)
    if branch is None:
        input_message = "Branch:\n"

        # input_message += "v"

        # user_input = ""

        # while not RE_SEMVER.match(user_input):
        branch = input(input_message)

        # branch = f"v{user_input}"
        os.environ["BRANCH"] = branch

    # RELEASE_TYPE
    mode = os.environ.get("MODE", None)
    if mode is None:
        modes = ["draft", "ready"]

        input_message = "PR mode:\n"

        for index, item in enumerate(modes):
            input_message += f"{index + 1}) {item}\n"

        input_message += "Choice: "

        user_input = ""

        while user_input not in map(str, range(1, len(modes) + 1)):
            user_input = input(input_message)

        mode = modes[int(user_input) - 1]
        os.environ["MODE"] = mode

    cmds = []

    gh = shutil.which("gh")

    # # defaults to draft if not overridden
    # _mode = os.environ.get("MODE", "draft").lower()
    # if _mode not in ["draft", "ready"]:
    #     session.error("MODE must be draft or ready.")
    # modes = str(_mode)

    # body_file = str(os.environ.get("BODY_FILE", ""))
    # session.log(f"{body_file = }")

    if bool(gh):

        # branch_name = session.posargs
        #
        # if len(branch_name) != 1:
        #     msg = "Invalid branch name. Tag argument must be exactly 1 argument."
        #     session.warn(msg)
        #     raise ValueError(msg)
        #
        # branch_name = branch_name[0]

        cmd_gh_pr_set_mode = [
            gh,
            "pr",
            "ready",
            branch,
        ]
        if mode == "draft":
            cmd_gh_pr_set_mode.append("--undo")
        cmds.append(cmd_gh_pr_set_mode)

        with session.chdir(engine_dir.parent / working_directory):

            session.log(
                f"Current Session Working Directory:\n\t{pathlib.Path.cwd().as_posix()}"
            )

            session.warn(f"MODE is set to '{mode}'")

            for cmd in cmds:

                session.log(f"Running Command:\n\t{shlex.join(cmd)}")

                session.run(
                    *cmd,
                    env=ENV,
                    external=True,
                    silent=SESSION_RUN_SILENT,
                )

    else:
        msg = "No Github CLI Found."
        session.skip(msg)


#######################################################################################################################
