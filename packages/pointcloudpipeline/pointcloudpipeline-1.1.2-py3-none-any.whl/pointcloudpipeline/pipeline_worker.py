import os
import subprocess
import pdal
import numpy
import json


def convert_laz_to_ept_laz(laz_file, directory_to, untwine_path):
    if not os.path.exists(laz_file):
        return laz_file + " does not exist."
    if not os.path.exists(untwine_path):
        return untwine_path + " does not exist."

    files = '--files=' + str(laz_file)
    out = '--output_dir=' + str(directory_to) + '/' + os.path.splitext(os.path.basename(laz_file))[0]
    untwine_return = subprocess.check_output([str(untwine_path), files, out])
    return untwine_return


def convert_to_laz(file, directory_to):
    if os.path.exists(file):
        if os.path.splitext(os.path.basename(file))[1] == ".las" or os.path.splitext(os.path.basename(file))[1] == ".laz":
            reader_type = "readers.las"
        elif os.path.splitext(os.path.basename(file))[1] == ".e57":
            reader_type = "readers.e57"
        elif os.path.splitext(os.path.basename(file))[1] == ".ply":
            reader_type = "readers.ply"
        else:
            return file + " does not match the supported filetypes laz/las/e57/ply"
        json_pipeline = {
            "pipeline": [
                {
                    "type": reader_type,
                    "filename": file
                },
                {
                    "type": "writers.las",
                    "compression": "laszip",
                    "filename": directory_to + "/" + os.path.splitext(os.path.basename(file))[0] + ".laz"
                }
            ]
        }
        pipeline = pdal.Pipeline(json.dumps(json_pipeline))
        pipeline.execute()
        metadata = pipeline.metadata
        return metadata
    return file + " does not exist."


def convert_from_laz(laz_file, directory_to, type_out):
    if os.path.exists(laz_file):
        if type_out == "las":
            writer = {
                "type": "writers.las",
                "filename": directory_to + "/" + os.path.splitext(os.path.basename(laz_file))[0] + ".las"
            }
        elif type_out == "e57":
            writer = {
                "type": "writers.e57",
                "filename": directory_to + "/" + os.path.splitext(os.path.basename(laz_file))[0] + ".e57"
            }
        elif type_out == "ply":
            writer = {
                "type": "writers.ply",
                "filename": directory_to + "/" + os.path.splitext(os.path.basename(laz_file))[0] + ".ply"
            }
        elif type_out == "laz":
            writer = {
                "type": "writers.las",
                "compression": "laszip",
                "filename": directory_to + "/" + os.path.splitext(os.path.basename(laz_file))[0] + ".laz"
            }
        else:
            return type_out + " does not match supported the filetypes laz/las/e57/ply"
        json_pipeline = {
            "pipeline": [
                {
                    "type": "readers.las",
                    "filename": laz_file
                },
                writer
            ]
        }
        pipeline = pdal.Pipeline(json.dumps(json_pipeline))
        pipeline.execute()
        metadata = pipeline.metadata
        return metadata
    return laz_file + " does not exist."


def convert_laz_to_2d(laz_file, directory_to):
    if os.path.exists(laz_file):
        json_pipeline = {
            "pipeline": [
                laz_file,
                {
                    "type": "filters.outlier",
                    "method": "statistical",
                    "mean_k": "12",
                    "multiplier": "1.0"
                },
                {
                    "type": "filters.range",
                    "limits": "Classification![7:7]"
                },
                {
                    "filename": directory_to + "/" + os.path.splitext(os.path.basename(laz_file))[0] + ".tif",
                    "resolution": "0.05",
                    "output_type": "max",
                    "radius": "0.1",
                    "type": "writers.gdal"
                }
            ]
        }
        pipeline = pdal.Pipeline(json.dumps(json_pipeline))
        pipeline.execute()
        metadata = pipeline.metadata
        return metadata
    return laz_file + " does not exist."
