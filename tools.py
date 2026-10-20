from datetime import datetime
from rag_tool import search_knowledge_base


def calculate_percentage(value: float, percentage: float) -> float:
    """
    Calculate a percentage of a value.

    Args:
        value: The original numeric value.
        percentage: The percentage to calculate.

    Returns:
        The calculate percentage amount.
    """

    return value * (percentage / 100)


def add_numbers(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Args:
    a: The first number.
    b: The second number.
    
    Returns:
        The sum of the two numbers.
    """
    return a + b

def multiply_numbers(a: float, b: float) -> float:
    """
    Multiply two numbers together.
    
    Args:
    a: The first number.
    b: The second number.
    
    Retruns:
        The product of the two numbers.
        
    """
    return a*b

def subtract_numbers(a: float, b: float) -> float:
    """
    Subtract the second from the first number.
    
    Args: 
        a: The number to subtract from.
        b: The number to subtract.
    
    Returns:
        The result of a minus b.
    """
    return a - b

def calculate_remaining_after_reduction(
        value: float,
        percentage: float,
) -> dict[str, float]:
    """
    Calculate the amount saved and the remaining value 
    after reducing quantity by a percentage.
    
    Args: 
        value: The original duration or quantity.
        percentage: The percentage reduction, from 0 to 100.
        
    Returns:
        The amount reduced and the remaining value.
    """
    amount_reduced = value * (percentage / 100)
    remaining_value = value - amount_reduced
    
    return {
        "amount_reduced": amount_reduced,
        "remaining_value": remaining_value,
    }

def get_current_datetime() -> str:
    """
    Get the current local date and time.
    
    Returns:
        The current local date and time.
    """
    return datetime.now().astimezone().strftime(
        "%Y-%m-%d %H:%M:%S %Z"
    )