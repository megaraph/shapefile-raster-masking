import fiona
import rasterio
import rasterio.mask
from shapely.geometry import shape

# config variables
from config import SHP_PATH, IMG_DIR_PATH, IMG_EXT, OUT_DIR_PATH, OUT_EXT

def main():
    print("\nRunning masks...") # PROGRESS UPDATE

    # Open Shapefile   
    with fiona.open(SHP_PATH, "r") as shapefile:
        print("Opening Shapefile...") # PROGRESS UPDATE

        shapes = [feature["geometry"] for feature in shapefile]
        print(f"Loaded file: {shapefile.path}")
        print(f"A total of {len(shapes)} loaded...") # PROGRESS UPDATE

        print("\nLocating rasters...") # PROGRESS UPDATE
        rasters = get_raster_files(IMG_DIR_PATH)
        print(f"Located {len(rasters)} rasters...") # PROGRESS UPDATE

        print("\n***MASKING RASTERS***...") # PROGRESS UPDATE
        for index, raster in enumerate(rasters):
            raster_path = str(raster)

            print(f"\nIn Progress: Masking Raster {index}...") # PROGRESS UPDATE
            with rasterio.open(raster_path) as src:
                out_image, out_transform = rasterio.mask.mask(src, shapes)
                out_meta = src.meta

            out_filename = f"{raster.stem}{OUT_EXT}"
            out_path = OUT_DIR_PATH.joinpath(out_filename)

            # Create output directory if it doesn't exist
            if not out_path.exists():
                print("\nOutput directory does not exist...") # PROGRESS UPDATE
                out_path.mkdir(parents=True, exist_ok=True)
                print(f"\nOutput directory {out_path} successfully created...") # PROGRESS UPDATE

            print(f"\nIn Progress: Downloading Raster {out_path}...") # PROGRESS UPDATE

            out_meta.update({"driver": "GTiff",
                            "height": out_image.shape[1],
                            "width": out_image.shape[2],
                            "transform": out_transform,
            })

            with rasterio.open(out_filename, "w", **out_meta) as dest:
                dest.write(out_image)

            print(f"\nFinished: Successfully Masked Raster {index}!!") # PROGRESS UPDATE



def get_raster_files(dir_path):
    files = [file for file in dir_path.iterdir() if file.is_file() and file.suffix.lower() in IMG_EXT]

    return files

if __name__ == "__main__":
    main()
