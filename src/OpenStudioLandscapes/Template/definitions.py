from dagster import (
    Definitions,
    load_assets_from_modules,
)

import OpenStudioLandscapes.<Your_New_Module>.assets
import OpenStudioLandscapes.<Your_New_Module>.constants


assets = load_assets_from_modules(
    modules=[OpenStudioLandscapes.<Your_New_Module>.assets],
)

constants = load_assets_from_modules(
    modules=[OpenStudioLandscapes.<Your_New_Module>.constants],
)


defs = Definitions(
    assets=[
        *assets,
        *constants,
    ],
)
