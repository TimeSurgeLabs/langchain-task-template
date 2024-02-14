from fire import Fire

from src.gen_question import gen_question
from src.gen_answers import gen_answers
from src.rank_poll import rank_poll


def generate_question(topic: str):
    '''Generates and returns a question that might be in a poll about a given topic'''
    return gen_question(topic)


def generate_answers(question: str):
    '''Generates and returns a list of answers provided a question'''
    return gen_answers(question)


def generate_poll(topic: str):
    '''Generates a poll based on a topic'''
    question = generate_question(topic)
    answers = generate_answers(question)
    return {
        'question': question,
        'answers': answers
    }


def generate_and_rank_poll(topic: str, target_audience: str):
    '''generates a poll based on a topic and ranks how good it is in accordance with how_to_make_good_polls.md'''
    poll = generate_poll(topic)
    print('Question:', poll['question'])
    print('Answers:', poll['answers'])
    print('Ranking poll....')
    final_rank = rank_poll(poll['question'], target_audience, poll['answers'])
    print('Final rank:', final_rank)

# this is the main function that will be called by other code later


def task(topic: str):
    '''Generates a poll based on a topic'''
    return generate_poll(topic)


if __name__ == "__main__":
    Fire()
