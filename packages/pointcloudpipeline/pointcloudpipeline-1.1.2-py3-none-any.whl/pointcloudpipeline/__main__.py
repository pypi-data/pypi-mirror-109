import click
import os
from .pipeline_worker import convert_to_laz, convert_from_laz, convert_laz_to_ept_laz, convert_laz_to_2d


@click.group()
@click.version_option("1.0.0")
def main():
    """A simple commandline app for managing pointclouds in LAZ"""
    pass


@main.command()
@click.option('--file', required=True, help='File to convert to LAZ')
@click.option('--directoryTo', default=os.getcwd(), help='Directory to save LAZ')
def converttolaz(file, directoryto):
    """Convert a pointcloud from ['las', 'laz', 'e57', 'ply'] to LAZ and save it."""
    pointcloud_metadata = convert_to_laz(file, directoryto)
    print(pointcloud_metadata)
    return pointcloud_metadata


@main.command()
@click.option('--lazFile', required=True, help='LAZ-file to convert')
@click.option('--directoryTo', default=os.getcwd(), help='Directory to save converted file')
@click.option('--convertTo', type=click.Choice(['las', 'laz', 'e57', 'ply'], case_sensitive=False))
def convertfromlaz(lazfile, directoryto, convertto):
    """Convert a LAZ-pointcloud to desired type."""
    pointcloud_metadata = convert_from_laz(lazfile, directoryto, convertto)
    print(pointcloud_metadata)
    return pointcloud_metadata


@main.command()
@click.option('--lazFile', required=True, help='LazFile to convert')
@click.option('--directoryTo', default=os.getcwd(), help='Directory to save')
@click.option('--untwinePath', default=os.getcwd(), help='Path to untwine')
def convertlaztoeptlaz(lazfile, directoryto, untwinepath):
    """Convert a pointcloud from LAZ to EPT-LAZ."""
    converted_laz = convert_laz_to_ept_laz(lazfile, directoryto, untwinepath)
    print(converted_laz)
    return converted_laz


@main.command()
@click.option('--lazFile', required=True, help='LazFile to convert')
@click.option('--directoryTo', default=os.getcwd(), help='Directory to save')
def convertlazto2d(lazfile, directoryto):
    """Convert LAZ to a top rasterview in 2D."""
    metadata_2d = convert_laz_to_2d(lazfile, directoryto)
    print(metadata_2d)
    return metadata_2d


if __name__ == '__main__':
    main()
