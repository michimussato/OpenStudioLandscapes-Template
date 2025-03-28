import copy
import json
import pathlib
import shutil
import tempfile
import textwrap
import urllib.parse

import time
from typing import Generator

import yaml
from python_on_whales import Builder

from dagster import (
    AssetExecutionContext,
    AssetIn,
    AssetKey,
    AssetMaterialization,
    MetadataValue,
    Output,
    asset,
    AssetsDefinition,
)

from OpenStudioLandscapes.engine.base.assets import KEY_BASE
from OpenStudioLandscapes.engine.constants import *

from OpenStudioLandscapes.engine.enums import *
from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.docker import *

from OpenStudioLandscapes.engine.base.ops import (
    op_compose,
    op_docker_compose_graph,
    op_group_out,
)

from OpenStudioLandscapes.Template.constants import *


@asset(
    **ASSET_HEADER,
    ins={
        "group_in": AssetIn(
            AssetKey([*KEY_BASE, "group_out"])
        ),
    },
    deps=[
        AssetKey([*ASSET_HEADER['key_prefix'], f"constants_{ASSET_HEADER['group_name']}"])
    ],
)
def env(
    context: AssetExecutionContext,
    group_in: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:

    env_in = copy.deepcopy(group_in["env"])

    env_in.update(ENVIRONMENT)

    env_in.update(
        {
            "COMPOSE_SCOPE": COMPOSE_SCOPE,
        },
    )

    yield Output(env_in)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(env_in),
            "ENVIRONMENT": MetadataValue.json(ENVIRONMENT),
        },
    )


@asset(
    **ASSET_HEADER,
)
def pip_packages(
    context: AssetExecutionContext,
) -> Generator[Output[list] | AssetMaterialization, None, None]:
    """ """

    _pip_packages: list = []

    yield Output(_pip_packages)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(_pip_packages),
        },
    )


@asset(
    **ASSET_HEADER,
)
def apt_packages(
    context: AssetExecutionContext,
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    _apt_packages = {}

    _apt_packages["list_a"] = [
        "git",
        "ca-certificates",
        "htop",
        "file",
        "tzdata",
        "curl",
        "wget",
        "ffmpeg",
        "xvfb",
        "libegl1",
        "libsm6",
        "libsm6",
        "libglu1-mesa",
        "libxss1",
    ]

    _apt_packages["list_b"] = [
        "build-essential",
        "pkg-config",
        "zlib1g-dev",
        "libncurses5-dev",
        "libgdbm-dev",
        "libnss3-dev",
        "libssl-dev",
        "libreadline-dev",
        "libffi-dev",
        "libsqlite3-dev",
        "libbz2-dev",
        "iproute2",
    ]

    yield Output(_apt_packages)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(_apt_packages),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*KEY, "env"]),
        ),
        "group_in": AssetIn(
            AssetKey([*KEY_BASE, "group_out"])
        ),
        "apt_packages": AssetIn(
            AssetKey([*KEY, "apt_packages"]),
        ),
        "pip_packages": AssetIn(
            AssetKey([*KEY, "pip_packages"]),
        ),
    },
)
def build_docker_image(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    group_in: dict,  # pylint: disable=redefined-outer-name
    apt_packages: dict[str, list[str]],  # pylint: disable=redefined-outer-name
    pip_packages: list,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    build_base_image_data: dict = group_in["docker_image"]
    build_base_docker_config: DockerConfig = group_in["docker_config"]
    build_base_parent_image_name: str = build_base_image_data["image_name"]

    docker_builder: Builder = group_in["docker_builder"]

    docker_file = pathlib.Path(
        env["DOT_LANDSCAPES"],
        env.get("LANDSCAPE"),
        f"{GROUP}__{'__'.join(KEY)}",
        "__".join(context.asset_key.path),
        "Dockerfiles",
        "Dockerfile",
    )

    image_name = get_image_name(context=context)
    image_path = parse_docker_image_path(
        image_name=image_name,
        docker_config=build_base_docker_config,
    )

    shutil.rmtree(docker_file.parent, ignore_errors=True)

    docker_file.parent.mkdir(parents=True, exist_ok=True)

    # @formatter:off
    extra_files = {
        "MyFile.txt": env.get(f"PATH_TO_LOCAL_MY_FILE_TXT"),
    }
    # @formatter:on

    tags = [
        env.get('LANDSCAPE', str(time.time())),
    ]

    apt_install_str_list_a: str = get_apt_install_str(
        apt_install_packages=apt_packages["list_a"],
    )

    apt_install_str_list_b: str = get_apt_install_str(
        apt_install_packages=apt_packages["list_b"],
    )

    pip_install_str: str = get_pip_install_str(pip_install_packages=pip_packages)

    if bool(extra_files):

        with tempfile.TemporaryDirectory(
            dir=docker_file.parent,
            prefix="installer__",
        ) as tmpdir:

            copy_str: str = get_copy_str(
                temp_dir=tmpdir,
                copy_packages=extra_files,
                mode=755,
            )

            # @formatter:off
            docker_file_str = textwrap.dedent(
                """
                # {auto_generated}
                # {dagster_url}
                FROM {parent_image} AS {image_name}
                LABEL authors="{AUTHOR}"
    
                ARG DEBIAN_FRONTEND=noninteractive
        
                ENV CONTAINER_TIMEZONE={TIMEZONE}
                ENV SET_CONTAINER_TIMEZONE=true
    
                SHELL ["/bin/bash", "-c"]
    
                RUN apt-get update && apt-get upgrade -y

                {apt_install_str_list_a}
        
                {apt_install_str_list_b}
    
                {pip_install_str}
    
                WORKDIR /workdir
    
                {copy_str}
    
                # RUN commands
                # [...]
    
                RUN apt-get clean
    
                ENTRYPOINT []
            """
            ).format(
                copy_str=copy_str,
                apt_install_str_list_a=apt_install_str_list_a,
                apt_install_str_list_b=apt_install_str_list_b,
                pip_install_str=pip_install_str.format(
                    **env,
                ),
                auto_generated=f"AUTO-GENERATED by Dagster Asset {'__'.join(context.asset_key.path)}",
                dagster_url=urllib.parse.quote(
                    f"http://localhost:3000/asset-groups/{'%2F'.join(context.asset_key.path)}",
                    safe=":/%",
                ),
                image_name=image_name,
                parent_image=parse_docker_image_path(
                    image_name=build_base_parent_image_name,
                    docker_config=build_base_docker_config,
                    tag=tags[-1],
                ),
                **env,
            )
            # @formatter:on

            # with open(docker_file, "w") as fw:
            #     fw.write(docker_file_str)
            #
            # with open(docker_file, "r") as fr:
            #     docker_file_content = fr.read()

            for key, value in extra_files.items():
                shutil.copyfile(
                    src=value,
                    dst=pathlib.Path(tmpdir) / key,
                )

    else:

        # @formatter:off
        docker_file_str = textwrap.dedent(
            """
            # {auto_generated}
            # {dagster_url}
            FROM {parent_image} AS {image_name}
            LABEL authors="{AUTHOR}"
    
            ARG DEBIAN_FRONTEND=noninteractive
    
            ENV CONTAINER_TIMEZONE={TIMEZONE}
            ENV SET_CONTAINER_TIMEZONE=true
    
            RUN apt-get update && apt-get upgrade -y
    
            {apt_install_str_base}
    
            {apt_install_str_build_python311}
    
            WORKDIR /workdir
    
            # RUN commands
            # [...]
    
            {pip_install_str}
    
            RUN apt-get clean
    
            ENTRYPOINT []
        """
        ).format(
            apt_install_str_list_a=apt_install_str_list_a,
            apt_install_str_list_b=apt_install_str_list_b,
            pip_install_str=pip_install_str.format(
                **env,
            ),
            auto_generated=f"AUTO-GENERATED by Dagster Asset {'__'.join(context.asset_key.path)}",
            dagster_url=urllib.parse.quote(
                f"http://localhost:3000/asset-groups/{'%2F'.join(context.asset_key.path)}",
                safe=":/%",
            ),
            image_name=image_name,
            **env,
        )
        # @formatter:on

    with open(docker_file, "w") as fw:
        fw.write(docker_file_str)

    with open(docker_file, "r") as fr:
        docker_file_content = fr.read()

    image_data = {
        "image_name": image_name,
        "image_path": image_path,
        "image_tags": tags,
        "image_parent": copy.deepcopy(build_base_image_data),
    }

    log: str = docker_build(
        context=context,
        docker_config=build_base_docker_config,
        context_path=docker_file.parent,
        docker_use_cache=DOCKER_USE_CACHE,
        builder=docker_builder,
        image_data=image_data,
    )

    yield Output(image_data)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(image_data),
            "docker_file": MetadataValue.md(
                f"```shell\n{docker_file_content}\n```"
            ),
            "build_logs": MetadataValue.md(f"```shell\n{log}\n```"),
            "env_10_2": MetadataValue.json(env),
        },
    )


@asset(
    **ASSET_HEADER,
)
def compose_networks(
    context: AssetExecutionContext,
) -> Generator[
    Output[dict[str, dict[str, dict[str, str]]]] | AssetMaterialization, None, None]:

    compose_network_mode = ComposeNetworkMode.DEFAULT

    if compose_network_mode == ComposeNetworkMode.DEFAULT:
        docker_dict = {
            "networks": {
                "template": {
                    "name": "network_template",
                },
            },
        }

    else:
        docker_dict = {
            "network_mode": compose_network_mode.value,
        }

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "compose_network_mode": MetadataValue.text(compose_network_mode.value),
            "docker_dict": MetadataValue.md(
                f"```json\n{json.dumps(docker_dict, indent=2)}\n```"
            ),
            "docker_yaml": MetadataValue.md(f"```shell\n{docker_yaml}\n```"),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "env": AssetIn(
            AssetKey([*KEY, "env"]),
        ),
        "build": AssetIn(
            AssetKey([*KEY, "build_docker_image"]),
        ),
        "compose_networks": AssetIn(
            AssetKey([*KEY, "compose_networks"]),
        ),
    },
)
def compose_template(
    context: AssetExecutionContext,
    build: dict,  # pylint: disable=redefined-outer-name
    env: dict,  # pylint: disable=redefined-outer-name
    compose_networks: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    network_dict = {}
    ports_dict = {}

    if "networks" in compose_networks:
        network_dict = {
            "networks": list(compose_networks.get("networks", {}).keys())
        }
        ports_dict = {
            "ports": [
                f"{env.get('PORT_HOST')}:{env.get('PORT_CONTAINER')}",
            ]
        }
    elif "network_mode" in compose_networks:
        network_dict = {
            "network_mode": compose_networks.get("network_mode")
        }

    volumes_dict = {
        "volumes": [],
    }

    docker_dict = {
        "services": {
            "template": {
                "container_name": "template",
                "hostname": "template",
                "domainname": env.get("ROOT_DOMAIN"),
                "restart": "always",
                **[
                    {
                        "image": "docker.io/template/template",
                    },
                    {
                        "image": f"{build['image_prefix_full']}{build['image_name']}:{build['image_tags'][0]}",
                    },
                ][1],
                **copy.deepcopy(volumes_dict),
                **copy.deepcopy(network_dict),
                **copy.deepcopy(ports_dict),
                # "environment": {
                # },
                # "healthcheck": {
                # },
                # "command": [
                # ],
            },
        },
    }

    docker_yaml = yaml.dump(docker_dict)

    yield Output(docker_dict)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(docker_dict),
            "docker_yaml": MetadataValue.md(f"```yaml\n{docker_yaml}\n```"),
            # Todo: "cmd_docker_run": MetadataValue.path(cmd_list_to_str(cmd_docker_run)),
        },
    )


@asset(
    **ASSET_HEADER,
    ins={
        "compose_template": AssetIn(
            AssetKey([*KEY, "compose_template"]),
        ),
    },
)
def compose_maps(
    context: AssetExecutionContext,
    **kwargs,  # pylint: disable=redefined-outer-name
) -> Generator[Output[list[dict]] | AssetMaterialization, None, None]:

    ret = list(kwargs.values())

    context.log.info(ret)

    yield Output(ret)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(ret),
        },
    )


compose = AssetsDefinition.from_op(
    op_compose,
    tags_by_output_name={
        "compose": {
            "compose": "third_party",
        },
    },
    group_name=GROUP,
    key_prefix=KEY,
    keys_by_input_name={
        "compose_networks": AssetKey(
            [*KEY, "compose_networks"]
        ),
        "compose_maps": AssetKey(
            [*KEY, "compose_maps"]
        ),
    },
)


group_out = AssetsDefinition.from_op(
    op_group_out,
    can_subset=True,
    group_name=GROUP,
    tags_by_output_name={
        "group_out": {
            "group_out": "third_party",
        },
    },
    key_prefix=KEY,
    keys_by_input_name={
        "compose": AssetKey(
            [*KEY, "compose"]
        ),
        "env": AssetKey(
            [*KEY, "env"]
        ),
        "group_in": AssetKey(
            [*KEY_BASE, "group_out"]
        ),
    },
)


docker_compose_graph = AssetsDefinition.from_op(
    op_docker_compose_graph,
    group_name=GROUP,
    key_prefix=KEY,
    keys_by_input_name={
        "group_out": AssetKey(
            [*KEY, "group_out"]
        ),
        "compose_project_name": AssetKey(
            [*KEY, "compose_project_name"]
        ),
    },
)
