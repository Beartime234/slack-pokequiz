import json
from pokequiz import helpers


def test_form_response():
    ret = helpers.form_response(200, {"something": "something"})
    assert ret["statusCode"] == 200

    data = json.loads(ret['body'])
    assert data == {"something": "something"}


def test_is_challenge():
    ret_true = helpers.is_challenge({"challenge": "dont_matter"})
    assert ret_true is True

    ret_false = helpers.is_challenge({"nothing": "nothing"})
    assert ret_false is False