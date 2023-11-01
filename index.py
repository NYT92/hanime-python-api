# Flask API Made by NYT92

# Credit to WeaveAche and Profility for the code
# https://github.com/WeaveAche/hanime-auto-coins-collector


import base64
import requests
import json
import cmt_hanime
import auth_hanime
import secrets
import configparser
import logging
from dateutil import parser
from waitress import serve
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

# Server Config
app = Flask(__name__)
config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 3600000
}
app.config.from_mapping(config)
cache = Cache(app)
CORS(app, resources={r"*": {"origins": "*"}})
limiter = Limiter(app=app, key_func=get_remote_address,
                  strategy='fixed-window', headers_enabled=True)
logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(message)s')
logger.info('API IS RUNNING')
logger.info('--------------------------------')
logger.info('Press Ctrl+C to stop the server.')
logger.info('--------------------------------')
logger.info(
    'Go to https://go.nyt92.eu.org/hanidocs for more information')
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
def method_not_allowed(e):
    return jsonify(error=str(e)), 405


@app.errorhandler(429)
def rate_limited(e):
    return jsonify(error=str(e)), 429


@app.errorhandler(500)
def server_error(e):
    return jsonify(error=str(e)), 500


@app.errorhandler(503)
def server_unavailable(e):
    return jsonify(error=str(e)), 503


@app.route('/')
def index():
    return jsonify({
        'status': 'ok',
        'Credit': 'Made by NYT92',
        'Github': 'https://github.com/nyt92/hanime-python-api',
        'Version': '5.1',
    }), 200

# Authentication


@app.route("/auth/login", methods=["POST"])
@limiter.limit(req)
@cache.cached(timeout=300)
def authbody():
    request_data = request.get_json(force=True)
    hanime_email = request_data['email']
    hanime_password = request_data['password']
    return jsonify(auth_hanime.authlogin(hanime_email, hanime_password))


@app.route("/auth/login/summary", methods=["POST"])
@cache.cached(timeout=300)
@limiter.limit(req)
def authsummarybody():
    request_data = request.get_json(force=True)
    hanime_email = request_data['email']
    hanime_password = request_data['password']
    received = auth_hanime.authlogin(hanime_email, hanime_password)
    return {
        "avatar": received["user"]["avatar_url"],
        "name": received["user"]["name"],
        "email": received["user"]["email"],
        "coins": received["user"]["coins"],
        "active_premium": received["user"]["alt_premium_status"],
        "id": received["user"]["id"],
        "slug": received["user"]["slug"],
        "video_view": received["user"]["video_views"],
        "session_token": received["session_token"]
    }


@app.route("/auth/getcoins", methods=["POST"])
@cache.cached(timeout=10)
@limiter.limit(req)
def authcoinbody():
    request_data = request.get_json(force=True)
    hanime_email = request_data['email']
    hanime_password = request_data['password']
    return jsonify(auth_hanime.getcoin(hanime_email, hanime_password))

# API


@app.route('/getInfo/<id>', methods=["GET"])
@limiter.limit(req)
def info(id):
    result = requests.get(f'{video_api_url}/?id={id}')
    if result.status_code == 404:
        return jsonify({"error": "No Hanime video id or slug provided", "status": "404"}), 404
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
    return jsonify({"slug": result["hentai_video"]["slug"], "id": result["hentai_video"]["id"], "title": result["hentai_video"]["name"], "views": res_view, "info": {"brand": result["hentai_video"]["brand"], "brand_slug": result["brand"]["slug"], "uploaded_date": res_crdt, "released_date": res_redt, "censored": result["hentai_video"]["is_censored"], }, "description": result["hentai_video"]["description"], "tags": [x["text"] for x in res_tags], "poster": result["hentai_video"]["cover_url"], "video": f"{video_url}/{id}", "downloadURL": res_dl}), 200


@app.route('/getVideo/<id>', methods=["GET"])
@limiter.limit(req)
def getVideo(id):
    url = f"{video_api_url}?id=" + id
    result = requests.get(url, headers={
        "X-Session-Token": request.headers.get('Token'),
    })
    if result.status_code == 404:
        return jsonify({"error": "No Hanime video id or slug provided", "status": "404"}), 404
    result = result.json()
    dl = "https://hanime.tv/downloads/" + \
        base64.b64encode(result["hentai_video"]["slug"].encode()).decode()
    ret = {
        "url": f"{video_url}/" + id, "download_url": dl, "streams": result["videos_manifest"]["servers"]
        [0]["streams"], "poster_url": result["hentai_video"]["poster_url"], "title": result["hentai_video"]["name"]}

    return jsonify(ret), 200


@app.route('/getComment', methods=["GET"])
def getComment():
    vid_id = request.args.get("id")
    try:
        return jsonify({
            "comments": cmt_hanime.get_comments(vid_id),
            "total": cmt_hanime.get_totals(vid_id),
        }), 200
    except Exception:
        return jsonify({"error": "No Hanime video id provided", "status": "404"}), 404


@app.route('/getComment/reply', methods=["GET"])
def getreply():
    rpy_id = request.args.get("id")
    try:
        return jsonify({
            "comments": cmt_hanime.get_reply(rpy_id),
            "total": cmt_hanime.get_totals(rpy_id),
        }), 200
    except Exception:
        return jsonify({"error": "No reply ID", "status": "400"}), 400


@app.route('/getComment/reply/reply', methods=["GET"])
def getreplyreply():
    rpy2_id = request.args.get("id")
    try:
        return jsonify({
            "comments": cmt_hanime.get_reply_reply(rpy2_id),
            "total": cmt_hanime.get_totals(rpy2_id),
        }), 200
    except Exception:
        return jsonify({"error": "No reply ID", "status": "400"}), 400


@app.route('/getLanding/recent', methods=["GET"])
@limiter.limit(req)
def getrecent():
    search_url = search_api
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
    res = requests.get(
        f"{browse_trends}?time={time}&page={p}", headers=headers)
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

    # Fixed KeyError
    search_query = request_data.get('search')
    search_brand = request_data.get('brands')
    search_page = request_data.get('page')
    search_blacklist = request_data.get('blacklist')
    search_ordering = request_data.get('ordering')
    search_order_by = request_data.get('order_by')
    search_tag = request_data.get('tags')

    # Fixed the error where the request being sent had empty strings,
    # where arrays were supposed to be
    if search_tag is None and search_brand is None and search_blacklist is None:
        search_tag = []
        search_brand = []
        search_blacklist = []

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

    response = requests.post(search_api, headers=headers, json=res_json)
    results = response.json()
    ret = {
        "results": json.loads(results['hits']),
        "page": results['page']
    }
    return jsonify(ret), 200


@app.route('/search', methods=['GET'])
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
    browse_url = f"{browse}/{type}/{tag}?page={page}&order_by=created_at_unix&ordering=desc"
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
        return jsonify({"errors": "Unauthorized, no user session token provided"}), 401
    ret = {"user": result["user_channel"],
           "achievements": result["user_achievements"], "playlists": result["playlists"]}
    return jsonify(ret), 200


@app.route('/user/<ch_id>', methods=['GET'])
@limiter.limit(req)
def oth_user(ch_id):
    user_url = f"{channels}/{ch_id}"
    result = requests.get(user_url)
    stt = result.status_code
    result = result.json()
    if stt == 404:
        return jsonify({"errors": "User Not Found"}), 401
    ret = {"user": result["user_channel"], "achievements": result["user_channel_user_achievements"],
           "playlists": result["user_channel_playlists"]}

    return jsonify(ret), 200

# Community Upload


@app.route('/community_upload', methods=['GET'])
@limiter.limit(req)
def community_upload():
    page = request.args.get("p")
    if page is None:
        page = 1
    community_upload_url = f"{community}?channel_name__in[]=media&channel_name__in[]=nsfw-general&channel_name__in[]=furry&channel_name__in[]=futa&channel_name__in[]=yaoi&channel_name__in[]=yuri&channel_name__in[]=traps&channel_name__in[]=irl-3d&query_method=nav-to-page&page={page}&loc=https://hanime.tv"
    result = requests.get(community_upload_url)
    result = result.json()
    return jsonify(result), 200


@app.route("/community_upload", methods=["POST"])
@limiter.limit(req)
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

    media = "channel_name__in[]=media" if media == True else ""
    nsfw = "&channel_name__in[]=nsfw-general" if nsfw == True else ""
    furry = "&channel_name__in[]=furry" if furry == True else ""
    futa = "&channel_name__in[]=futa" if futa == True else ""
    yaoi = "&channel_name__in[]=yaoi" if yaoi == True else ""
    yuri = "&channel_name__in[]=yuri" if yuri == True else ""
    traps = "&channel_name__in[]=traps" if traps == True else ""
    irl_3d = "&channel_name__in[]=irl-3d" if irl_3d == True else ""

    community_upload_url = f"{community}?{media}{nsfw}{furry}{futa}{yaoi}{yuri}{traps}{irl_3d}&query_method=nav-to-page&page={page}&loc=https://hanime.tv"
    result = requests.get(community_upload_url)
    result = result.json()
    return jsonify(result), 200


if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=8080)
    # app.run(host="127.0.0.1", port=8080)
