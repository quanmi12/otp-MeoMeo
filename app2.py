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
    <title>OTP Meo Meo</title>
    <style>
        body {background:#0f172a;color:white;font-family:Arial;text-align:center;}
        .box {background:#1e293b;padding:20px;margin:50px auto;width:600px;border-radius:15px;}
        textarea {width:90%;height:120px;border-radius:10px;padding:10px;}
        button {background:#22c55e;border:none;padding:10px 20px;margin-top:10px;border-radius:10px;cursor:pointer;}
        
        .result-box {
            background:#020617;
            padding:15px;
            border-radius:10px;
            width:90%;
            margin:auto;
            text-align:left;
            font-size:18px;
            line-height:1.8;
            margin-top:10px;
            white-space: pre-line;
        }
    </style>

    <script>
        function copyAll() {
            let text = document.getElementById("otpBox").innerText;
            navigator.clipboard.writeText(text);
            alert("Đã copy!");
        }
    </script>
</head>
<body>

<div class="box">
    <h1>⚡ OTP TOOL ⚡</h1>
    <p>by: Meo Meo</p>

    <form method="post">
        <textarea name="links" placeholder="Mỗi dòng 1 link"></textarea><br>
        <button type="submit">LẤY OTP</button>
    </form>

    {% if results %}
        <h3>Kết quả:</h3>

        <button onclick="copyAll()">COPY ALL</button>

        <div id="otpBox" class="result-box">
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
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}

def get_otp(url):
    try:
        res = requests.get(url, timeout=5, headers=HEADERS)

        match = re.search(r"\d{4,6}", res.text)

        if match:
            return match.group(0)
        else:
            return "ĐÉO VỀ"

    except:
        return "ĐÉO VỀ"

@app.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":
        links = [l.strip() for l in request.form["links"].splitlines() if l.strip()]

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(get_otp, links))

    return render_template_string(HTML, results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
