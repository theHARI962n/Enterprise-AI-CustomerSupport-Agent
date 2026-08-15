from typing import TypedDict, NotRequired
from langchain_core.documents import Document

from typing import TypedDict, NotRequired


class SupportState(TypedDict):
    ticket: str

    intent: NotRequired[str]

    knowledge: NotRequired[str]

    response: NotRequired[str]

    review: NotRequired[dict]


# class SupportState(TypedDict):
#     ticket: str

#     intent: NotRequired[str]

#     documents: NotRequired[list[Document]]

#     draft_response: NotRequired[str]

#     review_status: NotRequired[str]

#     review_feedback: NotRequired[str]

#     final_response: NotRequired[str]