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
