"""Helpers for the pokequiz
"""


def form_slack_field(value, short=False) -> dict:
    """Forms a slack field

    Args:
        value: The value of the field
        short: Whether or not

    Returns:

    """
    return {"value": value, "short": short}


def form_slack_action(name: str, text: str, value: str, action_type="button", style="default") -> dict:
    """Forms a slack action.

    Args:
        name: Name of the action
        text: Text of the action
        value: Value of the action
        action_type: action type e.g. button [Default: button]
        style: style of the action [Default: default]
    """
    return {"name": name, "text": text, "type": action_type, "value": value, "style": style}


def form_question_action(question_number: int, question_value: str) -> dict:
    """

    Args:
        question_value: The questions value
        question_number: The question number

    Returns:
        dict: A dictionary of the slack question
    """
    question_number = str(question_number)
    return form_slack_action(question_number, question_number, question_value)


def form_answered_question_field(emoji: str, answer: str) -> dict:
    """Forms a question field for a slack attachment

    Args:
        emoji: The emoji
        answer: The answer to the question

    Returns:
        dict: A dictionary of slack question field
    """
    return form_slack_field(f"{emoji} {answer}")


def form_question_field(question_number: int, answer: str) -> dict:
    """Forms a question field for a slack attachment

    Args:
        question_number: The question number
        answer: The answer to the question

    Returns:
        dict: A dictionary of slack question field
    """
    return form_slack_field(f"*{question_number}:* {answer}")
