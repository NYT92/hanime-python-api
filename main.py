# Flask API Made by NYT92

# Credit to WeaveAche and Profility for the code
# https://github.com/WeaveAche/hanime-auto-coins-collector

# api url : https://hani.nsdev.ml
# docs : https://aslnk.ml/zwi3ag

# PLEASE DONT ABUSE IT JUST PLEASE JUST FUCKING DONT ABUSing IT...........
# Im not good at this shit so dont call me copy&paste guy 
# also i want to port this to nodejs but the process is kinda hard so i will do it later

import base64
import requests
import json
import time
import cmt_hanime
import secrets
import configparser
import logging
from hashlib import sha256
from dateutil import parser
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from waitress import serve

# Server Config
app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
limiter = Limiter(app, key_func=get_remote_address)
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.DEBUG,
                    format=f'%(asctime)s : %(message)s')
logger.info('API IS RUNNING')
logger.info('--------------------------------')
logger.info('Never Use This API for Production If you deploying on the slow server')
logger.info('--------------------------------')
logger.info('Go to https://haniapi-docs.vercel.app/docs/config for more information')
logger.info('--------------------------------')

# Config
config_obj = configparser.ConfigParser()
config_obj.read("config.ini")

# Main
main_base = config_obj["main"]
base_url = main_base["base_url"]
video_url = main_base["video_url"]
video_api_url = main_base["video_api_url"]
search_api = main_base["search_api"]

# APIs
api_base = config_obj["api"]
api_url = api_base["api_url"]
landing = api_base["landing"]
browse = api_base["browse"]
community = api_base["community"]
channels = api_base["channel"]
mychannel = api_base["mychannel"]
browse_trends = api_base["browse-trends"]

# Server Config
server_base = config_obj["serv_config"]
req = server_base["req"]
search_req = server_base["search_req"]

# Index / Error Handler


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(405)
def resource_not_found(e):
    return jsonify(error=str(e)), 405

@app.errorhandler(500)
def server_error(e):
    return jsonify(error=str(e)), 500

@app.errorhandler(503)
def server_unavailable(e):
    return jsonify({
        "error": "Service unavailable",
        "message": str(e)
    }), 503

@app.route('/')
def index():
    return jsonify({
            'status': 'ok',
            'Warning': 'Never use this API in production and abusing there system, this is just for testing purposes and for fun only',
            'Credit': 'Made by NYT92',
            'Github': 'https://github.com/nyt92',
            'Version': '4.0',
            'Docs': 'https://haniapi-docs.vercel.app',
            'API': {
                'Info': 'Prod-URL1 will be use for main public api and will be available in V4. Deprecated-URL will be deprecated in V4',
                'Deprecated':'https://v3hani.nsdev.ml',
                'Prod-URL1':'https://hani.nsdev.ml',
                'Prod-URL2':'https://v4hani.nsdev.ml',
            }
        }), 200

# Authentication


@app.route("/login", methods=["GET"])
def login():
    return jsonify({"Read This": "https://haniapi-docs.vercel.app/docs/authentication#update", "200": "OK"}), 200


@app.route("/auth", methods=["GET"])
def auth():
    return jsonify({"Read This": "https://haniapi-docs.vercel.app/docs/authentication#update", "200": "OK"}), 200


@app.route("/auth/login", methods=["GET"])
@limiter.limit(req)
def authlogin():
    hanime_email = request.args.get("email")
    hanime_password = request.args.get("password")

    def getXHeaders():
        XClaim = str(int(time.time()))
        headers = {"X-Signature-Version": "web2",
                   "X-Time": XClaim, "X-Signature": secrets.token_hex(32)}
        return headers

    def login(s: requests.Session, email, password):
        s.headers.update(getXHeaders())
        response = s.post(f"{base_url}/rapi/v4/sessions", headers={
                          "Content-Type": "application/json;charset=utf-8"}, 
                          data=f'{{"burger":"{email}","fries":"{password}"}}')
        return getInfo(response.text)

    def getInfo(response):
        received = json.loads(response)
        return received

    def main():
        s = requests.Session()
        info = login(s, hanime_email, hanime_password)
        s.headers.update({"X-Session-Token": info["session_token"]})
        return info
    try:
        info = main()
        return jsonify(info), 200
    except:
        return jsonify({"error": "Unauthorized. Invalid Email or Password"}), 401

@app.route("/auth/login/getsession", methods=["GET"])
@limiter.limit(req)
def authgetsession():
    hanime_email = request.args.get("email")
    hanime_password = request.args.get("password")

    def getSHA256(to_hash):
        m = sha256()
        m.update(to_hash.encode())
        return m.hexdigest()

    def getXHeaders():
        XClaim = str(int(time.time()))
        XSig = getSHA256(f"9944822{XClaim}8{XClaim}113")
        headers = {"X-Signature-Version": "web2",
                   "X-Time": XClaim, "X-Signature": XSig}
        return headers

    def login(s: requests.Session, email, password):
        s.headers.update(getXHeaders())
        response = s.post(f"{base_url}/rapi/v4/sessions", headers={
                          "Content-Type": "application/json;charset=utf-8"}, data=f'{{"burger":"{email}","fries":"{password}"}}')
        return getInfo(response.text)

    def getInfo(response):
        received = json.loads(response)
        ret = {
            "Warning": "Please store this session token somewhere safe.",
            "Info": "1 Session token only vaild for 30 days. If you want to use it again, you need to request again.",
        }
        ret["session_token"] = received["session_token"]
        return ret

    def main():
        s = requests.Session()
        info = login(s, hanime_email, hanime_password)
        s.headers.update({"X-Session-Token": info["session_token"]})
        return info
    try:
        info = main()
        return jsonify(info), 200
    except:
        return jsonify({"error": "Unauthorized. Invalid Email or Password"}), 401


@app.route("/auth/login/summary", methods=["GET"])
@limiter.limit(req)
def authsummary():
    hanime_email = request.args.get("email")
    hanime_password = request.args.get("password")

    def getSHA256(to_hash):
        m = sha256()
        m.update(to_hash.encode())
        return m.hexdigest()

    def getXHeaders():
        XClaim = str(int(time.time()))
        XSig = getSHA256(f"9944822{XClaim}8{XClaim}113")
        headers = {"X-Signature-Version": "web2",
                   "X-Time": XClaim, "X-Signature": XSig}
        return headers

    def login(s: requests.Session, email, password):
        s.headers.update(getXHeaders())
        response = s.post(f"{base_url}/rapi/v4/sessions", headers={
                          "Content-Type": "application/json;charset=utf-8"}, data=f'{{"burger":"{email}","fries":"{password}"}}')
        return getInfo(response.text)

    def getInfo(response):
        received = json.loads(response)
        ret = {}
        ret["session_token"] = received["session_token"]
        ret["name"] = received["user"]["name"]
        ret["coins"] = received["user"]["coins"]
        ret["premium"] = received["user"]["alt_premium_status"]
        ret["email"] = received["user"]["email"]
        ret["avatar"] = received["user"]["avatar_url"]
        ret["id"] = received["user"]["id"]
        ret["slug"] = received["user"]["slug"]
        ret["video_view"] = received["user"]["video_views"]
        return ret

    def main():
        s = requests.Session()
        info = login(s, hanime_email, hanime_password)
        s.headers.update({"X-Session-Token": info["session_token"]})
        sum = ({
            "id": info["id"],
            "name": info["name"],
            "coin": info["coins"],
            "premium_status": info["premium"],
            "email": info["email"],
            "avatar": info["avatar"],
            "slug": info["slug"],
            "total_video_views": info["video_view"]
        })
        return sum
    try:
        info = main()
        return jsonify(info), 200
    except:
        return jsonify({"error": "Unauthorized. Invalid Email or Password"}), 401

@app.route("/auth/login/coins", methods=["GET"])
@limiter.limit(req)
def authcoins():
    hanime_email = request.args.get("email")
    hanime_password = request.args.get("password")

    def getSHA256(to_hash):
        m = sha256()
        m.update(to_hash.encode())
        return m.hexdigest()

    def getXHeaders():
        XClaim = str(int(time.time()))
        XSig = getSHA256(f"9944822{XClaim}8{XClaim}113")
        headers = {"X-Signature-Version": "app2","X-Claim": XClaim, "X-Signature": XSig}
        return headers

    def login(s: requests.Session, email, password):
        s.headers.update(getXHeaders())
        response = s.post(f"{base_url}/rapi/v4/sessions", headers={"Content-Type": "application/json;charset=utf-8"}, data=f'{{"burger":"{email}","fries":"{password}"}}')
        if '{"errors":["Unauthorized"]}' in response.text:
            print("[!!!] Login failed, please check your credentials.")
        else:
            return getInfo(response.text)

    def getInfo(response):
        received = json.loads(response)
        ret = {}
        ret["session_token"] = received["session_token"]
        ret["uid"] = received["user"]["id"]
        ret["name"] = received["user"]["name"]
        ret["coins"] = received["user"]["coins"]
        ret["last_clicked"] = received["user"]["last_rewarded_ad_clicked_at"]

        available_keys = list(received["env"]["mobile_apps"].keys())

        if "_build_number" in available_keys:
            ret["version"] = received["env"]["mobile_apps"]["_build_number"]
        elif "osts_build_number" in available_keys:
            ret["version"] = received["env"]["mobile_apps"]["osts_build_number"]
        elif "severilous_build_number" in available_keys:
            ret["version"] = received["env"]["mobile_apps"]["severilous_build_number"]
        else:
            print(
                "[!!!] Unable to find the build number for the latest mobile app, please report an issue on github.")
        return ret

    def getCoins(s: requests.Session, version, uid):
        s.headers.update(getXHeaders())
        curr_time = str(int(time.time()))
        to_hash = f"coins{version}|{uid}|{curr_time}|coins{version}"
        data = {"reward_token": getSHA256(
            to_hash)+f"|{curr_time}", "version": f"{version}"}
        response = s.post(f"{base_url}/rapi/v4/coins", data=data)
        ret = json.loads(response.text)
        return jsonify({
            "rewarded_amount": ret["rewarded_amount"],
            "message": "You have successfully collected your coins"
        })

    def main():
        s = requests.Session()
        info = login(s, hanime_email, hanime_password)
        s.headers.update({"X-Session-Token": info["session_token"]})
        if time.time() - parser.parse(info["last_clicked"]).timestamp() < 3*3600:
            return jsonify({"error": "You have already clicked on an ad less than 3 hrs ago.", "message": "You have already clicked on an ad and recieve coins. Please wait for another 3 hours",  "total_coins": info["coins"]})
        return getCoins(s, info["version"], info["uid"])

    try:
        info = main()
        return jsonify(info), 200
    except:
        return jsonify({"error": "Unauthorized. Invalid Email or Password"}), 401


@app.route("/auth/login/body", methods=["POST"])
@limiter.limit(req)
def authbody():
    request_data = request.get_json(force=True)
    hanime_email = request_data['email']
    hanime_password = request_data['password']

    def getSHA256(to_hash):
        m = sha256()
        m.update(to_hash.encode())
        return m.hexdigest()

    def getXHeaders():
        XClaim = str(int(time.time()))
        XSig = getSHA256(f"9944822{XClaim}8{XClaim}113")
        headers = {"X-Signature-Version": "web2",
                   "X-Time": XClaim, "X-Signature": XSig}
        return headers

    def login(s: requests.Session, email, password):
        s.headers.update(getXHeaders())
        response = s.post(f"{base_url}/rapi/v4/sessions", headers={
                          "Content-Type": "application/json;charset=utf-8"}, data=f'{{"burger":"{email}","fries":"{password}"}}')
        return getInfo(response.text)

    def getInfo(response):
        received = json.loads(response)
        return received

    def main():
        s = requests.Session()
        info = login(s, hanime_email, hanime_password)
        s.headers.update({"X-Session-Token": info["session_token"]})
        return info
    try:
        info = main()
        return jsonify(info), 200
    except:
        return jsonify({"error": "Unauthorized", "status": "401"}), 401


@app.route("/auth/coin/body", methods=["POST"])
@limiter.limit(req)
def authcoinbody():
    request_data = request.get_json(force=True)
    hanime_email = request_data['email']
    hanime_password = request_data['password']

    def getSHA256(to_hash):
        m = sha256()
        m.update(to_hash.encode())
        return m.hexdigest()

    def getXHeaders():
        XClaim = str(int(time.time()))
        XSig = getSHA256(f"9944822{XClaim}8{XClaim}113")
        headers = {"X-Signature-Version": "app2",
                   "X-Claim": XClaim, "X-Signature": XSig}
        return headers

    def login(s: requests.Session, email, password):
        s.headers.update(getXHeaders())
        response = s.post(f"{base_url}/rapi/v4/sessions", headers={
                          "Content-Type": "application/json;charset=utf-8"}, data=f'{{"burger":"{email}","fries":"{password}"}}')

        if '{"errors":["Unauthorized"]}' in response.text:
            print("[!!!] Login failed, please check your credentials.")
        else:
            return getInfo(response.text)

    def getInfo(response):
        received = json.loads(response)
        ret = {}
        ret["session_token"] = received["session_token"]
        ret["uid"] = received["user"]["id"]
        ret["name"] = received["user"]["name"]
        ret["coins"] = received["user"]["coins"]
        ret["last_clicked"] = received["user"]["last_rewarded_ad_clicked_at"]

        available_keys = list(received["env"]["mobile_apps"].keys())

        if "_build_number" in available_keys:
            ret["version"] = received["env"]["mobile_apps"]["_build_number"]
        elif "osts_build_number" in available_keys:
            ret["version"] = received["env"]["mobile_apps"]["osts_build_number"]
        elif "severilous_build_number" in available_keys:
            ret["version"] = received["env"]["mobile_apps"]["severilous_build_number"]
        else:
            print(
                "[!!!] Unable to find the build number for the latest mobile app, please report an issue on github.")
        return ret

    def getCoins(s: requests.Session, version, uid):
        s.headers.update(getXHeaders())
        curr_time = str(int(time.time()))
        to_hash = f"coins{version}|{uid}|{curr_time}|coins{version}"
        data = {"reward_token": getSHA256(
            to_hash)+f"|{curr_time}", "version": f"{version}"}
        response = s.post(f"{base_url}/rapi/v4/coins", data=data)
        ret = json.loads(response.text)
        return jsonify({
            "rewarded_amount": ret["rewarded_amount"],
            "message": "You have successfully collected your coins"
        })

    def main():
        s = requests.Session()
        info = login(s, hanime_email, hanime_password)
        s.headers.update({"X-Session-Token": info["session_token"]})
        if time.time() - parser.parse(info["last_clicked"]).timestamp() < 3*3600:
            return jsonify({"error": "You have already clicked on an ad less than 3 hrs ago.", "message": "You have already clicked on an ad and recieve coins. Please wait for another 3 hours",  "total_coins": info["coins"]})
        return getCoins(s, info["version"], info["uid"])
    try:
        info = main()
        return info, 200
    except:
        return jsonify({"error": "Unauthorized", "status": "401"}), 401

# API

@app.route('/getInfo', methods=["GET"])
@limiter.limit(req)
def info():
    id = request.args.get('id')
    result = requests.get(video_api_url + '/?id=' + id)
    if result.status_code == 404:
        return jsonify({"error": "No Hanime Video Id or Slug Provided", "status": "404"}), 404
    result = result.json()
    res_crdt = result["hentai_video"]["created_at"] = parser.parse(
        result["hentai_video"]["created_at"]).strftime("%Y %m %d")
    res_redt = result["hentai_video"]["released_at"] = parser.parse(
        result["hentai_video"]["released_at"]).strftime("%Y %m %d")
    res_view = result["hentai_video"]["views"] = "{:,}".format(
        result["hentai_video"]["views"])
    res_tags = result["hentai_video"]["hentai_tags"]
    res_dl = "https://hanime.tv/downloads/" + \
        base64.b64encode(result["hentai_video"]["slug"].encode()).decode()
    return jsonify(
        {
            "slug": result["hentai_video"]["slug"],
            "id": result["hentai_video"]["id"],
            "title": result["hentai_video"]["name"],
            "views": res_view,
            "info": {
                "brand": result["hentai_video"]["brand"],
                "uploaded_date": res_crdt,
                "released_date": res_redt,
                "censored": result["hentai_video"]["is_censored"],
            },
            "description": result["hentai_video"]["description"],
            "tags": [x["text"] for x in res_tags],
            "poster": result["hentai_video"]["cover_url"],
            "video": video_url + "/" + id,
            "downloadURL": res_dl,
        }
    ), 200

@app.route('/getVideo', methods=["GET"])
@limiter.limit(req)
def getVideo():
    url = video_api_url + "?id=" + request.args.get('id')
    result = requests.get(url, headers={
        "X-Session-Token": request.headers.get('Token'),
    })
    if result.status_code == 404:
        return jsonify({"error": "No Hanime Video Id or Slug Provided", "status": "404"}), 404
    result = result.json()
    dl = "https://hanime.tv/downloads/" + \
        base64.b64encode(result["hentai_video"]["slug"].encode()).decode()
    ret = {
        "url": video_url + "/" + request.args.get('id'),
        "download_url": dl,
        "streams": result["videos_manifest"]["servers"][0]["streams"]
    }
    return jsonify(ret), 200

@app.route('/getVideo/player', methods=["GET"])
@limiter.limit(req)
def vidplayerstrm():
    id = request.args.get('id')
    url = video_api_url + "?id=" + id
    result = requests.get(url)
    if result.status_code == 404:
        return jsonify({"error": "No Hanime Video Id or Slug Provided", "status": "404"}), 404
    result = result.json()
    try:
        str1 = result["videos_manifest"]["servers"][0]["streams"][1]["url"]
        resol1 = result["videos_manifest"]["servers"][0]["streams"][1]["height"]
        str2 = result["videos_manifest"]["servers"][0]["streams"][2]["url"]
        resol2 = result["videos_manifest"]["servers"][0]["streams"][2]["height"]
        str3 = result["videos_manifest"]["servers"][0]["streams"][3]["url"]
        resol3 = result["videos_manifest"]["servers"][0]["streams"][3]["height"]
    except IndexError:
        str1 = result["videos_manifest"]["servers"][0]["streams"][0]["url"]
        resol1 = result["videos_manifest"]["servers"][0]["streams"][0]["height"]
        str2 = result["videos_manifest"]["servers"][0]["streams"][1]["url"]
        resol2 = result["videos_manifest"]["servers"][0]["streams"][1]["height"]
        str3 = result["videos_manifest"]["servers"][0]["streams"][2]["url"]
        resol3 = result["videos_manifest"]["servers"][0]["streams"][2]["height"]
    thumb = result["hentai_video"]["poster_url"]
    title = result["hentai_video"]["name"]
    dl = "https://hanime.tv/downloads/" + \
        base64.b64encode(result["hentai_video"]["slug"].encode()).decode()
    ret = {
        "url": video_url + "/" + id,
        "downloadURL": dl,
        "info": "1080p is currently supported at /getVideo/premium",
        "player_url": f"https://player.nscdn.ml/player.html?title={title}&file=[{resol3}]{str3},[{resol2}]{str2},[{resol1}]{str1}&poster={thumb}&download={dl}&default_quality=720p",
        "iframe_api": f"<iframe src='https://player.nscdn.ml/player.html?title={title}&file=[{resol1}]{str1},[{resol2}]{str2},[{resol3}]{str3}&poster={thumb}&download={dl}&default_quality=720p' frameborder='0' allowfullscreen width='360' height='526'></iframe>",
        "main_url": "https://player.nscdn.ml",
        "info": "The Player is not working somehow due to CORS error. Please use /getVideo instead or Use CORS Extension & Proxy."
    }
    return jsonify(ret), 200

@app.route('/getComment', methods=["GET"])
def getComment():
    vid_id = request.args.get("id")
    try:
        return jsonify({
            "comments": cmt_hanime.get_comments(vid_id),
            "total": cmt_hanime.get_totals(vid_id),
        }), 200
    except:
        return jsonify({"error": "No Hanime Video ID Provided", "status": "404"}), 404

@app.route('/getComment/reply', methods=["GET"])
def getreply():
    rpy_id = request.args.get("id")
    try:
        return jsonify({
            "comments": cmt_hanime.get_reply(rpy_id),
            "total": cmt_hanime.get_totals(rpy_id),
        }), 200
    except:
        return jsonify({"error": "No Reply ID", "status": "400"}), 400

@app.route('/getComment/reply/reply', methods=["GET"])
def getreplyreply():
    rpy2_id = request.args.get("id")
    try:
        return jsonify({
            "comments": cmt_hanime.get_reply_reply(rpy2_id),
            "total": cmt_hanime.get_totals(rpy2_id),
        }), 200
    except:
        return jsonify({"error": "No Reply ID", "status": "400"}), 400

@app.route('/getLanding', methods=["GET"])
def getLanding():
    return jsonify({"Info": "https://haniapi-docs.vercel.app/docs/getapi#getlanding"})

@app.route('/getLanding/recent', methods=["GET"])
@limiter.limit(req)
def getrecent():
    search_url = search_api
    print(landing)
    res_json = {
        "search_text": "",
        "tags":
            [],
        "brands":
            [],
        "blacklist":
            [],
        "order_by": "created_at_unix",
        "ordering": "desc",
        "page": "0",
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    response = requests.post(search_url, headers=headers, json=res_json)
    results = response.json()
    ret = {
        "results": json.loads(results['hits']),
        "page": results['page']
    }
    return jsonify(ret), 200

@app.route('/getLanding/newest', methods=["GET"])
@limiter.limit(req)
def getnew():
    res_json = {
        "search_text": "",
        "tags":
            [],
        "brands":
            [],
        "blacklist":
            [],
        "order_by": "released_at_unix",
        "ordering": "desc",
        "page": "0",
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    response = requests.post(search_api, headers=headers, json=res_json)
    results = response.json()
    ret = {
        "results": json.loads(results['hits']),
        "page": results['page']
    }
    return jsonify(ret), 200

@app.route('/getLanding/trending', methods=["GET"])
@limiter.limit(req)
def gettrend():
    time = request.args.get('time')
    p = request.args.get('p')
    if time is None:
        time = "month"
    elif p is None:
        p = "0"
    headers = {"X-Signature-Version": "web2",
               "X-Signature": secrets.token_hex(32)}
    res = requests.get(browse_trends+f"?time={time}&page={p}", headers=headers)
    results = res.json()
    ret = {
        "results": results["hentai_videos"],
        "time": results["time"],
        "page": results["page"]
    }
    return jsonify(ret), 200

# Search

@app.route('/search', methods=['POST'])
@limiter.limit(search_req)
def search():
    request_data = request.get_json(force=True)
    search_query = request_data['search']
    search_brand = request_data['brands']
    search_page = request_data['page']
    search_blacklist = request_data['blacklist']
    search_ordering = request_data['ordering']
    search_order_by = request_data['order_by']
    search_tag = request_data['tags']
    res_json = {
        "search_text": search_query,
        "tags":
            search_tag,
        "tags-mode": "AND",
        "brands":
            search_brand,
        "blacklist":
            search_blacklist,
        "order_by": search_order_by,
        "ordering": search_ordering,
        "page": search_page,
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    if search_tag == None and search_brand == None and search_blacklist == None:
        search_tag = []
        search_brand = []
        search_blacklist = []
    response = requests.post(search_api, headers=headers, json=res_json)
    results = response.json()
    ret = {
        "results": json.loads(results['hits']),
        "page": results['page']
    }
    return jsonify(ret), 200

@app.route('/search/req', methods=['GET'])
@limiter.limit(search_req)
def searchq():
    search_query = request.args.get("q")
    search_page = request.args.get("p")
    search_ordering = request.args.get("ordering")
    search_order_by = request.args.get("order_by")
    res_json = {
        "search_text": search_query,
        "tags":
            [],
        "brands":
            [],
        "blacklist":
            [],
        "order_by": search_order_by,
        "ordering": search_ordering,
        "page": search_page,
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    response = requests.post(search_api, headers=headers, json=res_json)
    results = response.json()
    ret = {
        "results": json.loads(results['hits']),
        "page": results['page']
    }
    return jsonify(ret), 200

# Browse

@app.route("/browse", methods=["GET"])
@limiter.limit(req)
def Browse():
    result = requests.get(browse)
    result = result.json()
    ret = {
        "video": "null",
        "tags": result["hentai_tags"],
        "brands": result["brands"],
    }
    return jsonify(ret), 200


@app.route("/browse/<type>/<tag>/<page>", methods=["GET"])
@limiter.limit(req)
def browsefilter(type, tag, page):
    browse_url = browse + "/" + type + "/" + \
        tag + f"?page={page}&order_by=created_at_unix&ordering=desc"
    headers = {"X-Signature-Version": "web2",
               "X-Signature": secrets.token_hex(32)}
    result = requests.get(browse_url, headers=headers)
    stt = result.status_code
    result = result.json()
    if stt == 404:
        return jsonify({"errors": "Not Found"}), 401
    ret = {
        "tag": tag,
        "videos": result["hentai_videos"],
        "page": result["number_of_pages"],
    }
    return jsonify(ret), 200


# User

@app.route('/user', methods=['GET'])
@limiter.limit(req)
def user():
    user_url = mychannel
    headers = {"X-Session-Token": request.headers.get("Token")}
    result = requests.get(user_url, headers=headers)
    stt = result.status_code
    result = result.json()
    if stt == 401:
        return jsonify({"errors": "Unauthorized. No User Session Token provided"}), 401
    ret = {}
    ret["user"] = result["user_channel"]
    ret["achievements"] = result["user_achievements"]
    ret["playlists"] = result["playlists"]
    return jsonify(ret), 200

@app.route('/user/<ch_id>', methods=['GET'])
@limiter.limit(req)
def oth_user(ch_id):
    user_url = channels + "/" + ch_id
    result = requests.get(user_url)
    stt = result.status_code
    result = result.json()
    if stt == 404:
        return jsonify({"errors": "User Not Found"}), 401
    ret = {}
    ret["user"] = result["user_channel"]
    ret["achievements"] = result["user_channel_user_achievements"]
    ret["playlists"] = result["user_channel_playlists"]
    return jsonify(ret), 200

# Community Upload


@app.route('/community_upload', methods=['GET'])
@limiter.limit(req)
def community_upload():
    page = request.args.get("p")
    if page == None:
        page = 1
    community_upload_url = f"{community}?channel_name__in[]=media&channel_name__in[]=nsfw-general&channel_name__in[]=furry&channel_name__in[]=futa&channel_name__in[]=yaoi&channel_name__in[]=yuri&channel_name__in[]=traps&channel_name__in[]=irl-3d&query_method=nav-to-page&page={page}&loc=https://hanime.tv"
    result = requests.get(community_upload_url)
    result = result.json()
    return jsonify(result), 200


@app.route("/community_upload", methods=["POST"])
def community_upload_fltr():
    request_data = request.get_json(force=True)
    page = request_data["page"]
    media = request_data["media"]
    nsfw = request_data["nsfw"]
    furry = request_data["furry"]
    futa = request_data["futa"]
    yaoi = request_data["yaoi"]
    yuri = request_data["yuri"]
    traps = request_data["traps"]
    irl_3d = request_data["irl_3d"]

    if media == "true" or media == "":
        media = "channel_name__in[]=media"
    else:
        media = ""
    if nsfw == "true":
        nsfw = "&channel_name__in[]=nsfw-general"
    else:
        nsfw = ""
    if furry == "true":
        furry = "&channel_name__in[]=furry"
    else:
        furry = ""
    if futa == "true":
        futa = "&channel_name__in[]=futa"
    else:
        futa = ""
    if yaoi == "true":
        yaoi = "&channel_name__in[]=yaoi"
    else:
        yaoi = ""
    if yuri == "true":
        yuri = "&channel_name__in[]=yuri"
    else:
        yuri = ""
    if traps == "true":
        traps = "&channel_name__in[]=traps"
    else:
        traps = ""
    if irl_3d == "true":
        irl_3d = "&channel_name__in[]=irl-3d"
    else:
        irl_3d = ""

    community_upload_url = f"{community}?{media}{nsfw}{furry}{futa}{yaoi}{yuri}{traps}{irl_3d}&query_method=nav-to-page&page={page}&loc=https://hanime.tv"
    result = requests.get(community_upload_url)
    result = result.json()
    return jsonify(result), 200


if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=8080)

