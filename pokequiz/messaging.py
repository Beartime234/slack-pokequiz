import logging

from pokequiz.exceptions import FailedSlackApiCall

logger = logging.getLogger(__name__)


def check_slack_response(slack_api_response):
    if slack_api_response['ok'] is False:
        raise FailedSlackApiCall(f"{slack_api_response}")


def send_intro_message(slack_client, channel_id):
    logger.info("Sending intro message")

    quiz_start_message = f"Okay trainer, let's catch them all! :smiley:"

    intro_message_response = slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=quiz_start_message
    )

    check_slack_response(intro_message_response)

    logger.debug(f"Sending intro response: {intro_message_response}")


def send_question(slack_client, channel_id, question_attachment):
    logger.info("Sending question.")

    send_question_response = slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text="",
        attachments=[question_attachment]
    )

    logger.debug(f"Question sent response: {send_question_response}")


def send_unknown_command_response(slack_client, channel_id, user_id):
    logger.info("Unknown command so sending ephemeral message")

    unknown_command_message = f"Sorry <@{user_id}> I didn't quite get that. If you want to start a quiz say " \
                              f"something with quiz and start in it :grin: e.g. @pokequiz let's start a quiz!"

    unknown_command_response = slack_client.api_call(
        "chat.postEphemeral",
        channel=channel_id,
        text=unknown_command_message,
        user=user_id
    )

    logger.debug(f"Unknown command response: {unknown_command_response}")


def update_answered_question(slack_client, channel_id, ts, question_attachment):
    logger.debug(f"Updating previous question to show correct answer")

    update_response = slack_client.api_call(
        "chat.update",
        channel=channel_id,
        ts=ts,
        text="",
        attachments=[question_attachment]
    )

    logger.debug(f"Update previous response: {update_response}")


def ask_user_to_play_again(slack_client, channel_id, play_again_attachment):
    logger.debug(f"Asking user if they want to play again.")

    play_again_response = slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text="",
        attachments=[play_again_attachment]
    )

    logger.debug(f"Play Again Response: {play_again_response}")


def delete_play_again(slack_client, channel_id, ts):
    logger.debug(f"Deleting the play again action.")

    play_again_response = slack_client.api_call(
        "chat.delete",
        channel=channel_id,
        ts=ts
    )

    logger.debug(f"Deleting play again response: {play_again_response}")


def send_answered_question(slack_client, channel_id, user_id, correct, streak):
    # As we get there streak before the data is saved it will be behind by 1
    if correct:
        streak += 1

    if not correct:
        if streak >= 10:  # if they got it wrong but there streak was over 10 tell them how much they lost
            reply_text = f"Sorry <@{user_id}> that's incorrect! :disappointed_relieved: You lost a {streak} streak."
        else:
            reply_text = f"Sorry <@{user_id}> that's incorrect! :disappointed_relieved:"
    else:
        if streak % 100 == 0:  # If this is the users 100th correct in a row
            reply_text = f":tada: :tada: :tada: WOW <@{user_id}> that's your {streak}th correct answer in a row! " \
                         f":tada: :tada: Congratulations you truly are a Pokemon master! :tada: "
        elif streak % 10 == 0:  # If this is the users 10th, 20th correct answer in a row
            reply_text = f"Nice one <@{user_id}> that's your {streak}th correct answer in a row! :astonished:"
        else:
            reply_text = f"Nice one <@{user_id}> that's correct! :tada:"

    answer_response = slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=reply_text
    )

    logger.debug(f"Answer Response: {answer_response}")


def update_play_again(slack_client, channel_id, question_attachment, ts):
    logger.info("Sending question by updating play again.")

    send_question_response = slack_client.api_call(
        "chat.update",
        channel=channel_id,
        text="",
        attachments=[question_attachment],
        ts=ts
    )

    logger.debug(f"Question sent response: {send_question_response}")


def send_leaderboard(slack_client, channel_id, leaderboard):
    logger.info("Sending leaderboard.")

    send_leaderboard_response = slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=str(leaderboard)
    )

    logger.debug(f"Leaderboard sent. Response: {send_leaderboard_response}")


def send_oauth_response(slack_client, client_id, client_secret, auth_code):
    logger.info("Sending oauth response")

    auth_response = slack_client.api_call(
        "oauth.access",
        client_id=client_id,
        client_secret=client_secret,
        code=auth_code
    )

    logger.info(f"Successfully Sent Oauth Code. Response: {auth_response}")