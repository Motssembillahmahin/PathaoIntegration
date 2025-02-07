import requests

# 📌 Pathao API Login URL
LOGIN_URL = "https://merchant.pathao.com/api/v1/login"

# ✅ Pathao Merchant Credentials
PAYLOAD = {
    "username": "govaly.shop@gmail.com",
    "password": "JeioN@1702077"
}

# 📌 Store the Access Token
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI1Mjg4IiwianRpIjoiOTU3OGIyNTM0MjUyMWI2OTc3MWZjZmM2NmU0MDFiYTdmMjU5ZDFjOWEyODhiYzZjNDZhNTk0NmNkYmNiNWQ4NzFjZjA1OTJkNWI0ZGM5OWUiLCJpYXQiOjE3Mzc4NzU2ODcuMjg3MzM3LCJuYmYiOjE3Mzc4NzU2ODcuMjg3MzQxLCJleHAiOjE3NDU2NTE2ODcuMjY5MzE0LCJzdWIiOiIxOTg0ODEiLCJzY29wZXMiOltdfQ.Oy_Y8-xvJTUDjuqsI9VgBjT6Do9Y_Sf3XUxuKFGVtcSWxucfMcH7TSSoiliwmaXZaLkb2nxHzZaITU4BzMdrlTsCuQguiflPeKbsB_8Qzp3WjlbQWq2ZfNuAdTLV1RrogUDPx_3PqO_1kWCXSNaflc-KQq2TY1IKuHXA0zAogfm95aaGi46TgBd8woCwMAJrDG2HGdBG78RqVOmBg4JBolSvp-U2SMff7MA5kCD3sdWM8gXHRARLWmzsuhRzDsBLLSQNjz7ZkptYQNyHjmuqt8a8yZblrF7NYgR4m1YCF1z9Aaa5Y_zLThDIl1xyj6eW5iMm6HYbxlnUkV3Fcz9URcxTl9-bkkLEFb0cLTJjg04LCeDJSbwgFKU8B4a8lzZIWmTONma6RxHTrBzmxi6DwaUl3XZvtgqy72b1Kpdrwu5yR34yr7cM7yowHmjnS8FORu96sUm5Rf6jipiScQl5isD6TP7-VTJgqAoi1nhB_5ddJrfR1DFuUqrcQ-4BjcJMgiWvzHHa-LA1Gxx4dWpVaSedDl-UoeVFvQSgj2J8KuSgAJI4ajR_m65ob11lJoRywWm_f-rgA-La506OcIUbd7PqKtddd17d4eG1Hd8dquM6hgxle8msTjvkJL9OL_ys1FXolYC6QhW_tSalC_foNyPBHF-w_63j2Bh2avlHIk4"

def login():
    """Logs into Pathao Merchant and retrieves an access token."""
    global ACCESS_TOKEN

    try:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.post(LOGIN_URL, json=PAYLOAD, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            ACCESS_TOKEN = response_data.get("access_token")
            if not ACCESS_TOKEN:
                print("❌ Login successful, but access token not found")
                return None
            print(f"✅ Login successful! Access Token: {ACCESS_TOKEN}")
            return ACCESS_TOKEN
        else:
            print(f"❌ Login failed: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Login request failed: {e}")
        return None
