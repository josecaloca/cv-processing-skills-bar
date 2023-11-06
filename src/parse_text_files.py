import numpy as np
from collections import Counter
import re

##############################################################################
##############################################################################

def create_skills_list(data, start_keyword, end_keyword):
    # Initialize an empty list to hold skills
    skills_list = []

    bugged_texts = ['ae','eemeeeneeneenenmnen','er']
    
    # Find the indexes for 'SKILLS' and 'CERTIFICATES'
    start_index = data['text'].index(start_keyword) if start_keyword in data['text'] else None
    end_index = data['text'].index(end_keyword) if end_keyword in data['text'] else None

    # Check if both keywords were found
    if start_index is not None and end_index is not None and start_index < end_index:
        # Extract potential skills
        for i in range(start_index + 1, end_index):
            text = data['text'][i].strip()
            # Use regular expression to filter out valid words and remove unwanted characters
            valid_texts = re.findall(r'\b[a-zA-Z]{2,}\b', text)
            # Join consecutive words to form skills
            if valid_texts and valid_texts[0] not in bugged_texts:
                # If the previous item in skills_list is not empty, append the current valid text to it
                if skills_list and skills_list[-1]:
                    skills_list[-1] += ' ' + ' '.join(valid_texts)
                else:
                    skills_list.append(' '.join(valid_texts))
            elif skills_list and skills_list[-1]:  # If there is an empty string but the last skill is not empty
                skills_list.append('')  # Append an empty string to indicate potential separation between skills

    # Remove any empty strings at the end of joined words and convert to lowercase
    skills_list = [skill.lower().strip() for skill in skills_list if skill.strip()]

    return skills_list

##############################################################################
##############################################################################

def calculate_bar_length_and_ratio(pixels : np.ndarray, 
                                   bar_value : int, 
                                   tolerance : int = 10) -> tuple:
    """_summary_

    Args:
        pixels (numpy.ndarray): List of pixel values in gray scale (0-255) where the bar is present
        bar_value (_type_): Light intensity of the bar. This is defined as the most common pixel value in pixels array which is not equal to 255 (white)
        tolerance (int, optional): Number of colour intensity values around the bar value due to anti-aliasing, shadows, or gradients. 
        If the bar value is 165 and tolerance is set at 10, then all pixels with light 10 values above and below the bar value will be considered. Defaults to 10.

    Returns:
        tuple: lenght of the bar, how many pixels are of the bar_value, and the ratio of bar_value pixels to the bar length.
    """
    bar_start = -1
    bar_end = -1
    bar_value_count = 0

    # Iterate over the pixel values to find the bar length and count of bar_value pixels
    for i, pixel in enumerate(pixels):
        if bar_start == -1 and (bar_value - tolerance) <= pixel <= (bar_value + tolerance):
            bar_start = i  # Start of the bar (shadow or gradient included)
        
        if bar_start != -1 and pixel == 255:
            # Check if we've encountered a significant gap of white pixels to mark the end of the bar
            if i + 1 < len(pixels) and pixels[i + 1] == 255:
                bar_end = i
                break

        if (bar_value - tolerance) <= pixel <= (bar_value + tolerance):
            bar_value_count += 1

    # If the bar doesn't end in the given pixel array, we set the end to the last pixel
    if bar_end == -1 and bar_start != -1:
        bar_end = len(pixels) - 1

    # Calculate the bar length and the ratio
    bar_length = bar_end - bar_start if bar_start != -1 else 0
    ratio = bar_value_count / bar_length if bar_length > 0 else 0

    return bar_length, bar_value_count, ratio
