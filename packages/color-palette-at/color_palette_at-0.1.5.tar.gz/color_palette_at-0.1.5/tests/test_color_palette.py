# test_color_palette.py

import pytest
from color_palette.color_palette import ColorPalette, ColorModelTransformator

test_image_1 = ColorPalette.get_image('./tests/temple.png')
test_image_2 = ColorPalette.get_image('./tests/icon.png')
test_image_3 = ColorPalette.get_image('./tests/sunset.png')

@pytest.mark.parametrize("image, expected_values", [
    (test_image_1, (866, 557)),
    (test_image_2, (256, 256)),
    (test_image_3, (700, 433)),
])
def test_is_image_dimensions_read_correct(image, expected_values):
    assert ColorPalette.get_image_dimensions(image) == expected_values
    
@pytest.mark.parametrize("rgb_values, expected_hsl_values", [
    ((84, 178, 59), (107.394, 0.502, 0.464)),
    ((21, 28, 148), (236.692, 0.751, 0.331)),
    ((9, 95, 35), (138.139, 0.826, 0.203)),
    ((51, 241, 181), (161.052, 0.871, 0.572)),
    ((88, 140, 114), (150.0, 0.228, 0.447)),
])
def test_is_rgb_to_hsl_transformation_correct(rgb_values, expected_hsl_values):
    assert ColorModelTransformator.transform_rgb_to_hsl(*rgb_values) == pytest.approx(expected_hsl_values, abs=1e-2)
    
@pytest.mark.parametrize("hsl_values, expected_rgb_values", [
    ((179.447, 0.931, 0.543), (30, 247, 245)),
    ((32.903, 0.931, 0.543), (247, 149, 30)),
    ((333.529, 0.552, 0.517), (200, 64, 124)),
    ((144.963, 0.724, 0.370), (26, 163, 83)),
    ((160.5, 0.892, 0.439), (12, 212, 147)),
])
def test_is_hsl_to_rgb_transformation_correct(hsl_values, expected_rgb_values):
    assert ColorModelTransformator.transform_hsl_to_rgb(*hsl_values) == expected_rgb_values
    
@pytest.mark.parametrize("hsl_values, expected_hex_values", [
    ((28.0, 0.762, 0.115), '#341c07'),
    ((91.327, 0.738, 0.3), '#4a8514'),
    ((25.714, 0.147, 0.464), '#887465'),
    ((174.333, 0.857, 0.588), '#3cf0df'),
    ((15.483, 0.373, 0.837), '#e5cec6'),
])
def test_is_hsl_to_hex_transformation_correct(hsl_values, expected_hex_values):
    assert ColorModelTransformator.transform_hsl_to_hex(*hsl_values) == expected_hex_values
      
@pytest.mark.parametrize("image, expected_first_color_count, expected_second_color_saturation, expected_fourth_color_hue", [
    (test_image_1, 147454, 0.3711, 211.0331),
    (test_image_2, 51047, 0.0968, 34.6772),
    (test_image_3, 53404, 0.8534, 23.1361),
])  
def test_is_color_values_hsl_list_correct(image, expected_first_color_count, expected_second_color_saturation, expected_fourth_color_hue):
    colors_list = ColorPalette.get_sorted_hsl_values_list(image)
    assert colors_list[0]['count'] == expected_first_color_count
    assert colors_list[1]['saturation_value'] == pytest.approx(expected_second_color_saturation, 1e-3)
    assert colors_list[3]['hue_value'] == pytest.approx(expected_fourth_color_hue, 1e-3)
    
@pytest.mark.parametrize("image, expected_hex_colors_list, limit", [
    (test_image_1, ['#195467', '#3c6b84', '#093135', '#426c99', '#405e9b', '#0e2f2d', '#14312b', '#a92732', '#19342a', '#1d3629'], 10),
    (test_image_2, ['#0a0a0a', '#464d56', '#d3d3d1', '#e0c6a2', '#575c67', '#847e74', '#595975', '#7f9595'], 8),
    (test_image_3, ['#76221c', '#ba660f', '#852c11', '#b65010', '#46262d'], 5),
])  
def test_is_color_values_hex_list_correct(image, expected_hex_colors_list, limit):
    colors_list = ColorPalette.get_sorted_hsl_values_list(image)
    colors_hex_list = ColorPalette.get_hex_color_values_list(colors_list, limit)
    assert colors_hex_list == expected_hex_colors_list
