"""
Transition frame generation via ImageMagick's convert utility.

Author: Benedikt Vollmerhaus
License: MIT
"""

import filecmp
import subprocess
from pathlib import Path

from blurwal import paths, utils, wallpaper


def generate(output_dir: Path, blur_level: int,
             max_blur_level: int, max_sigma: int) -> None:
    """
    Generate a transition frame by applying a blur to the wallpaper.

    The blur level is given in the range:
      [0, <total no. of transition steps>]

    and then converted to the sigma range:
      [0, <max. sigma when fully blurred>]

    The resulting sigma is then used for ImageMagick's blur operation.
    This means that the highest blur level, i.e. final frame in a blur
    transition, will have been blurred with the given max. sigma value.

    ImageMagick's blur operator needs two values, a radius and a sigma:

    - Radius limits the blurring to pixels that are within that radius
      of the one being blurred. For example, a radius of 1 would limit
      the blurred area to the direct neighbors of each pixel.

    - Sigma determines the blur strength within that radius, i.e. how
      much each of the neighbors in the pixel's radius contributes to
      the blurred area. For example, the largest possible sigma would
      produce a simple averaging of all neighboring pixels.

    See also: https://www.imagemagick.org/Usage/blur/#blur_args

    :param output_dir: Where to save the resulting frame
    :param blur_level: A blur level to blur the wallpaper with
    :param max_blur_level: The max. blur level (total no. of steps)
    :param max_sigma: The sigma to use at the maximum blur level

    :return: None
    """
    output_file = output_dir / f'frame-{blur_level}.jpg'
    sigma = utils.map_range(blur_level, (0, max_blur_level), (0, max_sigma))

    subprocess.run(['convert', wallpaper.get_original(),
                    '-blur', f'0x{sigma}', str(output_file)])


def is_outdated(blur_level: int, max_blur_level: int, max_sigma: int) -> bool:
    """
    Blur the wallpaper with a given blur level and compare the result
    to the already existing frame of that level. If the images differ,
    then the wallpaper changed and the frames need to be regenerated.

    :param blur_level: A blur level whose existing frame to validate
    :param max_blur_level: The max. blur level (total no. of steps)
    :param max_sigma: The sigma to use at the maximum blur level

    :return: Whether the frame of the given blur level is outdated
    """
    generate(paths.TEMP_DIR, blur_level, max_blur_level, max_sigma)

    reference_frame = paths.TEMP_DIR / f'frame-{blur_level}.jpg'
    actual_frame = paths.CACHE_DIR / f'frame-{blur_level}.jpg'

    return not filecmp.cmp(reference_frame, actual_frame)
