"""
Utility functions for formatting and text processing.
"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


def format_section_title(key: str) -> str:
    """
    Format section keys into readable titles.
    
    Args:
        key: The key to format
        
    Returns:
        Formatted title string
    """
    # Handle special cases
    title_mappings = {
        "notable_works": "Notable Works",
        "art_style": "Art Style",
        "time_period": "Time Period",
        "birth_date": "Birth Date",
        "death_date": "Death Date",
        "birth_place": "Birth Place",
        "architectural_style": "Architectural Style",
        "construction_period": "Construction Period",
        "cultural_significance": "Cultural Significance",
        "created_by": "Created By",
        "materials_used": "Materials Used",
        "dimensions": "Dimensions",
        "location": "Location",
        "historical_context": "Historical Context",
        "artistic_movement": "Artistic Movement",
        "influenced_by": "Influenced By",
        "influence_on": "Influence On",
        "major_works": "Major Works",
        "awards_honors": "Awards & Honors",
        "exhibition_history": "Exhibition History",
        "restoration_history": "Restoration History",
        "current_status": "Current Status",
        "visitor_information": "Visitor Information",
        "fun_facts": "Fun Facts",
        "technical_details": "Technical Details",
        "conservation_notes": "Conservation Notes",
    }

    if key in title_mappings:
        return title_mappings[key]

    # Default formatting: replace underscores with spaces and capitalize
    return key.replace("_", " ").title()


def format_date(date_input: Union[str, datetime, None]) -> str:
    """
    Format various date inputs into a readable format.
    
    Args:
        date_input: Date in various formats
        
    Returns:
        Formatted date string
    """
    if not date_input:
        return "Unknown"
    
    if isinstance(date_input, datetime):
        return date_input.strftime("%B %d, %Y")
    
    if isinstance(date_input, str):
        # Try to parse common date formats
        date_patterns = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%B %d, %Y",
            "%d %B %Y",
            "%Y"
        ]
        
        for pattern in date_patterns:
            try:
                parsed_date = datetime.strptime(date_input, pattern)
                if pattern == "%Y":  # Just year
                    return date_input
                else:
                    return parsed_date.strftime("%B %d, %Y")
            except ValueError:
                continue
        
        # If no pattern matches, return as is
        return date_input
    
    return str(date_input)


def format_list_items(items: List[str], max_items: int = 5, separator: str = " • ") -> str:
    """
    Format a list of items into a readable string.
    
    Args:
        items: List of items to format
        max_items: Maximum number of items to show
        separator: Separator between items
        
    Returns:
        Formatted string
    """
    if not items:
        return "None listed"
    
    if len(items) <= max_items:
        return separator.join(items)
    else:
        displayed_items = items[:max_items]
        remaining_count = len(items) - max_items
        return f"{separator.join(displayed_items)} (+{remaining_count} more)"


def format_dimensions(dimensions: Union[str, Dict[str, Any]]) -> str:
    """
    Format dimension information into a readable format.
    
    Args:
        dimensions: Dimension data in various formats
        
    Returns:
        Formatted dimension string
    """
    if not dimensions:
        return "Not specified"
    
    if isinstance(dimensions, dict):
        # Handle dictionary format
        parts = []
        if "height" in dimensions:
            parts.append(f"H: {dimensions['height']}")
        if "width" in dimensions:
            parts.append(f"W: {dimensions['width']}")
        if "depth" in dimensions or "length" in dimensions:
            depth_val = dimensions.get("depth") or dimensions.get("length")
            parts.append(f"D: {depth_val}")
        
        if parts:
            return " × ".join(parts)
    
    # Handle string format
    return str(dimensions)


def format_currency(amount: Union[str, int, float], currency: str = "USD") -> str:
    """
    Format currency amounts.
    
    Args:
        amount: The amount to format
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    if not amount:
        return "Not specified"
    
    try:
        if isinstance(amount, str):
            # Try to extract numeric value
            numeric_amount = float(re.sub(r'[^\d.]', '', amount))
        else:
            numeric_amount = float(amount)
        
        if currency.upper() == "USD":
            return f"${numeric_amount:,.2f}"
        else:
            return f"{numeric_amount:,.2f} {currency}"
    
    except (ValueError, TypeError):
        return str(amount)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in bytes to human readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a specified length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        suffix: Suffix to add when truncated
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)].rstrip() + suffix


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and formatting.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', text.strip())
    
    # Remove markdown-style formatting for display
    cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned)  # Bold
    cleaned = re.sub(r'\*(.*?)\*', r'\1', cleaned)      # Italic
    cleaned = re.sub(r'`(.*?)`', r'\1', cleaned)        # Code
    
    return cleaned


def format_phone_number(phone: str) -> str:
    """
    Format phone numbers into a standard format.
    
    Args:
        phone: Phone number string
        
    Returns:
        Formatted phone number
    """
    if not phone:
        return ""
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if can't format


def format_percentage(value: Union[str, int, float], decimal_places: int = 1) -> str:
    """
    Format a value as a percentage.
    
    Args:
        value: Value to format as percentage
        decimal_places: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    if value is None:
        return "N/A"
    
    try:
        numeric_value = float(value)
        return f"{numeric_value:.{decimal_places}f}%"
    except (ValueError, TypeError):
        return str(value)


def format_address(address: Union[str, Dict[str, str]]) -> str:
    """
    Format address information.
    
    Args:
        address: Address in string or dictionary format
        
    Returns:
        Formatted address string
    """
    if not address:
        return "Not specified"
    
    if isinstance(address, dict):
        # Handle dictionary format
        parts = []
        for key in ["street", "city", "state", "country", "postal_code"]:
            if key in address and address[key]:
                parts.append(address[key])
        return ", ".join(parts)
    
    return str(address)


def capitalize_words(text: str, exceptions: List[str] = None) -> str:
    """
    Capitalize words in a string, with exceptions for certain words.
    
    Args:
        text: Text to capitalize
        exceptions: List of words that should not be capitalized
        
    Returns:
        Capitalized text
    """
    if not text:
        return ""
    
    if exceptions is None:
        exceptions = ["and", "or", "but", "the", "a", "an", "in", "on", "at", "by", "for", "of", "to", "with"]
    
    words = text.split()
    capitalized_words = []
    
    for i, word in enumerate(words):
        if i == 0 or word.lower() not in exceptions:
            capitalized_words.append(word.capitalize())
        else:
            capitalized_words.append(word.lower())
    
    return " ".join(capitalized_words)


def extract_year(date_string: str) -> Optional[str]:
    """
    Extract year from a date string.
    
    Args:
        date_string: Date string to extract year from
        
    Returns:
        Extracted year or None
    """
    if not date_string:
        return None
    
    # Look for 4-digit year pattern
    year_match = re.search(r'\b(19|20)\d{2}\b', str(date_string))
    if year_match:
        return year_match.group()
    
    return None


def format_tags(tags: List[str], max_display: int = 5) -> str:
    """
    Format tags for display.
    
    Args:
        tags: List of tags
        max_display: Maximum number of tags to display
        
    Returns:
        Formatted tags string
    """
    if not tags:
        return ""
    
    displayed_tags = tags[:max_display]
    formatted_tags = [f"#{tag.replace(' ', '_').lower()}" for tag in displayed_tags]
    
    result = " ".join(formatted_tags)
    
    if len(tags) > max_display:
        result += f" +{len(tags) - max_display} more"
    
    return result