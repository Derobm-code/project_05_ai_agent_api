from cloud_rag import search_cloud_knowledge_base
from tools_cloud import (
    calculate_percentage,
    add_numbers,
    multiply_numbers,
    subtract_numbers,
    calculate_remaining_after_reduction,
    get_current_datetime,
)
from tool_models import (
    CalculatePercentageArgs,
    TwoNumbersArgs,
    SearchKnowledgeBaseArgs,
    PercentageReductionArgs,
)

TOOL_CONFIG = {
    "calculate_percentage": {
        "function": calculate_percentage,
        "arguments": CalculatePercentageArgs,
    },
    "add_numbers": {
        "function": add_numbers,
        "arguments": TwoNumbersArgs,
    },
    "multiply_numbers": {
        "function": multiply_numbers,
        "arguments": TwoNumbersArgs,
    },
    "subtract_numbers": {
        "function": subtract_numbers,
        "arguments": TwoNumbersArgs,
    },
    "calculate_remaining_after_reduction": {
        "function": calculate_remaining_after_reduction,
        "arguments": PercentageReductionArgs,
    },
    "get_current_datetime": {
        "function": get_current_datetime,
        "arguments": None,
    },
    "search_knowledge_base": {
        "function": search_cloud_knowledge_base,
        "arguments": SearchKnowledgeBaseArgs,
    },
}
