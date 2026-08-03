# output schema for intent classification

from pydantic import BaseModel, Field

class IntentOutput(BaseModel):
    intent: str = Field(
        description="Support ticket category"
    )