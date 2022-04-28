# For HaniAPI, Script by NYT92
import requests
import secrets
import configparser

config_obj = configparser.ConfigParser()
config_obj.read("config.ini")

cmt_base = config_obj["comments_api"]
comments = cmt_base["base_cmt_url"]
reply_comments = cmt_base["reply_url"]
reply2_comments = cmt_base["reply_reply_url"]

def get_totals(id: str) -> dict:
    comments_params = comments + f"?hv_id={id}&order=upvotes,desc&offset=0&count=12"
    headers = {"X-Signature-Version": "web2","X-Signature": secrets.token_hex(32)}
    response = requests.get(comments_params, headers=headers)
    comments_res = response.json()
    return {
        'comments': comments_res["meta"]
    }

def get_comments(id: str) -> dict:
    comments_params = comments + f"?hv_id={id}&order=upvotes,desc&offset=0&count=12"
    headers = {"X-Signature-Version": "web2","X-Signature": secrets.token_hex(32)}
    response = requests.get(comments_params, headers=headers)
    return response.json()["data"]

def get_reply(id: str) -> dict:
    reply_params = reply_comments + f"?hthread_id={id}&order=upvotes,desc&offset=0&count=12"
    headers = {"X-Signature-Version": "web2","X-Signature": secrets.token_hex(32)}
    response = requests.get(reply_params, headers=headers)
    return response.json()

def get_reply_reply(id: str) -> dict: 
    reply2_params = reply2_comments + f"?hthread_comment_id={id}&order=upvotes,desc&offset=0&count=12"
    headers = {"X-Signature-Version": "web2","X-Signature": secrets.token_hex(32)}
    response = requests.get(reply2_params, headers=headers)
    return response.json()