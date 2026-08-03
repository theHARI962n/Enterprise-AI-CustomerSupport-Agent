from typing import TypedDict, NotRequired
from langchain_core.documents import Document

class SupportState(TypedDict):
    ticket: str

    intent: NotRequired[str]

    documents: NotRequired[list[Document]]

    draft_response: NotRequired[str]

    review_status: NotRequired[str]

    review_feedback: NotRequired[str]

    final_response: NotRequired[str]