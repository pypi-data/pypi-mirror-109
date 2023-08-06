# bitcomp_color.py

from typing import Dict, List, Tuple
from PIL import Image

class ColorPalette:
    DEFAULT_LIMIT = 10
    DEFAULT_FORMAT = 'hex'
    SUPPORTED_FORMATS = ('hex',)
    SIZE_OF_COLOR_SECTION_IN_DEGREES = 9
    FULL_CIRCLE = 360.0
    NUMBER_OF_SECTIONS = int(FULL_CIRCLE // SIZE_OF_COLOR_SECTION_IN_DEGREES)

    def __init__(self, image_address, limit=DEFAULT_LIMIT, output_format=DEFAULT_FORMAT):
        self.image_address = image_address
        self.limit = limit
        self.output_format = output_format
        self.output_color_list = self.get_color_palette(image_address, limit, output_format)
        
    def __str__(self):
        return f"{self.output_color_list}"
    
    @staticmethod  
    def get_image(img_address: str) -> Image:
        """Open image from given image address and return PIL.Image file.

        Parameters:
        img_address (str): Path to an image file.
        
        Returns:
        Image: A PIL.image file.
    I
        """
        return Image.open(img_address)
    
    @staticmethod
    def get_image_dimensions(image: Image) -> Tuple[str, str]:
        """Return image size.
        
        Parameters:
        image (Image): A PIL.Image file.
        
        Returns:
        Tuple[str, str]: Tuple containing width and height of an image.
        """
        width, height = image.size
        return width, height
    
    @staticmethod
    def check_format_support(given_format):
        """Check if given format is supported by the library.
    
        Parameters:
        given_format (str): Format in which color values should be returned."""
        if given_format not in ColorPalette.SUPPORTED_FORMATS:
            raise Exception(f"{given_format} format is not supported.")
    
    @staticmethod
    def calculate_mean_hsl_values(hsl_colors_list: List[Dict[str, int]]) -> None:
        """Calculate mean hue, saturation, light values for each color section.
        
        Parameters:
        hsl_colors_list (List[Dict[str, int]]): List containing hue, saturation, light values for each color section.
        """
        for color_section in hsl_colors_list:
            if color_section['count'] == 0:
                number_of_appearances = 1
            else:
                number_of_appearances = color_section['count']
                
            color_section['hue_value'] = color_section['hue_value'] / number_of_appearances
            color_section['saturation_value'] = color_section['saturation_value'] / number_of_appearances
            color_section['light_value'] = color_section['light_value'] / number_of_appearances
   
    @staticmethod        
    def get_sorted_hsl_values_list(image: Image) -> List[Dict[str, int]]:
        """Return sorted list of mean HSL values for each color section.
        
        Values are sorted in order: from the most often occuring one to the least often occuring one.
        
        Parameters:
        image (Image): A PIL.Image file.
        
        Returns:
        List[Dict[str, int]]: Sorted list of mean HSL values for each color section.
        """
        colors_list = [{'count': 0, 'hue_value': 0, 'saturation_value': 0, 'light_value': 0} for _ in range(0, ColorPalette.NUMBER_OF_SECTIONS)]
        image_width, image_height = ColorPalette.get_image_dimensions(image)
        image = image.convert('RGB')
        
        for width in range(image_width-1):
            for height in range(image_height-1):
                r, g, b = image.getpixel((width, height))
                h, s, l = ColorModelTransformator.transform_rgb_to_hsl(r, g, b)
                
                color_section = int((h // ColorPalette.SIZE_OF_COLOR_SECTION_IN_DEGREES) % ColorPalette.NUMBER_OF_SECTIONS)
                colors_list[color_section]['count'] += 1
                colors_list[color_section]['hue_value'] = colors_list[color_section]['hue_value'] + h
                colors_list[color_section]['saturation_value'] = colors_list[color_section]['saturation_value'] + s
                colors_list[color_section]['light_value'] = colors_list[color_section]['light_value'] + l    
                
        ColorPalette.calculate_mean_hsl_values(colors_list)
        
        colors_list.sort(key=lambda color_section: color_section['count'], reverse=True)
        return colors_list
    
    @staticmethod
    def get_hex_color_values_list(hsl_colors_list: List, limit: int) -> List[str]:
        """Return list of colors in hex format.
        
        Parameters:
        hsl_colors_list (List): List of HSL color values.
        limit (int): Number of colors that will be returned, from most often occuring.
        
        Returns:
        List[str]: List of colors in hex format.
        """
        return [ColorModelTransformator.transform_hsl_to_hex(color_section['hue_value'],
                                    color_section['saturation_value'],
                                    color_section['light_value'])
                                        for index, color_section in enumerate(hsl_colors_list) if index < limit]   
        
    @staticmethod
    def get_color_palette(img_address: str, limit: int = DEFAULT_LIMIT, output_format: str = DEFAULT_FORMAT) -> List[str]:
        """Return a list of most common colors (in a hex format) appearing in the given image.
        
        Currently supported formats: hex.
        
        Parameters:
        img_address (str): Path to an image file.
        limit (int): Number that defines how many colors should be returned in a list; default - 10.
        output_format (str): Defines output format; default - 'hex'.
        
        Returns:
        List[str]: List of most common colors (in a given output format).
        """
        ColorPalette.check_format_support(output_format)
        return ColorPalette.get_hex_color_values_list(ColorPalette.get_sorted_hsl_values_list(ColorPalette.get_image(img_address)), limit)
        
           
        
        
class ColorModelTransformator:
    """Contain methods used to transform values from one color model to another."""
    RGB_MAX_VALUE = 255.0
    
    @staticmethod
    def transform_rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
        """Transform RGB values to HSL values.
    
        Parameters:
        r (int): Red color value, accepts ints from 0 to 255.
        g (int): Green color value, accepts ints from 0 to 255.
        b (int): Blue color value, accepts ints from 0 to 255.
        
        Returns:
        Tuple[float, float, float]: HSL values.
        """
        
        h, s, l = 0, 0, 0
        r, g, b = r / ColorModelTransformator.RGB_MAX_VALUE, g / ColorModelTransformator.RGB_MAX_VALUE, b / ColorModelTransformator.RGB_MAX_VALUE
        cmax = max(r, g, b)
        cmin = min(r, g, b)
        cdiff = cmax - cmin
        
        # hue calculation
        if cdiff == 0:
            h = 0
        elif cmax == r:
            h = ((g - b) / cdiff) % 6
        elif cmax == g:
            h = (b - r) / cdiff + 2
        else:
            h = (r - g) / cdiff + 4
        
        # light calculation
        l = ((cmax + cmin) / 2)
            
        # saturation calculation
        if cdiff == 0:
            s = 0
        else:
            s = cdiff / (1 - abs(2 * l - 1)) 
            
        h, s, l = h * 60, s, l
            
        return h, s, l
    
    @staticmethod   
    def transform_hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
        """Transform HSL values to RGB values.
        
        Parameters:
        h (float): Hue value, accepts ints from 0 to 360
        s (float): Saturation value, accepts floats from 0 to 1
        l (float): Light value, accepts floats from 0 to 1
        
        Returns:
        Tuple[int, int, int]: RGB values.
        """
        
        r, g, b = 0, 0, 0
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = l - c / 2
        
        if h >= 0 and h < 60:
            r, g, b = c, x, 0
        elif h >= 60 and h < 120:
            r, g, b = x, c, 0
        elif h >= 120 and h < 180:
            r, g, b = 0, c, x
        elif h >= 180 and h < 240:
            r, g, b = 0, x, c
        elif h >= 240 and h < 300:
            r, g, b = x, 0, c
        elif h >= 300 and h < 360:
            r, g, b = c, 0, x
            
        r, g, b = round((r + m) * ColorModelTransformator.RGB_MAX_VALUE), round((g + m) * ColorModelTransformator.RGB_MAX_VALUE), round((b + m) * ColorModelTransformator.RGB_MAX_VALUE)
        return r, g, b

    @staticmethod
    def transform_hsl_to_hex(h: float, s: float, l: float) -> str:
        """Transform HSL values to HEX value.
        
        Parameters:
        h (float): Hue value, accepts ints from 0 to 360.
        s (float): Saturation value, accepts floats from 0 to 1.
        l (float): Light value, accepts floats from 0 to 1.
        
        Returns:
        str: Color value in HEX format.
        """
        r, g, b = ColorModelTransformator.transform_hsl_to_rgb(h, s, l)
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
    