import json
from urllib.parse import parse_qsl
import base64

from fuzzywuzzy import process


def lambda_handler(event: dict, context):
    with open("ascii.json") as infile:
        art = json.load(infile)

    resp = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
        },
    }
    if event.get("requestContext", {}).get("http", {}).get("method", "") == "OPTIONS":
        return resp

    body = event.get("body")
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")
    payload = dict(parse_qsl(body))
    art_map = {i["title"]: i for i in art}
    art_name = payload.get("text")
    output = process.extractOne(art_name, art_map.keys())[0]
    return art_map.get(output, {}).get("content")
