from pokequiz.quiz import helpers


def test_form_slack_field():
    ret = helpers.form_slack_field("Test")
    assert ret == {"value": "Test", "short": False}
    ret_short = helpers.form_slack_field("Test", True)
    assert ret_short == {"value": "Test", "short": True}


def test_form_slack_action():
    ret_default = helpers.form_slack_action("name", "text", "value")
    assert ret_default == {
        "name": "name",
        "value": "value",
        "text": "text",
        "type": "button",
        "style": "default"
    }

    ret_primary = helpers.form_slack_action("name", "text", "value", style="primary")
    assert ret_primary == {
        "name": "name",
        "value": "value",
        "text": "text",
        "type": "button",
        "style": "primary"
    }

    ret_danger = helpers.form_slack_action("name", "text", "value", style="danger")
    assert ret_danger == {
        "name": "name",
        "value": "value",
        "text": "text",
        "type": "button",
        "style": "danger"
    }


def test_form_question_action():
    ret = helpers.form_question_action(1, "value")
    assert ret == {
        "name": "1",
        "text": "1",
        "value": "value",
        "type": "button",
        "style": "default"
    }


def test_form_answered_question_field():
    ret = helpers.form_answered_question_field(":emoji:", "answer")
    assert ret == {
        "value": ":emoji: answer",
        "short": False
    }


def test_form_question_field():
    ret = helpers.form_question_field(1, "answer")
    assert ret == {
        "value": "*1:* answer",
        "short": False
    }
