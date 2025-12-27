"""
Utility functions for Cloud Cost Optimizer
Helper functions for formatting, validation, and UI
"""
import os
import json
import platform

def clear_screen():
    """Clear the terminal screen (works on Windows/Linux/Mac)"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_banner(title):
    """
    Print a formatted banner with title
    
    Args:
        title: Banner title text
    """
    width = 70
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)

def format_currency(amount):
    """
    Format amount as Indian Rupees with commas
    
    Args:
        amount: Numeric amount
    
    Returns:
        str: Formatted currency string
    """
    return f"₹{amount:,.2f}"

def print_menu(options):
    """
    Print a menu with numbered options
    
    Args:
        options: List of menu option strings
    """
    print("\nPlease select an option:\n")
    for idx, option in enumerate(options, 1):
        print(f"  {idx}. {option}")

def validate_json_file(filepath):
    """
    Validate that a file contains valid JSON
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Invalid JSON in {filepath}: {str(e)}")
        return False
def extract_json_from_text(text):
    """
    Extract JSON from text that might contain markdown or extra text
    Handles cases where LLM wraps JSON in ```json``` or adds explanations
    
    Args:
        text: Text that might contain JSON
    
    Returns:
        str: Extracted JSON string
    """
    if not text:
        return ""
    
    # Remove markdown code blocks
    if "```json" in text:
        # Extract between ```json and ```
        start = text.find("```json") + 7
        end = text.find("```", start)
        if end != -1:
            text = text[start:end].strip()
    elif "```" in text:
        # Extract between first ``` and second ```
        start = text.find("```") + 3
        end = text.find("```", start)
        if end != -1:
            text = text[start:end].strip()
    
    # Find JSON array boundaries [ ... ] FIRST (for billing data)
    array_start = text.find('[')
    array_end = text.rfind(']')
    
    # Find JSON object boundaries { ... }
    obj_start = text.find('{')
    obj_end = text.rfind('}')
    
    # Decide which to use based on what comes first
    if array_start != -1 and (array_start < obj_start or obj_start == -1):
        # It's an array
        if array_end != -1 and array_start < array_end:
            return text[array_start:array_end + 1].strip()
    
    # Otherwise try object
    if obj_start != -1 and obj_end != -1 and obj_start < obj_end:
        return text[obj_start:obj_end + 1].strip()
    
    # Last resort: return cleaned text
    return text.strip()

def calculate_percentage(part, whole):
    """
    Calculate percentage
    
    Args:
        part: Part value
        whole: Whole value
    
    Returns:
        float: Percentage (0-100)
    """
    if whole == 0:
        return 0
    return (part / whole) * 100

def truncate_text(text, max_length=100):
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
    
    Returns:
        str: Truncated text with ... if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

def create_data_directory():
    """Create data directory if it doesn't exist"""
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created directory: {data_dir}")
    return data_dir

def save_json_file(filepath, data):
    """
    Save data to JSON file with pretty formatting
    
    Args:
        filepath: Path to save file
        data: Data to save (dict or list)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON to {filepath}: {str(e)}")
        return False

def load_json_file(filepath):
    """
    Load data from JSON file
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        dict/list: Loaded data, or None if error
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {filepath}: {str(e)}")
        return None
    except Exception as e:
        print(f"Error loading {filepath}: {str(e)}")
        return None

def print_progress(message, success=True):
    """
    Print a progress message with icon
    
    Args:
        message: Message to print
        success: True for success (✓), False for error (✗)
    """
    icon = "✓" if success else "✗"
    print(f"  {icon} {message}")

def print_section_header(title):
    """
    Print a section header
    
    Args:
        title: Section title
    """
    print(f"\n{'='*70}")
    print(f"{title}")
    print(f"{'='*70}")

def format_number(number):
    """
    Format number with commas
    
    Args:
        number: Number to format
    
    Returns:
        str: Formatted number string
    """
    return f"{number:,.2f}"

def get_file_size(filepath):
    """
    Get file size in human-readable format
    
    Args:
        filepath: Path to file
    
    Returns:
        str: File size (e.g., "2.5 KB")
    """
    try:
        size_bytes = os.path.getsize(filepath)
        
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    except:
        return "Unknown"

def validate_environment():
    """
    Validate that required environment variables are set
    
    Returns:
        tuple: (is_valid, error_message)
    """
    required_vars = ['HUGGINGFACE_API_KEY']
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        return False, f"Missing environment variables: {', '.join(missing_vars)}"
    
    # Check if API key looks valid
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not api_key.startswith('hf_'):
        return False, "HUGGINGFACE_API_KEY should start with 'hf_'"
    
    return True, None

if __name__ == "__main__":
    # Test utilities
    print("Testing Utility Functions...")
    
    # Test JSON extraction
    test_text = """
    Here is the JSON:
    ```json
    {"name": "test", "value": 123}
    ```
    """
    
    extracted = extract_json_from_text(test_text)
    print(f"\nExtracted JSON: {extracted}")
    
    # Test currency formatting
    print(f"\nFormatted currency: {format_currency(12345.67)}")
    
    # Test percentage calculation
    print(f"\nPercentage: {calculate_percentage(25, 100):.1f}%")
    
    # Test environment validation
    is_valid, error = validate_environment()
    print(f"\nEnvironment valid: {is_valid}")
    if not is_valid:
        print(f"Error: {error}")
    
    print("\n✅ Utility tests complete!")