import copy
import json
from collections import ChainMap
from functools import reduce
from typing import Generator, MutableMapping

import yaml

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
from OpenStudioLandscapes.engine.base.ops import op_docker_compose_graph
from OpenStudioLandscapes.engine.base.ops import op_group_out

from OpenStudioLandscapes.engine.enums import *

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
        "compose_networks": AssetIn(
            AssetKey([*KEY, "compose_networks"]),
        ),
    },
)
def compose_template(
    context: AssetExecutionContext,
    env: dict,  # pylint: disable=redefined-outer-name
    compose_networks: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[dict] | AssetMaterialization, None, None]:
    """ """

    if "networks" in compose_networks:
        network_dict = {
            "networks": list(compose_networks.get("networks", {}).keys())
        }
        ports_dict = {
            "ports": [
                f"{env.get('DAGSTER_DEV_PORT_HOST')}:{env.get('DAGSTER_DEV_PORT_CONTAINER')}",
            ]
        }
    elif "network_mode" in compose_networks:
        network_dict = {
            "network_mode": compose_networks.get("network_mode")
        }
        ports_dict = {}
    else:
        network_dict = {}
        ports_dict = {}

    volumes = []

    docker_dict = {
        "services": {
            "template": {
                "container_name": "template",
                "hostname": "template",
                "domainname": env.get("ROOT_DOMAIN"),
                "restart": "always",
                "image": "template/template",
                **copy.deepcopy(network_dict),
                **copy.deepcopy(ports_dict),
                # "environment": {
                # },
                # "healthcheck": {
                # },
                # "command": [
                # ],
                # "volumes": [
                # ],
                # "ports": [
                #     f"{env.get('<TEMPLATE>_PORT_HOST')}:{env.get('<TEMPLATE>_PORT_CONTAINER')}",
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
        "compose_networks": AssetIn(
            AssetKey([*KEY, "compose_networks"]),
        ),
        "compose_template": AssetIn(
            AssetKey([*KEY, "compose_template"]),
        ),
    },
)
def compose(
    context: AssetExecutionContext,
    compose_networks: dict,  # pylint: disable=redefined-outer-name
    compose_template: dict,  # pylint: disable=redefined-outer-name
) -> Generator[Output[MutableMapping] | AssetMaterialization, None, None]:
    """ """

    if "networks" in compose_networks:
        network_dict = copy.deepcopy(compose_networks)
    else:
        network_dict = {}

    docker_chainmap = ChainMap(
        network_dict,
        compose_template,
    )

    docker_dict = reduce(deep_merge, docker_chainmap.maps)

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


group_out = AssetsDefinition.from_op(
    op_group_out,
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
    },
)
