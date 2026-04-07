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
        .box {background:#1e293b;padding:20px;margin:50px auto;width:500px;border-radius:15px;}
        textarea {width:90%;height:120px;border-radius:10px;padding:10px;}
        button {background:#22c55e;border:none;padding:10px 20px;margin-top:10px;border-radius:10px;}
        .otp {background:#020617;margin:10px;padding:10px;border-radius:10px;display:flex;justify-content:space-between;}
        .copy {background:#3b82f6;padding:5px 10px;border-radius:8px;cursor:pointer;}
    </style>

    <script>
        function copyText(text) {
            navigator.clipboard.writeText(text);
            alert("Copied: " + text);
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
        {% for otp in results %}
            <div class="otp">
                <span>{{ otp }}</span>
                <div class="copy" onclick="copyText('{{ otp }}')">COPY</div>
            </div>
        {% endfor %}
    {% endif %}
</div>

</body>
</html>
"""

def get_otp(url):
    try:
        res = requests.get(url, timeout=5, headers={"user-agent": "Mozilla/5.0"})
        match = re.search(r"\b\d{6}\b", res.text)
        return match.group(0) if match else ""
    except:
        return ""

@app.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":
        links = [l.strip() for l in request.form["links"].splitlines() if l.strip()]

        with ThreadPoolExecutor(max_workers=20) as executor:
            otps = list(executor.map(get_otp, links))

        for otp in otps:
            if otp:
                results.append(otp)

    return render_template_string(HTML, results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
