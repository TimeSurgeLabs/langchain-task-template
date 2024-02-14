from src.rank_poll.rank_questions import rank_question
from src.rank_poll.rank_answers import rank_answers

# if you have a bunch of complex subtasks for your subtask,
# define the "gen_" function in the __init__.py file


def rank_poll(question: str, target_audience: str, answers: list[str]) -> float:
    '''Returns a floating point number describing how good the poll is based on the criteria specified in how_to_make_good_polls.md'''
    ranks = [rank_question(question, target_audience),
             rank_answers(question, target_audience, answers)]
    return sum(ranks) / len(ranks)
