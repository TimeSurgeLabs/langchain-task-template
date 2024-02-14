import time

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

llm = ChatOpenAI(model="gpt-4-turbo-preview")

question_criteria = [
    "Does it include a call to action?",
    "Is the question clear?",
    "Is the question free of technical jargon that the target audience may find confusing?",
    "Is the question itself confusing for our target audience?"
    "Is the question concise?",
    "Is the question attempting to lead people to answer a certain way? Opinions based questions are fine and should not have points deducted.",
]


class Rank(BaseModel):
    reasoning: str = Field(description="The reasoning behind the rank")
    rank: int = Field(description="The rank of the question")


parser = PydanticOutputParser(pydantic_object=Rank)

prompt = PromptTemplate(
    template="Given a question, a target audience, and a criteria, rank a question based on how well it fits the given criteria for that target audience. State your reasoning as well as an integer value from 0 to 10 on how closely the question fits the criteria given the target audience.{format_instructions}\n\nQuestion: {question}\nTarget Audience:{target_audience}\nCriteria: {criteria}\n\n",
    input_variables=["question", "criteria", "target_audience"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

question_rater_chain = prompt | llm | parser


def rank_question(question: str, target_audience: str) -> float:
    total_score = 0
    total_criteria = len(question_criteria)
    print(
        f'Ranking question: {question} for target audience: {target_audience}')
    for criteria in question_criteria:
        rank: Rank = question_rater_chain.invoke(
            {"question": question, "criteria": criteria, "target_audience": target_audience})
        print(
            f'Criteria: {criteria} Rank: {rank.rank} Reasoning: {rank.reasoning}')
        total_score += rank.rank
        # avoid rate limiting
        # time.sleep(3)

    # if the question is greater than 140 characters, deduct a point for every 2 characters over
    char_score = 10
    if len(question) > 140:
        char_score -= (len(question) - 140) / 2
        if char_score < 0:
            char_score = 0
    total_score += char_score
    total_criteria += 1

    return total_score / total_criteria
