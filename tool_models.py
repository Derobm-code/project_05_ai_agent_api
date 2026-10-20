from pydantic import BaseModel, Field


class CalculatePercentageArgs(BaseModel):
    value: float = Field(description="The original numeric value")
    percentage: float = Field(description="The percentage to calculate")

    percentage: float = Field(description="The percentage to calculate", ge=0)

class TwoNumbersArgs(BaseModel):
    a: float = Field(description="The first number")
    b: float = Field(descrtiption="The second number")

class SearchKnowledgeBaseArgs(BaseModel):
    query: str = Field(
        description="The question or information to search for"
    )

class PercentageReductionArgs(BaseModel):
    value: float = Field(
        description="The original duration or quantity"
    )
    percentage: float = Field(
        description="Percentage reduction from 0 to 100",
        ge=0,
        le=100,
    )