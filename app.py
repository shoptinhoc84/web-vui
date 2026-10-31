import os
from flask import Flask, request, render_template_string, redirect, url_for, abort
from itsdangerous import URLSafeSerializer, BadSignature

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "doi-chuoi-bi-mat-nay-khi-dua-len-render")
serializer = URLSafeSerializer(app.config["SECRET_KEY"], salt="thiep-loi-chuc-v1")

CREATE_PAGE = r"""
<!doctype html><html lang="vi"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tạo thiệp gửi riêng</title>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;700;800;900&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}body{margin:0;min-height:100vh;padding:28px 14px;background:radial-gradient(circle at 15% 15%,#fff2c9,transparent 28%),radial-gradient(circle at 90% 20%,#ffd8ec,transparent 30%),linear-gradient(135deg,#d8f5ff,#f5e3ff 55%,#ffe4ed);font-family:Nunito,sans-serif;color:#38284f}.wrap{width:min(760px,100%);margin:auto}.panel{background:#ffffffcf;border:1px solid white;border-radius:26px;padding:clamp(18px,4vw,32px);box-shadow:0 18px 55px #6c4e9a20}header{text-align:center;margin:12px 0 24px}.tag{display:inline-block;padding:7px 15px;border-radius:30px;background:#ffffffb8;font-weight:900}h1{font:800 clamp(32px,6vw,50px)/1.1 "Baloo 2";color:#7247b9;margin:14px 0 7px}header p{color:#76658b;font-weight:700}label{display:block;font-weight:900;margin:0 0 9px}textarea{width:100%;min-height:120px;border:2px solid #eadcff;border-radius:17px;padding:15px;font:700 17px Nunito;color:#46335d;resize:vertical;outline:none}textarea:focus{border-color:#a98aff}button{border:0;border-radius:999px;padding:13px 21px;font:900 15px Nunito;cursor:pointer;color:white;background:linear-gradient(110deg,#ff70ad,#936cff);box-shadow:0 8px 18px #b16be94a;margin-top:14px}.hint{font-size:13px;color:#887b98;line-height:1.6}.result{display:none;margin-top:20px;padding:16px;background:#f5efff;border-radius:17px;overflow-wrap:anywhere}.result.show{display:block}.result a{color:#754bd0;font-weight:900}.footer{text-align:center;color:#887b98;font-size:12px;margin-top:18px}
</style></head><body><main class="wrap">
<header><span class="tag">💌 THIỆP RIÊNG DÀNH TẶNG AI ĐÓ</span><h1>Tạo lời chúc bất ngờ</h1><p>Bạn viết lời chúc, website tạo một link riêng để gửi người nhận.</p></header>
<section class="panel">
<form id="createForm" method="post" action="/create">
<label for="message">Nhập lời chúc của bạn</label>
<textarea id="message" name="message" maxlength="300" required placeholder="Ví dụ: Chúc Diên một ngày mới vui vẻ, hạnh phúc">Chúc Diên một ngày mới vui vẻ, hạnh phúc</textarea>
<button type="submit">✨ Tạo thiệp và lấy link gửi đi</button>
</form>
<p class="hint">Người nhận mở link chỉ xem được thiệp. Họ không thấy ô nhập và không có chức năng sửa lời chúc.</p>
<div id="result" class="result"></div>
</section><div class="footer">Made with 💗 • Một lời chúc nhỏ, một niềm vui lớn</div>
<script>
document.getElementById('createForm').addEventListener('submit',async function(e){
 e.preventDefault(); const btn=this.querySelector('button'); btn.disabled=true;btn.textContent='Đang tạo thiệp...';
 try{
  const response=await fetch('/create',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(this))});
  const data=await response.json(); if(!response.ok) throw new Error(data.error||'Không tạo được link');
  const box=document.getElementById('result');box.classList.add('show');
  box.innerHTML='<b>🎉 Thiệp đã sẵn sàng! Link dành riêng cho người nhận:</b><br><a id="giftLink" href="'+data.url+'" target="_blank" rel="noopener">'+data.url+'</a><br><button type="button" id="copyBtn">🔗 Sao chép link gửi Zalo</button>';
  document.getElementById('copyBtn').onclick=async()=>{try{await navigator.clipboard.writeText(data.url);document.getElementById('copyBtn').textContent='✅ Đã sao chép!'}catch(err){prompt('Sao chép link này:',data.url)}};
 }catch(err){alert(err.message)}finally{btn.disabled=false;btn.textContent='✨ Tạo thiệp và lấy link gửi đi'}
});
</script></main></body></html>
"""

GIFT_PAGE = r"""
<!doctype html><html lang="vi"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Một lời chúc dành tặng bạn</title>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;700;800;900&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}body{margin:0;min-height:100vh;padding:22px 14px;display:grid;place-items:center;font-family:Nunito,sans-serif;background:linear-gradient(135deg,#d8f5ff,#f5e3ff 55%,#ffe4ed)}.wrap{width:min(900px,100%);text-align:center}.card{min-height:470px;position:relative;isolation:isolate;overflow:hidden;border-radius:30px;display:grid;place-items:center;padding:40px 24px;color:white;background-size:cover;background-position:center;box-shadow:0 22px 65px #50356c45}.card:before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(135deg,#24133ba8,#57245d66,#11194488)}.card:after{content:"";position:absolute;inset:13px;border:1px solid #ffffff99;border-radius:20px;pointer-events:none}.content{position:relative;z-index:2;max-width:760px;text-shadow:0 3px 14px #1b123baa}.small{font-size:12px;font-weight:900;letter-spacing:.2em}.message{font:800 clamp(34px,7vw,66px)/1.12 "Baloo 2";margin:22px 0;overflow-wrap:anywhere}.sub{font-size:17px;font-weight:800}.decor{position:absolute;z-index:1;font-size:clamp(30px,6vw,56px);filter:drop-shadow(0 4px 8px #0005);animation:float 4s ease-in-out infinite}.a{top:8%;left:8%}.b{top:12%;right:9%;animation-delay:-1s}.c{bottom:10%;left:12%;animation-delay:-2s}.d{bottom:9%;right:12%;animation-delay:-.5s}.spark{position:absolute;width:7px;height:7px;border-radius:50%;background:white;box-shadow:0 0 15px 5px white;animation:twinkle 1.7s infinite alternate}.footer{color:#77658b;font-size:13px;margin-top:17px;font-weight:800}@keyframes float{50%{transform:translateY(-18px) rotate(9deg)}}@keyframes twinkle{to{opacity:1;transform:scale(1.6)}}@media(max-width:550px){.card{min-height:410px}}
</style></head><body><main class="wrap">
<div class="card" id="card">
<span class="decor a" id="d1">🌸</span><span class="decor b" id="d2">✨</span><span class="decor c" id="d3">🦋</span><span class="decor d" id="d4">💖</span>
<div class="content"><div class="small" id="kicker">A LITTLE SURPRISE FOR YOU</div><div class="message">{{ message }}</div><div class="sub" id="sub">Mong hôm nay của bạn thật rực rỡ! ☀️</div></div>
</div><div class="footer">💗 Có người gửi bạn một điều dễ thương. Chúc bạn luôn vui vẻ!</div>
<script>
const backgrounds=[
"https://images.unsplash.com/photo-1490730141103-6cac27aaab94?auto=format&fit=crop&w=1600&q=85",
"https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=1600&q=85",
"https://images.unsplash.com/photo-1490750967868-88aa4486c946?auto=format&fit=crop&w=1600&q=85",
"https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&w=1600&q=85",
"https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1600&q=85",
"https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=85",
"https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1600&q=85"];
const themes=[
{icons:["🌸","🦋","💗","✨"],k:"A LITTLE FLOWER FOR YOU",s:"Chúc bạn luôn xinh tươi như những đóa hoa 🌷"},
{icons:["🎈","🎉","🌟","🥳"],k:"TODAY IS YOUR DAY",s:"Cười thật tươi và đón điều tuyệt vời nhé!"},
{icons:["🌈","☀️","💛","🍀"],k:"A BRIGHT NEW DAY",s:"May mắn và niềm vui đang chờ bạn phía trước!"},
{icons:["💖","💕","🌹","✨"],k:"SENDING YOU LOVE",s:"Mong mọi điều dịu dàng sẽ đến bên bạn."},
{icons:["🌊","🐚","🫧","☀️"],k:"GOOD VIBES ONLY",s:"Thả lỏng, tận hưởng và vui hết mình nhé!"}];
function pick(a){return a[Math.floor(Math.random()*a.length)]}
const theme=pick(themes);document.getElementById('card').style.backgroundImage='url("'+pick(backgrounds)+'")';
['d1','d2','d3','d4'].forEach((id,i)=>document.getElementById(id).textContent=theme.icons[i]);
document.getElementById('kicker').textContent=theme.k;document.getElementById('sub').textContent=theme.s;
for(let i=0;i<28;i++){let x=document.createElement('i');x.className='spark';x.style.left=(3+Math.random()*94)+'%';x.style.top=(3+Math.random()*94)+'%';x.style.animationDelay=(Math.random()*2)+'s';document.getElementById('card').appendChild(x)}
</script></main></body></html>
"""

@app.route("/")
def home():
    return render_template_string(CREATE_PAGE)

@app.route("/create", methods=["POST"])
def create():
    message = (request.form.get("message") or "").strip()
    if not message:
        return {"error": "Bạn chưa nhập lời chúc."}, 400
    if len(message) > 300:
        return {"error": "Lời chúc tối đa 300 ký tự."}, 400
    token = serializer.dumps({"message": message})
    return {"url": request.url_root.rstrip("/") + url_for("gift", token=token)}

@app.route("/thiep/<token>")
def gift(token):
    try:
        data = serializer.loads(token)
        message = data.get("message", "")
        if not isinstance(message, str) or not message:
            abort(404)
    except BadSignature:
        abort(404)
    return render_template_string(GIFT_PAGE, message=message)

@app.errorhandler(404)
def not_found(_):
    return "Link thiệp không hợp lệ hoặc đã bị thay đổi.", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
