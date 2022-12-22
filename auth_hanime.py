import requests
import time
import secrets
import configparser
import json
from hashlib import sha256
from dateutil import parser

# Config
config_obj = configparser.ConfigParser()
config_obj.read("config.ini")

# Main
main_base = config_obj["main"]
base_url = main_base["base_url"]

def authlogin(hanime_email: str, hanime_password: str) -> dict:
    def getXHeaders():
        XClaim = str(int(time.time()))
        return {"X-Signature-Version": "web2", "X-Time": XClaim, "X-Signature": secrets.token_hex(32)}

    def login(s: requests.Session, email, password):
        s.headers.update(getXHeaders())
        response = s.post(f"{base_url}/rapi/v4/sessions", headers={
                          "Content-Type": "application/json;charset=utf-8"},
                          data=f'{{"burger":"{email}","fries":"{password}"}}')
        return getInfo(response.text)

    def getInfo(response):
        return json.loads(response)

    def main():
        s = requests.Session()
        info = login(s, hanime_email, hanime_password)
        s.headers.update({"X-Session-Token": info["session_token"]})
        return info
    try:
        info = main()
        return info
    except:
        return 'Unauthorized. Invalid Email or Password'


def getcoin(hanime_email: str, hanime_password: str) -> dict:
    def getSHA256(to_hash):
        m = sha256()
        m.update(to_hash.encode())
        return m.hexdigest()

    def getXHeaders():
        XClaim = str(int(time.time()))
        XSig = getSHA256(f"9944822{XClaim}8{XClaim}113")
        return {"X-Signature-Version": "app2", "X-Claim": XClaim, "X-Signature": XSig}

    def login(s: requests.Session, email, password):
        s.headers.update(getXHeaders())
        response = s.post(f"{base_url}/rapi/v4/sessions", headers={
                          "Content-Type": "application/json;charset=utf-8"}, data=f'{{"burger":"{email}","fries":"{password}"}}')

        if '{"errors":["Unauthorized"]}' in response.text:
            return ("[!!!] Login failed, please check your credentials.")
        else:
            return getInfo(response.text)

    def getInfo(response):
        received = json.loads(response)
        ret = {"session_token": received["session_token"], "uid": received["user"]["id"], "name": received["user"]
               ["name"], "coins": received["user"]["coins"], "last_clicked": received["user"]["last_rewarded_ad_clicked_at"]}

        available_keys = list(received["env"]["mobile_apps"].keys())

        if "_build_number" in available_keys:
            ret["version"] = received["env"]["mobile_apps"]["_build_number"]
        elif "osts_build_number" in available_keys:
            ret["version"] = received["env"]["mobile_apps"]["osts_build_number"]
        elif "severilous_build_number" in available_keys:
            ret["version"] = received["env"]["mobile_apps"]["severilous_build_number"]
        else:
            return(
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
        return {
            "rewarded_amount": ret["rewarded_amount"],
            "message": "You have successfully collected your coins"
        }

    def main():
        s = requests.Session()
        info = login(s, hanime_email, hanime_password)
        s.headers.update({"X-Session-Token": info["session_token"]})
        if time.time() - parser.parse(info["last_clicked"]).timestamp() < 3*3600:
            return {"error": "You have already clicked on an ad less than 3 hrs ago.", "message": "You have already clicked on an ad and recieve coins. Please wait for another 3 hours",  "total_coins": info["coins"]}
        return getCoins(s, info["version"], info["uid"])
    try:
        info = main()
        return info
    except:
        return {"error": "Unauthorized", "status": "401"}
