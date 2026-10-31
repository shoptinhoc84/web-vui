from flask import Flask, request, render_template_string
from urllib.parse import quote

app = Flask(__name__)

PAGE = r"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Thiệp vui nhộn & lung linh</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;600;700;800&family=Nunito:wght@400;700;800;900&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}body{margin:0;min-height:100vh;padding:26px 14px 45px;font-family:Nunito,sans-serif;color:#38284f;background:radial-gradient(circle at 15% 15%,#fff2c9,transparent 28%),radial-gradient(circle at 90% 20%,#ffd8ec,transparent 30%),linear-gradient(135deg,#d8f5ff,#f5e3ff 55%,#ffe4ed)}
.wrap{width:min(940px,100%);margin:auto}header{text-align:center;margin:8px 0 22px}.tag{display:inline-block;padding:7px 15px;border-radius:30px;background:#ffffffb8;font-weight:900}h1{font:800 clamp(30px,6vw,52px)/1.05 "Baloo 2",cursive;margin:14px 0 8px;color:#7247b9;text-shadow:0 3px #fff}header p{font-weight:700;color:#76658b}
.panel{background:#ffffffc9;border:1px solid white;box-shadow:0 18px 55px #6c4e9a20;border-radius:26px;padding:clamp(16px,3vw,28px)}label{display:block;font-weight:900;margin-bottom:9px}textarea{width:100%;min-height:100px;resize:vertical;border:2px solid #eadcff;border-radius:17px;padding:15px;font:700 17px Nunito;color:#46335d;outline:none}textarea:focus{border-color:#a98aff}.controls,.actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}button{border:0;border-radius:999px;padding:12px 19px;font:900 15px Nunito;cursor:pointer}.primary{color:white;background:linear-gradient(110deg,#ff70ad,#936cff);box-shadow:0 8px 18px #b16be94a}.secondary{color:#694c91;background:#f0e8ff}.hint{color:#887b98;font-size:13px}.stage{margin-top:22px}.card{min-height:390px;border-radius:28px;overflow:hidden;position:relative;isolation:isolate;display:grid;place-items:center;padding:34px 24px;text-align:center;color:white;background-size:cover;background-position:center;box-shadow:0 22px 55px #5c3b7c35}.card:before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(135deg,#2a174b99,#54235b66,#151a4788)}.card:after{content:"";position:absolute;inset:12px;border:1px solid #ffffff88;border-radius:20px;pointer-events:none}.content{max-width:760px;position:relative;z-index:2;text-shadow:0 3px 12px #1b123b88}.small{font-weight:900;letter-spacing:.18em;text-transform:uppercase;font-size:12px}.message{font:800 clamp(31px,6vw,58px)/1.15 "Baloo 2",cursive;margin:18px 0;overflow-wrap:anywhere}.sub{font-weight:800;font-size:17px}.decor{position:absolute;z-index:1;font-size:clamp(25px,5vw,46px);animation:float 4s ease-in-out infinite;filter:drop-shadow(0 4px 8px #0004)}.d1{top:8%;left:8%}.d2{top:14%;right:9%;animation-delay:-1s}.d3{bottom:10%;left:12%;animation-delay:-2s}.d4{bottom:9%;right:12%;animation-delay:-.5s}.spark{position:absolute;width:7px;height:7px;border-radius:50%;background:white;box-shadow:0 0 14px 5px white;animation:twinkle 1.8s infinite alternate}@keyframes float{50%{transform:translateY(-17px) rotate(8deg)}}@keyframes twinkle{to{opacity:1;transform:scale(1.5)}}.footer{text-align:center;color:#887b98;font-size:12px;margin-top:18px}@media(max-width:560px){.card{min-height:340px}}
</style></head>
<body><div class="wrap">
<header><span class="tag">✨ MÓN QUÀ NHỎ MỖI NGÀY ✨</span><h1>Tạo thiệp bất ngờ</h1><p>Viết lời chúc — mỗi lần bấm sẽ có một phong cách lung linh khác nhau!</p></header>
<section class="panel">
<label for="msg">💌 Nhập lời chúc hoặc dòng chữ muốn gửi</label>
<textarea id="msg" maxlength="180" placeholder="Nhập lời chúc của bạn...">{{ message }}</textarea>
<div class="controls"><button class="primary" onclick="makeCard()">🌈 Tạo thiệp ngẫu nhiên</button><button class="secondary" onclick="surprise()">🎁 Câu chúc bất ngờ</button></div>
<p class="hint">Mỗi lần tạo sẽ đổi ảnh nền, biểu tượng và hiệu ứng. Sau khi tạo, hãy sao chép link để gửi qua Zalo.</p>
<div class="stage" id="stage"><div class="card" id="card">
<span class="decor d1">🌸</span><span class="decor d2">✨</span><span class="decor d3">🦋</span><span class="decor d4">💖</span>
<div class="content"><div class="small" id="kicker">A LITTLE NOTE FOR YOU</div><div class="message" id="out"></div><div class="sub" id="sub">Mong hôm nay của bạn thật rực rỡ! ☀️</div></div>
</div><div class="actions"><button class="primary" onclick="makeCard()">🔄 Đổi phong cách</button><button class="secondary" onclick="shareLink()">🔗 Sao chép link thiệp</button></div></div>
</section><div class="footer">Made with 💗 • Gửi một chút niềm vui đến người bạn quý mến</div></div>
<script>
const backgrounds=[
"https://images.unsplash.com/photo-1490730141103-6cac27aaab94?auto=format&fit=crop&w=1600&q=85",
"https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=1600&q=85",
"https://images.unsplash.com/photo-1490750967868-88aa4486c946?auto=format&fit=crop&w=1600&q=85",
"https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&w=1600&q=85",
"https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1600&q=85",
"https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=85",
"https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1600&q=85"];
const styles=[
{icons:["🌸","🦋","💗","✨"],k:"A LITTLE FLOWER FOR YOU",s:"Chúc bạn luôn xinh tươi như những đóa hoa 🌷"},
{icons:["🎈","🎉","🌟","🥳"],k:"TODAY IS YOUR DAY",s:"Cười thật tươi và đón điều tuyệt vời nhé!"},
{icons:["🌈","☀️","💛","🍀"],k:"A BRIGHT NEW DAY",s:"May mắn và niềm vui đang chờ bạn phía trước!"},
{icons:["💖","💕","🌹","✨"],k:"SENDING YOU LOVE",s:"Mong mọi điều dịu dàng sẽ đến bên bạn."},
{icons:["🌊","🐚","🫧","☀️"],k:"GOOD VIBES ONLY",s:"Thả lỏng, tận hưởng và vui hết mình nhé!"}];
const surprises=["Chúc bạn hôm nay cười nhiều hơn hôm qua! 🌻","Một ngày mới, một niềm vui mới. Bạn xứng đáng với những điều tốt đẹp! 💖","Chúc mọi việc hanh thông, tâm trạng luôn rạng rỡ! ☀️","Gửi bạn một chiếc ôm thật to và thật nhiều may mắn! 🧸"];
let current="";
function pick(a){return a[Math.floor(Math.random()*a.length)]}
function makeCard(){let m=document.getElementById('msg').value.trim();if(!m){alert('Bạn hãy nhập lời chúc trước nhé!');return}current=m;let st=pick(styles),card=document.getElementById('card');card.style.backgroundImage=`url("${pick(backgrounds)}")`;document.getElementById('out').textContent=m;document.getElementById('kicker').textContent=st.k;document.getElementById('sub').textContent=st.s;document.querySelectorAll('.decor').forEach((e,i)=>e.textContent=st.icons[i]);document.querySelectorAll('.spark').forEach(e=>e.remove());for(let i=0;i<18;i++){let e=document.createElement('i');e.className='spark';e.style.left=(5+Math.random()*90)+'%';e.style.top=(5+Math.random()*90)+'%';e.style.animationDelay=(Math.random()*2)+'s';card.appendChild(e)}history.replaceState(null,'',location.pathname+'?text='+encodeURIComponent(m))}
function surprise(){document.getElementById('msg').value=pick(surprises);makeCard()}
async function shareLink(){let url=location.origin+location.pathname+'?text='+encodeURIComponent(current);try{await navigator.clipboard.writeText(url);alert('Đã sao chép link thiệp!')}catch(e){prompt('Sao chép link này:',url)}}
const params=new URLSearchParams(location.search);if(params.has('text'))document.getElementById('msg').value=params.get('text');makeCard();
</script></body></html>"""

@app.route("/")
def home():
    message = request.args.get("text", "Chúc Diên một ngày mới vui vẻ, hạnh phúc")
    return render_template_string(PAGE, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
