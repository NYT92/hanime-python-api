# Flask API Made by NYT92

# Credit to WeaveAche and Profility for the code
# https://github.com/WeaveAche/hanime-auto-coins-collector
# https://github.com/Profility/hanime-scraper

# api url : https://hani.nsdev.ml (deploy on deta.sh)
# docs : https://aslnk.ml/zwi3ag

# PLEASE DONT ABUSE IT JUST PLEASE JUST FUCKING DONT ABUSing IT...........
# Im not good at this shit so dont call me copy&paste guy 
# also i want to port this to nodejs but the process is kinda hard so i will do it later

import requests
import json
import time
import hanime
import cmt_hanime
import secrets
from hashlib import sha256
from dateutil import parser
from flask import Flask, request, jsonify
from flask_cors import CORS

# Config

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

base_url = "https://hanime.tv/"

# Error Handler + Index

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify(error=str(e)), 500

@app.errorhandler(503)
def server_unavailable(e):
    return jsonify({
        "error": "Server unavailable",
        "message": str(e)
    }), 503

@app.route('/')
def index(): 
    return jsonify(
        {
            'status': 'ok', 
            'Warning':'Never use this API in production and abusing there system, this is just for testing purposes and for fun only',
            'Github': 'https://github.com/nyt92',
            'Help': 'https://haniapi-docs.vercel.app',
        }
    ), 200

# Authentication

@app.route("/auth/login", methods=["GET"])
def authlogin():
    host = "https://hanime.tv/"
    hanime_email = request.args.get("email")
    hanime_password = request.args.get("password")

    def getSHA256(to_hash):
        m = sha256()
        m.update(to_hash.encode())
        return m.hexdigest()    

    def getXHeaders():
        XClaim = str(int(time.time()))
        XSig = getSHA256(f"9944822{XClaim}8{XClaim}113")
        headers = {"X-Signature-Version": "web2","X-Time": XClaim,"X-Signature": XSig}
        return headers 

    def login(s:requests.Session, email,password):
        s.headers.update(getXHeaders())
        response = s.post(f"{host}/rapi/v4/sessions", headers={"Content-Type":"application/json;charset=utf-8"},data=f'{{"burger":"{email}","fries":"{password}"}}')
        return getInfo(response.text)

    def getInfo(response):
        received = json.loads(response)
        return received

    def main():
        s = requests.Session()
        info = login(s,hanime_email, hanime_password)
        s.headers.update({"X-Session-Token":info["session_token"]})
        return info
    try:
        info = main()
        return jsonify(info), 200
    except:
        return jsonify({"error": "Unauthorized", "status":"401"}), 401

@app.route("/auth/login/getsession", methods=["GET"])
def authgetsession():
    host = "https://hanime.tv/"
    hanime_email = request.args.get("email")
    hanime_password = request.args.get("password")

    def getSHA256(to_hash):
        m = sha256()
        m.update(to_hash.encode())
        return m.hexdigest()    

    def getXHeaders():
        XClaim = str(int(time.time()))
        XSig = getSHA256(f"9944822{XClaim}8{XClaim}113")
        headers = {"X-Signature-Version": "web2","X-Time": XClaim,"X-Signature": XSig}
        return headers 

    def login(s:requests.Session, email,password):
        s.headers.update(getXHeaders())
        response = s.post(f"{host}/rapi/v4/sessions", headers={"Content-Type":"application/json;charset=utf-8"},data=f'{{"burger":"{email}","fries":"{password}"}}')
        return getInfo(response.text)

    def getInfo(response):
        received = json.loads(response)
        ret = {
            "Warning":"Please store the session token somewhere safe.",
            "Info" : "1 Session token only vaild for 30 days. If you want to use it again, you need to request again.",
        }
        ret["session_token"] = received["session_token"]
        return ret

    def main():
        s = requests.Session()
        info = login(s,hanime_email, hanime_password)
        s.headers.update({"X-Session-Token":info["session_token"]})
        return info
    try:
        info = main()
        return jsonify(info), 200
    except:
        return jsonify({"error": "Unauthorized", "status":"401"}), 401

@app.route("/auth/login/summary", methods=["GET"])
def authsummary():

    host = "https://hanime.tv/"
    hanime_email = request.args.get("email")
    hanime_password = request.args.get("password")

    def getSHA256(to_hash):
        m = sha256()
        m.update(to_hash.encode())
        return m.hexdigest()    

    def getXHeaders():
        XClaim = str(int(time.time()))
        XSig = getSHA256(f"9944822{XClaim}8{XClaim}113")
        headers = {"X-Signature-Version": "web2","X-Time": XClaim,"X-Signature": XSig}
        return headers 

    def login(s:requests.Session, email,password):
        s.headers.update(getXHeaders())
        response = s.post(f"{host}/rapi/v4/sessions", headers={"Content-Type":"application/json;charset=utf-8"},data=f'{{"burger":"{email}","fries":"{password}"}}')
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
        info = login(s,hanime_email, hanime_password)
        s.headers.update({"X-Session-Token":info["session_token"]})
        sum = ({
            "data": {
                "id": info["id"],
                "name":info["name"],
                "coin":info["coins"],
                "premium_status":info["premium"],
                "email":info["email"],
                "avatar":info["avatar"],
                "slug":info["slug"],
                "all_video_views":info["video_view"]
                }
            }
        )
        return sum
    try:
        info = main()
        return jsonify(info), 200
    except:
        return jsonify({"error": "Unauthorized", "status":"401"}), 401

@app.route("/auth/login/coins", methods=["GET"])
def authcoins():
    host = "https://hanime.tv/"
    hanime_email = request.args.get("email")
    hanime_password = request.args.get("password")

    def getSHA256(to_hash):
        m = sha256()
        m.update(to_hash.encode())
        return m.hexdigest()
    
    def getXHeaders():
        XClaim = str(int(time.time()))
        XSig = getSHA256(f"9944822{XClaim}8{XClaim}113")
        headers = {"X-Signature-Version": "app2","X-Claim": XClaim,"X-Signature": XSig}
        return headers

    def login(s:requests.Session, email,password):
        s.headers.update(getXHeaders())
        response = s.post(f"{host}/rapi/v4/sessions",headers={"Content-Type":"application/json;charset=utf-8"},data=f'{{"burger":"{email}","fries":"{password}"}}')
        
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
            print("[!!!] Unable to find the build number for the latest mobile app, please report an issue on github.")
        return ret

    def getCoins(s:requests.Session,version,uid):
        s.headers.update(getXHeaders())
        curr_time = str(int(time.time()))
        to_hash = f"coins{version}|{uid}|{curr_time}|coins{version}"
        data = {"reward_token": getSHA256(to_hash)+f"|{curr_time}" ,"version":f"{version}"}
        response = s.post(f"{host}/rapi/v4/coins",data=data)
        ret = json.loads(response.text)
        return jsonify({
            "rewarded_amount": ret["rewarded_amount"],
            "message" : "You have successfully collected your coins" 
        })
        
    def main():
        s = requests.Session()
        info = login(s,hanime_email, hanime_password)
        s.headers.update({"X-Session-Token":info["session_token"]})
        if time.time() - parser.parse(info["last_clicked"]).timestamp() < 3*3600:
            return jsonify({"error":"You have already clicked on an ad less than 3 hrs ago.","message" : "You have already clicked on an ad and recieve coins. Please wait for another 3 hours",  "total_coins":info["coins"]})
        return getCoins(s,info["version"],info["uid"])

    try:
        info = main()
        return info, 200
    except:
        return jsonify({"error": "Unauthorized", "status":"401"}), 401

@app.route("/auth/login/body", methods=["POST"])
def authbody():
    host = "https://hanime.tv/"
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
        headers = {"X-Signature-Version": "web2","X-Time": XClaim,"X-Signature": XSig}
        return headers 

    def login(s:requests.Session, email,password):
        s.headers.update(getXHeaders())
        response = s.post(f"{host}/rapi/v4/sessions", headers={"Content-Type":"application/json;charset=utf-8"},data=f'{{"burger":"{email}","fries":"{password}"}}')
        return getInfo(response.text)

    def getInfo(response):
        received = json.loads(response)
        return received

    def main():
        s = requests.Session()
        info = login(s,hanime_email, hanime_password)
        s.headers.update({"X-Session-Token":info["session_token"]})
        return info

    try:
        info = main()
        return jsonify(info), 200
    except:
        return jsonify({"error": "Unauthorized", "status":"401"}), 401

@app.route("/auth/coin/body", methods=["POST"])
def authcoinbody():
    host = "https://hanime.tv/"
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
        headers = {"X-Signature-Version": "app2","X-Claim": XClaim,"X-Signature": XSig}
        return headers

    def login(s:requests.Session, email,password):
        s.headers.update(getXHeaders())
        response = s.post(f"{host}/rapi/v4/sessions",headers={"Content-Type":"application/json;charset=utf-8"},data=f'{{"burger":"{email}","fries":"{password}"}}')
        
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
            print("[!!!] Unable to find the build number for the latest mobile app, please report an issue on github.")
        return ret

    def getCoins(s:requests.Session,version,uid):
        s.headers.update(getXHeaders())
        curr_time = str(int(time.time()))
        to_hash = f"coins{version}|{uid}|{curr_time}|coins{version}"
        data = {"reward_token": getSHA256(to_hash)+f"|{curr_time}" ,"version":f"{version}"}
        response = s.post(f"{host}/rapi/v4/coins",data=data)
        ret = json.loads(response.text)
        return jsonify({
            "rewarded_amount": ret["rewarded_amount"],
            "message" : "You have successfully collected your coins" 
        })
        
    def main():
        s = requests.Session()
        info = login(s,hanime_email, hanime_password)
        s.headers.update({"X-Session-Token":info["session_token"]})
        if time.time() - parser.parse(info["last_clicked"]).timestamp() < 3*3600:
            return jsonify({"error":"You have already clicked on an ad less than 3 hrs ago.","message" : "You have already clicked on an ad and recieve coins. Please wait for another 3 hours",  "total_coins":info["coins"]})
        return getCoins(s,info["version"],info["uid"])

    try:
        info = main()
        return info, 200
    except:
        return jsonify({"error": "Unauthorized", "status":"401"}), 401    

#API

@app.route('/getInfo', methods=["GET"])
def info():
    id = request.args.get('id')
    if (id == None):
        return jsonify({"error": "No Hanime Video Id or Slug Provided", "status":"400"}), 400
    results = requests.get(base_url + 'api/v8/video?id=' + id)
    results = results.json()

    return jsonify(
        {
            "slug": results["hentai_video"]["slug"],
            "id": results["hentai_video"]["id"],
            "info":hanime.info(id), 
            "description":results["hentai_video"]["description"],
            "tags":hanime.tags(id),
            "poster":hanime.poster(id),
            "video": base_url + "videos/hentai/" + id,
            "downloadURL" : hanime.download(request.args.get('id')),
        }
    ), 200

@app.route('/getVideo', methods=["GET"])
def getVideo():
    url = base_url + "api/v8/video?id="+ request.args.get('id')
    result = requests.get(url)
    result = result.json()
    ret = {
        "url" : base_url + "videos/hentai/" + request.args.get('id'),
        "downloadURL" : hanime.download(request.args.get('id')),
        "info" : "1080p is currently supported at /getVideo/premium"
    }
    ret["1080"] = result["videos_manifest"]["servers"][0]["streams"][0]
    ret["720"] = result["videos_manifest"]["servers"][0]["streams"][1]
    ret["480"] = result["videos_manifest"]["servers"][0]["streams"][2]
    ret["360"] = result["videos_manifest"]["servers"][0]["streams"][3]
    return jsonify(ret), 200

@app.route('/getVideo/premium', methods=["GET"])
def getVideopremium():
    url = base_url + "api/v8/video?id="+ request.args.get('id')
    result = requests.get(url, headers={"X-Session-Token": request.headers.get('Token')})
    
    result = result.json()
    ret = {
        "url" : base_url + "videos/hentai/" + request.args.get('id'),
        "downloadURL" : hanime.download(request.args.get('id')),
    }
    if result["videos_manifest"]["servers"][0]["streams"][0]["url"] == "" :
        return jsonify({"error":"Premium Account Only", "info":"use /getVideo instead of /getVideo/premium"}), 401

    ret["1080"] = result["videos_manifest"]["servers"][0]["streams"][0]
    ret["720"] = result["videos_manifest"]["servers"][0]["streams"][1]
    ret["480"] = result["videos_manifest"]["servers"][0]["streams"][2]
    ret["360"] = result["videos_manifest"]["servers"][0]["streams"][3]
    return jsonify(ret), 200

@app.route('/getComment', methods=["GET"])
def getComment():
    vid_id = request.args.get("id")
    if vid_id == None:
        return jsonify({"error": "No Hanime Video ID", "status":"400"}), 400

    return jsonify({
        "comments": cmt_hanime.get_comments(vid_id),
        "total": cmt_hanime.get_totals(vid_id),
        "info": hanime.info(vid_id)
    }), 200

@app.route('/getDownloadURL', methods=["GET"])
def getDownloadURL():
    return jsonify({"download_url" : hanime.download(request.args.get('id'))})

@app.route('/getLanding', methods=["GET"])
def getallld():
    request_url = base_url + "api/v8/landing"
    result = requests.get(request_url)
    result = result.json()
    return result

@app.route('/getLanding/recent', methods=["GET"])
def getldrecent():
    return jsonify({"test" : "ok"})    

# Search

@app.route('/search', methods=['POST'])
def search():
    #srv2-hani-api wont fetch to your website...
    search_url = "https://service2-haniapi.nsdev.ml/hanimetv/search/web2/"

    request_data = request.get_json(force=True)
    search_query = request_data['search']
    search_brand = request_data['brands']
    search_page = request_data['page']
    search_blacklist = request_data['blacklist']
    search_ordering = request_data['ordering']
    search_order_by = request_data['order_by']
    search_tag = request_data['tags']

    res_json = {
        "search": search_query,
        "tags":
            search_tag
        ,
        "brands": 
            search_brand
        ,
        "blacklist": 
            search_blacklist
        ,
        "order": search_order_by,
        "ordering": search_ordering,
        "page": search_page,
    }
    headers = {
        "Content-Type":"application/json; charset=utf-8"
    }
    if search_tag == None and search_brand == None and search_blacklist == None:
        search_tag = []
        search_brand = []
        search_blacklist = []
    response = requests.post(search_url, headers=headers, json=res_json)
    results = response.json()

    return jsonify(results, {"Info":"500 might happened if the requests body got typo", "docs":"https://haniapi-docs.vercel.app/docs/search"}), 200

@app.route('/search/req', methods=['GET'])
def searchq():
    #srv2-hani-api wont fetch to your website...
    search_url = "https://service2-haniapi.nsdev.ml/hanimetv/search/web2/"

    search_query = request.args.get("q")
    search_page = request.args.get("p")
    search_ordering = request.args.get("ordering")
    search_order_by = request.args.get("order_by")

    res_json = {
        "search": search_query,
        "tags":
            []
        ,
        "brands": 
            []
        ,
        "blacklist": 
            []
        ,
        "order": search_order_by,
        "ordering": search_ordering,
        "page": search_page,
    }
    headers = {
        "Content-Type":"application/json; charset=utf-8"
    }
    response = requests.post(search_url, headers=headers, json=res_json)
    results = response.json()

    return jsonify(results), 200

# Browse

@app.route("/browse" , methods=["GET"])
def browse():
    browse_url = base_url + "api/v8/browse"
    result = requests.get(browse_url)
    result = result.json()
    ret = {
        "video": "null",
        "tags": result["hentai_tags"],
        "brands": result["brands"],
    }
    return jsonify(ret), 200

@app.route("/browse/<type>/<tag>/<page>" , methods=["GET"])
def browsefilter(type, tag, page):
    browse_url = base_url + "api/v8/browse/" + type + "/" + tag + f"?page={page}&order_by=created_at_unix&ordering=desc"
    headers = {"X-Signature-Version": "web2","X-Signature": secrets.token_hex(32)}
    result = requests.get(browse_url, headers=headers)
    result = result.json()
    ret = {
        "tag": tag,
        "videos": result["hentai_videos"],
        "page": result["number_of_pages"],
    }
    return jsonify(ret), 200

# User

@app.route('/user', methods=['GET'])
def user():
    user_url = base_url + "rapi/v7/my_channel"
    headers = {"X-Session-Token": request.headers.get("Token")}
    result = requests.get(user_url, headers=headers)
    result = result.json()
    if request.headers.get("Token") == None:
        return jsonify({"errors": "Unauthorized", "message": "No User Session Token provided"}), 401
    ret = {}
    ret["user"] = result["user_channel"]
    ret["achievements"] = result["user_achievements"]
    ret["playlists"] = result["playlists"]
    return jsonify(ret), 200

@app.route('/user/<ch_id>', methods=['GET'])
def oth_user(ch_id):
    user_url = base_url + "rapi/v7/channels/" + ch_id
    result = requests.get(user_url)
    result = result.json()
    ret = {}
    if ch_id == None:
        return jsonify({"error": "User Not Found"}), 404
    ret["user"] = result["user_channel"]
    ret["achievements"] = result["user_channel_user_achievements"]
    ret["playlists"] = result["user_channel_playlists"]
    return jsonify(ret), 200

if __name__ == "__main__":
    app.run()
