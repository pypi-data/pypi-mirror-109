#!/usr/bin/env python3

"""Definition of class DefaultStyle."""

import os
import pkg_resources

from . import StyleClass, Media


class DefaultStyle:  # pylint: disable=R0903
    """DefaultStyle allows to load default style classes of pygwin."""

    @classmethod
    def load(cls) -> None:
        """Load style classes and fonts from the package data directory."""
        data_dir = pkg_resources.resource_filename('pygwin', 'data')

        #  load fonts
        json = os.path.join(data_dir, 'fonts.json')
        Media.load_fonts(json)

        #  load default style
        json = os.path.join(data_dir, 'default-style.json')
        StyleClass.load(json)
