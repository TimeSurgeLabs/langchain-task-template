from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")


def gen_question(topic: str) -> str:
    '''Generates and returns a list of questions'''
    q = llm.invoke(f"Write me a question for a poll about '{topic}'")
    return q.content
questions = []


