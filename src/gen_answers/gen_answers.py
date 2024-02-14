from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI


class Answers(BaseModel):
    answers: list[str] = Field(description="The answers to the poll question")


parser = PydanticOutputParser(pydantic_object=Answers)


prompt = PromptTemplate(
    template="Write me 3 to 4 answers for a poll with the following question, If the question would have more than 3 mainstream answers have the 4th answer be something like 'other 👇', feel free to add emojis to an answer if one fits: {question}\n{format_instructions}",
    input_variables=["question"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

llm = ChatOpenAI(model="gpt-3.5-turbo")


chain = prompt | llm | parser


def gen_answers(question: str) -> list[str]:
    '''Generates and returns a list of answers provided a question'''
    return chain.invoke({"question": question}).answers
