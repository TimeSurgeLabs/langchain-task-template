# Langchain Task Template repo

This is a template repo that is meant to be cloned/used whenever you are trying to use openai/langchain to optimize/do some task. Takes about three minutes to run.

# Best practices

First, you should define what it is you are trying to have the LLM accomplish in the form of a simple step by step guide.  
An example is in [how_to_make_good_polls.md](how_to_make_good_polls.md).  
This will be your guide for structuring the tool you are trying to make.

For each step you can try:
* Asking chatgpt outright to do it in the form of a prompt, be sure to ask for its reasoning, encourage it, and include few shot prompting/examples, 
* Iterate to make a part of it better
* Rank output and cherry pick the best option
# Installation

put your .env file in place, it should be structured like example.env

## Install Poetry

See their [official docs](https://python-poetry.org/docs/#installing-with-the-official-installer).

# Run the project

```
poetry run python main.py generate_poll --topic "programming"
poetry run python main.py generate_question --topic "programming"
poetry run python main.py generate_answers --question "which programming language is easiest to use"
poetry run python main.py rank_poll --topic "programming" --target_audience "software developers" # generates and ranks a poll
```

# Relevant links
* [OpenAI Docs](https://platform.openai.com/docs/guides/text-generation)  
* [LangChain Quickstart](https://python.langchain.com/docs/get_started/quickstart)  
