# cli_color_palette.py

import argparse
import os
import sys
from color_palette import ColorPalette

# ColorPalette('path/to/an/image.jpg', 5, 'hex')

class ColorCLI:

    @staticmethod
    def print_color_palette(file_name: str, limit: int, output_format: str):
        ColorPalette(file_name, limit, output_format)

    @staticmethod
    def get_color_palette():
        parser = argparse.ArgumentParser(description="CLI that utilize color_palette_at library.")
        parser.add_argument('file_name', type=str, help="Path to the file image.")
        parser.add_argument('limit', type=int, nargs='?', default=10, help="Number of colors that will be returned, default value: 10.")
        parser.add_argument('output_format', type=str, nargs='?', default='hex', help="Format in which output colors will be returned, default value: hex.")
        
        arguments = parser.parse_args()
        arguments.output_format = arguments.output_format.lower()
        
        if not os.path.isfile(arguments.file_name):
            print(f"File called {arguments.file_name} does not exist.")
            sys.exit(1)
            
        if arguments.output_format not in ColorPalette.SUPPORTED_FORMATS:
            print(f"The {arguments.output_format} format is not supported.")
            print("Currently supported formats:")
            for format in ColorPalette.SUPPORTED_FORMATS:
                print(f"{format}", end=", ")
            sys.exit(1)
            
        ColorCLI.print_color_palette(arguments.file_name, arguments.limit, arguments.output_format)
            

            