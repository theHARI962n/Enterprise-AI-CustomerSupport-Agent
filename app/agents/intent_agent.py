from app.graph.state import SupportState
from app.prompts.intent_prompt import INTENT_PROMPT
from app.schemas.intent_schema import IntentOutput
from app.utils.llm import llm


structured_llm = llm.with_structured_output(IntentOutput)


def intent_agent(state: SupportState):

    ticket = state["ticket"]

    prompt = INTENT_PROMPT.format(ticket=ticket)

    result = structured_llm.invoke(prompt)

    return {
        "intent": result.intent
    }