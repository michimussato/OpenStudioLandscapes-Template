from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.Template.assets
from OpenStudioLandscapes.Template import (
    dist,
    LOGGER,
)

LOGGER.info(f"Loading {dist.name} assets...")

assets_base = load_assets_from_modules(
    modules=[OpenStudioLandscapes.Template.assets],
)


defs = Definitions(
    assets=[
        *assets_base,
    ],
)
