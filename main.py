import time
import fiona
import rasterio
import rasterio.mask
from remove_bg import remove_bg

# config variables
from config import SHP_PATH, IMG_DIR_PATH, IMG_EXT, OUT_DIR_PATH, OUT_EXT

def main():
    print("\nRunning masks...") # PROGRESS UPDATE

    # Open Shapefile   
    with fiona.open(SHP_PATH, "r") as shapefile:
        print("Opening Shapefile...") # PROGRESS UPDATE

        shapes = [feature["geometry"] for feature in shapefile]
        print(f"Loaded file: {shapefile.path}")
        print(f"A total of {len(shapes)} shapes loaded...") # PROGRESS UPDATE

    # Create Output Directory if it doesn't exist yet
    if not OUT_DIR_PATH.exists():
        print("\nOutput directory does not exist...") # PROGRESS UPDATE
        OUT_DIR_PATH.mkdir(parents=True, exist_ok=True)
        print(f"\nOutput directory {OUT_DIR_PATH} successfully created...") # PROGRESS UPDATE

    # Open Raster files
    print("\nLocating rasters...") # PROGRESS UPDATE
    rasters = get_image_files(IMG_DIR_PATH)
    print(f"Located {len(rasters)} rasters...") # PROGRESS UPDATE

    print("\n***MASKING RASTERS*** ...") # PROGRESS UPDATE
    masks = 0
    for index, raster in enumerate(rasters):
        raster_path = str(raster)

        # Apply mask
        print(f"\nIn Progress: Masking Raster {index}...") # PROGRESS UPDATE
        with rasterio.open(raster_path) as src:
            out_image, out_transform = rasterio.mask.mask(src, shapes)
            out_meta = src.meta

        out_filename = f"{raster.stem}{OUT_EXT}"
        out_path = OUT_DIR_PATH.joinpath(out_filename)

        out_meta.update({"driver": "GTiff",
                        "height": out_image.shape[1],
                        "width": out_image.shape[2],
                        "transform": out_transform,
        })

        # Download masked image 
        print(f"In Progress: Downloading Raster {out_path}...") # PROGRESS UPDATE
        with rasterio.open(out_path, "w", **out_meta) as dest:
            dest.write(out_image)

        masks = index
        print(f"Finished: Successfully Masked Raster {index}!!") # PROGRESS UPDATE

    # Remove background for each file
    print("\n***REMOVING BACKGROUNDS*** ...") # PROGRESS UPDATE
    masked_images = get_image_files(OUT_DIR_PATH)

    for index, image in enumerate(masked_images):
        remove_bg(str(image), str(image))

    print("Removed Backgrounds!!")

    return masks + 1



def get_image_files(dir_path):
    files = [file for file in dir_path.iterdir() if file.is_file() and file.suffix.lower() in IMG_EXT]

    return files

if __name__ == "__main__":
    start_time = time.time()
    masks = main()
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"\nCompleted {masks} Masks in {elapsed_time:.2f} seconds")

