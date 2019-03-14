import json
import os
import logging
import urllib.request

# <Required Enviroment Varialbes>
# - SLACK_VERIFY_TOKEN: Bot's "Verification Token" at "Basic Information"
# - SLACK_OAUTH_ACCESS_TOKEN: Bot's "OAuth Access Token" at "Install App"
# - SLACK_BOT_USER_ACCESS_TOKEN: Bot's "Bot User OAuth Access Token" at "Install App"

SLACK_VERIFY_TOKEN = os.environ['SLACK_VERIFY_TOKEN']
SLACK_OAUTH_ACCESS_TOKEN = os.environ['SLACK_OAUTH_ACCESS_TOKEN']
SLACK_BOT_USER_ACCESS_TOKEN = os.environ['SLACK_BOT_USER_ACCESS_TOKEN']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    body = json.loads(event["body"])
    # for verification
    if "challenge" in body:
        return make_response(200, {}, {"challenge": body["challenge"]})
    # check request token
    if not is_valid_token(body):
        return make_response(400, {}, "Forbidden Request")
    # check parameters
    if not "event" in body:
        return make_response(400, {}, "Invalid Parameter(lack of 'event')")
    # check parameters in "event"
    body_event = body["event"]
    if not body_event.keys() >= {'channel', 'user'}:
        return make_response(400, {}, "Invalid Parameter(lack of 'channel' in event'")
    # reply to slack
    return reply_msg_to_slack(body_event["channel"], body_event["user"], "Hail, good citizen.")
def make_response(statusCode, headers, body):
    """
    statusCode: HTTP status code
    headers: response headers(if you don't need, pass empty dictionary)
    body: response as dictionary
    """
    res = {
        "statusCode": statusCode,
        "headers": headers,
        "body": json.dumps(body)
    }
    logger.info("Response: " + str(res))
    return res
def is_valid_token(body):
    """
    check request by token
    """
    token = body.get("token")
    if token != SLACK_VERIFY_TOKEN:
        return False
    return True
def reply_msg_to_slack(channel, reply_to, msg):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer {0}".format(os.environ["SLACK_BOT_USER_ACCESS_TOKEN"])
    }
    data = {
        "token": SLACK_BOT_USER_ACCESS_TOKEN,
        "channel": channel,
        "as_user": True,
        "text": "<@%s> %s" % (reply_to, msg),
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), method="POST", headers=headers)
    with urllib.request.urlopen(req) as res:
        body = json.load(res)
        return make_response(200, {}, body)
    return make_response(400, {}, body)