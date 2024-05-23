from pathlib import Path

_BASE_PATH = Path.cwd()

# Shapefile Path
_SHP_DIR = "shapefile_masks"
_SHP_FILENAME = "BAGO_RICELANDS.shp"
SHP_PATH = _BASE_PATH.joinpath(_SHP_DIR, _SHP_FILENAME)

# Valid Image Extensions
IMG_EXT = [".png", ".tiff"] 

# Image Directory Path
_IMG_DIR = "raster_images"
IMG_DIR_PATH = _BASE_PATH.joinpath(_IMG_DIR)

# Output Directory Path
_OUT_DIR = "masked_outputs"
OUT_DIR_PATH = _BASE_PATH.joinpath(_OUT_DIR)

# Output Masked Image Extension
OUT_EXT = ".png"
