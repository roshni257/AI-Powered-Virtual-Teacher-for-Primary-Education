"""
Gujarati OCR using Tesseract
Reads Gujarati text from images using pytesseract
"""

import pytesseract
from PIL import Image
import os
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def read_gujarati_text(image_path):
    """
    Read Gujarati text from an image using OCR
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Extracted Gujarati text as string
    """
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Perform OCR with Gujarati language
        # 'guj' is the language code for Gujarati
        text = pytesseract.image_to_string(img, lang='guj')
        
        return text
    
    except FileNotFoundError:
        return f"Error: Image file '{image_path}' not found"
    except Exception as e:
        return f"Error: {str(e)}"


def read_gujarati_with_preprocessing(image_path):
    """
    Read Gujarati text with image preprocessing for better accuracy
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Extracted Gujarati text as string
    """
    try:
        from PIL import ImageEnhance, ImageFilter
        
        # Open and preprocess the image
        img = Image.open(image_path)
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        
        # Apply slight sharpening
        img = img.filter(ImageFilter.SHARPEN)
        
        # Perform OCR with Gujarati language
        text = pytesseract.image_to_string(img, lang='guj')
        
        return text
    
    except FileNotFoundError:
        return f"Error: Image file '{image_path}' not found"
    except Exception as e:
        return f"Error: {str(e)}"


def read_multiple_languages(image_path, languages=['guj', 'eng']):
    """
    Read text in multiple languages (e.g., Gujarati and English)
    
    Args:
        image_path: Path to the image file
        languages: List of language codes (default: Gujarati and English)
        
    Returns:
        Extracted text as string
    """
    try:
        img = Image.open(image_path)
        
        # Join languages with '+' for Tesseract
        lang_string = '+'.join(languages)
        
        text = pytesseract.image_to_string(img, lang=lang_string)
        
        return text
    
    except FileNotFoundError:
        return f"Error: Image file '{image_path}' not found"
    except Exception as e:
        return f"Error: {str(e)}"


# Example usage
if __name__ == "__main__":
    # Replace with your image path
    image_path = "testing-guj.png"
    
    # Basic OCR
    print("=== Basic Gujarati OCR ===")
    text = read_gujarati_text(image_path)
    print(text)
    
    print("\n" + "="*50 + "\n")
    
    # OCR with preprocessing
    print("=== With Preprocessing ===")
    text = read_gujarati_with_preprocessing(image_path)
    print(text)
    
    print("\n" + "="*50 + "\n")
    
    # Multiple languages (Gujarati + English)
    print("=== Gujarati + English ===")
    text = read_multiple_languages(image_path)
    print(text)