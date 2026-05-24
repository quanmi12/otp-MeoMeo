from flask import Flask, request, render_template_string
import requests
import re
from concurrent.futures import ThreadPoolExecutor
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>OTP Tool</title>

    <style>
        body{
            background:#0f172a;
            color:white;
            font-family:Arial;
            text-align:center;
        }

        .box{
            background:#1e293b;
            width:650px;
            margin:50px auto;
            padding:20px;
            border-radius:15px;
        }

        textarea{
            width:90%;
            height:150px;
            padding:10px;
            border:none;
            border-radius:10px;
            outline:none;
        }

        button{
            margin-top:15px;
            padding:10px 20px;
            border:none;
            border-radius:10px;
            cursor:pointer;
            background:#22c55e;
            color:white;
            font-size:16px;
        }

        .result-box{
            margin-top:20px;
            background:#020617;
            padding:15px;
            border-radius:10px;
            text-align:left;
            white-space:pre-line;
        }
    </style>

    <script>
        function copyAll(){
            let text = document.getElementById("otpBox").innerText;
            navigator.clipboard.writeText(text);
            alert("Đã copy");
        }
    </script>

</head>

<body>

<div class="box">

    <h1>⚡ OTP TOOL ⚡</h1>

    <form method="POST">

        <textarea name="links" placeholder="Mỗi dòng 1 link"></textarea>

        <br>

        <button type="submit">LẤY OTP</button>

    </form>

    {% if results %}

    <br>

    <button onclick="copyAll()">COPY ALL</button>

    <div class="result-box" id="otpBox">

{% for r in results %}
{{ r }}
{% endfor %}

    </div>

    {% endif %}

</div>

</body>
</html>
"""

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_otp(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10,
            verify=False
        )

        otp = re.search(r"\b\d{4,6}\b", response.text)

        if otp:
            return otp.group(0)

        return "ĐÉO VỀ"

    except Exception as e:
        return f"ERROR: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():

    results = []

    if request.method == "POST":

        links = request.form.get("links", "")

        links = [
            x.strip()
            for x in links.splitlines()
            if x.strip()
        ]

        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(get_otp, links))

    return render_template_string(
        HTML,
        results=results
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
