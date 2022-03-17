# For HanimeAPI, Script by NYT92

import requests
import secrets

comments = "https://hanime.tv/api/v8/hthreads"
reply_comments = "https://hanime.tv/api/v8/hthread_comments"
reply2_comments = "https://hanime.tv/api/v8/hthread_comment_comments"
user = "https://hanime.tv/rapi/v8/user"

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
