import enum
import pathlib
from typing import List

from dagster import get_dagster_logger
from pydantic import (
    Field,
    PositiveInt,
)

LOGGER = get_dagster_logger(__name__)

from OpenStudioLandscapes.engine.config.models import FeatureBaseModel
from OpenStudioLandscapes.engine.config.str_gen import get_config_str

from OpenStudioLandscapes.Template import constants, dist


class Branches(enum.StrEnum):
    main = "main"


class Config(FeatureBaseModel):

    feature_name: str = dist.name

    group_name: str = constants.ASSET_HEADER["group_name"]

    key_prefixes: List[str] = constants.ASSET_HEADER["key_prefix"]

    enabled: bool = False

    ENV_VAR_PORT_HOST: PositiveInt = Field(
        default=1234,
        description="The host port.",
        frozen=True,
    )
    ENV_VAR_PORT_CONTAINER: PositiveInt = Field(
        default=2345,
        description="The Ayon container port.",
        frozen=False,
    )

    MOUNTED_VOLUME: pathlib.Path = Field(
        description="The host side mounted volume.",
        default=pathlib.Path("{DOT_LANDSCAPES}/{LANDSCAPE}/{FEATURE}/volume"),
    )

    # EXPANDABLE PATHS
    @property
    def MOUNTED_VOLUME_expanded(self) -> pathlib.Path:
        LOGGER.debug(f"{self.env = }")
        if self.env is None:
            raise KeyError("`env` is `None`.")
        LOGGER.debug(f"Expanding {self.MOUNTED_VOLUME}...")
        ret = pathlib.Path(
            self.MOUNTED_VOLUME.expanduser()
            .as_posix()
            .format(
                **{
                    "FEATURE": self.feature_name,
                    **self.env,
                }
            )
        )
        return ret


CONFIG_STR = get_config_str(
    Config=Config,
)
