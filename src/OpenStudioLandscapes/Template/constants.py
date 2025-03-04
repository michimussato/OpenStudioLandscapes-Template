__all__ = [
    "DOCKER_USE_CACHE",
    "GROUP",
    "KEY",
    "ASSET_HEADER",
    "ENVIRONMENT",
]

from typing import Generator, MutableMapping

from dagster import (
    asset,
    Output,
    AssetMaterialization,
    MetadataValue,
    AssetExecutionContext,
)

from OpenStudioLandscapes.engine.utils import *
from OpenStudioLandscapes.engine.constants import DOCKER_USE_CACHE_GLOBAL


DOCKER_USE_CACHE = DOCKER_USE_CACHE_GLOBAL or False


GROUP = "Template"
KEY = [GROUP]

ASSET_HEADER = {
    "group_name": GROUP,
    "key_prefix": KEY,
    "compute_kind": "python",
}

# @formatter:off
ENVIRONMENT = {
    "DOCKER_USE_CACHE": DOCKER_USE_CACHE,
}
# @formatter:on


@asset(
    name=f"constants_{GROUP}",
    group_name="Constants",
    key_prefix=KEY,
    compute_kind="python",
    description="",
)
def constants(
    context: AssetExecutionContext,
) -> Generator[Output[MutableMapping] | AssetMaterialization, None, None]:
    """ """

    _constants = dict()

    _constants["DOCKER_USE_CACHE"] = DOCKER_USE_CACHE
    _constants["ASSET_HEADER"] = ASSET_HEADER
    _constants["ENVIRONMENT"] = ENVIRONMENT

    yield Output(_constants)

    yield AssetMaterialization(
        asset_key=context.asset_key,
        metadata={
            "__".join(context.asset_key.path): MetadataValue.json(_constants),
        },
    )
