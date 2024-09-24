import os
import shutil
import tempfile

from bmptosvg import BMPtoSVG
from sheettobmp import SHEETtoBMP
from svgtottf import SVGtoTTF


def run(sheet, output_directory, characters_dir, config, metadata):
    SHEETtoBMP().convert(sheet, characters_dir, config)
    BMPtoSVG().convert(directory=characters_dir)
    SVGtoTTF().convert(characters_dir, output_directory, config, metadata)


def main(sheet, output_directory, directory=None, config=None, metadata=None):
    if not directory:
        directory = tempfile.mkdtemp()
        isTempdir = True
    else:
        isTempdir = False

    if config is None:
        config = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "default.json"
        )
    if os.path.isdir(config):
        raise IsADirectoryError("Config parameter should not be a directory.")

    if os.path.isdir(sheet):
        raise IsADirectoryError("Sheet parameter should not be a directory.")
    else:
        run(sheet, output_directory, directory, config, metadata)

    if isTempdir:
        shutil.rmtree(directory)



main("img.jpg", "output", "output")
