import os
import shutil
import subprocess


class PotraceNotFound(Exception):
    pass


class BMPtoSVG:
    """Converter class to convert character BMPs to BMPs and SVGs."""

    def convert(self, directory):
        """Call converters on each .bmp in the provider directory.

        Walk through the custom directory containing all .bmp files
        from sheettobmp and convert them to svg.
        """
        path = os.walk(directory)
        for root, dirs, files in path:
            for f in files:
                if f.endswith(".bmp"):
                    self.bmpToSvg(root + "/" + f)

    def bmpToSvg(self, path):
        """Convert .bmp image to .svg using potrace.

        Converts the passed .bmp file to .svg using the potrace
        (http://potrace.sourceforge.net/). Each .bmp is passed as
        a parameter to potrace which is called as a subprocess.

        Parameters
        ----------
        path : str
            Path to the bmp file to be converted.

        Raises
        ------
        PotraceNotFound
            Raised if potrace not found in path by shutil.which()
        """
        if shutil.which("potrace") is None:
            raise PotraceNotFound("Potrace is either not installed or not in path")
        else:
            subprocess.run(["potrace", path, "-b", "svg", "-o", path[0:-4] + ".svg"])
