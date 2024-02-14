import re
import time

import httpx
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE)


def contains_emoji(s: str) -> bool:
    return bool(emoji_pattern.search(s))


llm = ChatOpenAI(model="gpt-4-turbo-preview")

answer_criteria = [
    "Is the answer free of technical jargon that the target audience may find confusing?",
    "Is the answer confusing for our target audience?",
    "Is the answer clear?",
    "Is the answer concise?",
]


class Rank(BaseModel):
    reasoning: str = Field(description="The reasoning behind the rank")
    rank: int = Field(description="The rank of the question")


parser = PydanticOutputParser(pydantic_object=Rank)

prompt = PromptTemplate(
    template="Given an answer, a target audience, and a criteria, rank an answer based on how well it fits the given criteria. State your reasoning as well as an integer value from 0 to 10 on how closely the answer fits the criteria, with 0 being not at all and 10 being very well. State your reasoning as well.{format_instructions}\n\nAnswer: {answer}\nTarget Audience: {target_audience}\nCriteria: {criteria}\n\n",
    input_variables=["answer", "criteria", "target_audience"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

answer_rater_chain = prompt | llm | parser

question_related_prompt = PromptTemplate(
    template="Given a question and an answer, rank on a scale of 0 to 10 how well the answer fits the question, with 0 being not at all and 10 being very well. State your reasoning as well.{format_instructions}\n\nQuestion: {question}\nAnswer: {answer}\n\n",
    input_variables=["question", "answer"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# every component in a chain can be used in other chains
question_related_rater_chain = question_related_prompt | llm | parser


def rank_answer(answer: str, question: str, target_audience: str) -> float:
    total_score = 0
    total_criteria = len(answer_criteria)
    print(f'Ranking answer: {answer} for target audience: {target_audience}')
    for criteria in answer_criteria:
        rank: Rank = answer_rater_chain.invoke(
            {"answer": answer, "criteria": criteria, "target_audience": target_audience})
        print(
            f'Ranking criteria: {criteria} with rank: {rank.rank} with reasoning {rank.reasoning}')
        total_score += rank.rank
        # time.sleep(3)
    # if they contain emojis, add 10 to the score
    if contains_emoji(answer):
        total_score += 10
        # need to add 1 to the total criteria because we are adding 10 to the score
        total_criteria += 1

    total_score += question_related_rater_chain.invoke(
        {"question": question, "answer": answer}).rank
    total_criteria += 1

    # answers should be less than 30 characters. We will deduct 1 point for every character over 30
    char_score = 10
    if len(answer) > 30:
        char_score -= (len(answer) - 30)
        if char_score < 0:
            char_score = 0

    total_score += char_score
    total_criteria += 1

    return total_score / total_criteria


def rank_answers(question: str, target_audience: str, answers: list[str]) -> float:
    '''Ranks answers based on criteria'''
    scores = [rank_answer(answer, question, target_audience)
              for answer in answers]
    score = 0
    if len(answers) == 3 or len(answers) == 4:
        score += 10
    # calculate the average of the scores
    return (sum(scores) + score) / (len(scores) + 1)
