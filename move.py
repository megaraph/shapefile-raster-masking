import os
from pathlib import Path
import shutil


def move():
    # Define paths
    base = Path.cwd()
    raster_images_path = base.joinpath("raster_images")
    masked_outputs_path = base.joinpath("masked_outputs")
    processed_rasters_path = base.joinpath("processed_rasters")

    # Create processed_rasters directory if it doesn't exist
    if not processed_rasters_path.exists():
        processed_rasters_path.mkdir(parents=True, exist_ok=True)

    # Get all the PNG filenames in masked_outputs
    masked_files = [file.stem for file in masked_outputs_path.glob("*.png")]

    # Move corresponding TIFF files from raster_images to processed_rasters
    for masked_file in masked_files:
        tiff_file = raster_images_path / f"{masked_file}.tiff"
        if tiff_file.exists():
            shutil.move(str(tiff_file), str(processed_rasters_path / tiff_file.name))
            print(f"Moved: {tiff_file.name} to {processed_rasters_path}")


print("All processed raster images have been moved.")


if __name__ == "__main__":
    move()
