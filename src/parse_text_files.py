import numpy as np
from collections import Counter
import re

##############################################################################
##############################################################################

def create_skills_list(data : dict, 
                       start_keyword : str, 
                       end_keyword : str) -> list:
    """
    Extracts a list of skills from a dictionary containing text, 
    using specified start and end keywords to locate the skills section.

    The function searches for the start and end keywords within the text 
    to determine the section where skills are listed. It then iterates through 
    this section to compile a list of skills, filtering out any known 'bugged' texts 
    and ensuring only valid words are included. The skills are cleaned, joined, 
    and transformed to lowercase to form a finalized list of skills.

    Args:
        data (dict): A dictionary where the text containing potential skills is 
                     located under the key 'text', which maps to a list of strings.
        start_keyword (str): A string that marks the beginning of the skills section 
                             in the text.
        end_keyword (str): A string that signifies the end of the skills section 
                           in the text.

    Returns:
        list: A list of strings, where each string is a skill extracted from the text. 
              The skills are in lowercase and extraneous whitespace is removed.
    """
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

def calculate_bar_length_and_ratio(pixels: np.ndarray, 
                                   bar_value: int, 
                                   tolerance: int = 10) -> tuple:
    """
    Calculates the length of a graphical bar in an image and the ratio of pixels matching the bar's intensity.

    This function analyzes a one-dimensional array of grayscale pixel intensities representing a bar in an image.
    It identifies the length of the bar based on the presence of pixel intensities within a specified range centered
    on a given bar intensity value. The function also computes the ratio of the number of pixels with the bar's intensity
    to the total length of the bar. This can be useful for analyzing the intensity profile of image elements.

    Args:
        pixels (np.ndarray): A 1D numpy array of pixel values in grayscale (0-255) representing the intensity profile along a bar.
        bar_value (int): The intensity value of the bar which is the target for the count. This value is typically
                         the most common pixel intensity within the bar region, excluding pure white (255).
        tolerance (int, optional): A tolerance range around the bar_value to account for variations due to anti-aliasing, shadows, 
                                   or gradients. For example, with a bar_value of 165 and a tolerance of 10, pixels with intensities 
                                   from 155 to 175 will be counted as part of the bar. Defaults to 10.

    Returns:
        tuple: A tuple containing three elements:
               - The length of the bar in pixels.
               - The count of pixels within the tolerance range of the bar's intensity value.
               - The ratio of pixels matching the bar's intensity to the total bar length.
    """
    bar_start = -1  # Initialize the start of the bar to an invalid index
    bar_end = -1  # Initialize the end of the bar to an invalid index
    bar_value_count = 0  # Initialize the count of pixels with the bar's intensity

    # Iterate over the pixel values to find the bar length and count of bar_value pixels
    for i, pixel in enumerate(pixels):
        # Check if the current pixel falls within the bar's intensity range
        if bar_start == -1 and (bar_value - tolerance) <= pixel <= (bar_value + tolerance):
            bar_start = i  # Mark the start of the bar

        # Check if we've found the end of the bar based on a white gap
        if bar_start != -1 and pixel == 255:
            # If the next pixel is also white, consider it the end of the bar
            if i + 1 < len(pixels) and pixels[i + 1] == 255:
                bar_end = i
                break

        # Count the pixels that fall within the bar's intensity range
        if (bar_value - tolerance) <= pixel <= (bar_value + tolerance):
            bar_value_count += 1

    # If the bar end wasn't found in the loop, set it to the last pixel (if the bar has started)
    if bar_end == -1 and bar_start != -1:
        bar_end = len(pixels) - 1

    # Calculate the bar length; if the bar hasn't started, bar_length is 0
    bar_length = bar_end - bar_start if bar_start != -1 else 0
    # Calculate the ratio of pixels with the bar's intensity to the total bar length
    ratio = bar_value_count / bar_length if bar_length > 0 else 0

    return bar_length, bar_value_count, ratio
