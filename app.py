
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flappy Bird",
    page_icon="🐤",
    layout="centered"
)

st.title("🐤 Flappy Bird")
st.write("Chạm màn hình hoặc nhấn Space để bay!")

game_html = """
<div style="text-align:center">
<canvas id="game" width="360" height="520"
style="width:100%;max-width:360px;border:3px solid #333;
border-radius:12px;background:#87CEEB;touch-action:manipulation">
</canvas>
<p>
<button onclick="startGame()" style="font-size:18px;padding:10px 24px">
Chơi lại
</button>
</p>
</div>

<script>
const c = document.getElementById("game");
const ctx = c.getContext("2d");

let bird, pipes, score, frame, running, started;

function reset() {
  bird = {x:75, y:220, v:0};
  pipes = [];
  score = 0;
  frame = 0;
  running = false;
  started = false;
  draw();
}

function startGame() {
  bird = {x:75, y:220, v:0};
  pipes = [];
  score = 0;
  frame = 0;
  running = true;
  started = true;
}

function flap() {
  if (!started) startGame();
  if (running) bird.v = -6.5;
  else startGame();
}

c.addEventListener("pointerdown", flap);
document.addEventListener("keydown", e => {
  if (e.code === "Space" || e.code === "ArrowUp") {
    e.preventDefault();
    flap();
  }
});

function draw() {
  ctx.clearRect(0,0,360,520);

  ctx.fillStyle = "#87CEEB";
  ctx.fillRect(0,0,360,520);

  ctx.fillStyle = "#fff";
  ctx.beginPath();
  ctx.arc(60,75,20,0,Math.PI*2);
  ctx.arc(82,75,27,0,Math.PI*2);
  ctx.arc(105,75,18,0,Math.PI*2);
  ctx.fill();

  ctx.fillStyle = "#70c94a";
  for (const p of pipes) {
    ctx.fillRect(p.x,0,52,p.top);
    ctx.fillRect(p.x,p.top+135,52,520-p.top-135);
    ctx.fillStyle = "#4a9c32";
    ctx.fillRect(p.x-4,p.top-15,60,15);
    ctx.fillRect(p.x-4,p.top+135,60,15);
    ctx.fillStyle = "#70c94a";
  }

  ctx.fillStyle = "#f7d33d";
  ctx.beginPath();
  ctx.arc(bird.x,bird.y,13,0,Math.PI*2);
  ctx.fill();

  ctx.fillStyle = "#fff";
  ctx.beginPath();
  ctx.arc(bird.x+5,bird.y-4,5,0,Math.PI*2);
  ctx.fill();

  ctx.fillStyle = "#222";
  ctx.beginPath();
  ctx.arc(bird.x+7,bird.y-4,2,0,Math.PI*2);
  ctx.fill();

  ctx.fillStyle = "#f08030";
  ctx.beginPath();
  ctx.moveTo(bird.x+11,bird.y);
  ctx.lineTo(bird.x+23,bird.y+4);
  ctx.lineTo(bird.x+11,bird.y+7);
  ctx.fill();

  ctx.fillStyle = "#e8d58a";
  ctx.fillRect(0,490,360,30);
  ctx.fillStyle = "#53a83d";
  ctx.fillRect(0,490,360,7);

  ctx.fillStyle = "#fff";
  ctx.font = "bold 32px Arial";
  ctx.textAlign = "center";
  ctx.fillText(score,180,45);

  if (!started) {
    ctx.fillStyle = "#17324d";
    ctx.font = "bold 24px Arial";
    ctx.fillText("FLAPPY BIRD",180,210);
    ctx.font = "16px Arial";
    ctx.fillText("Chạm để bắt đầu!",180,245);
  } else if (!running) {
    ctx.fillStyle = "#17324d";
    ctx.font = "bold 25px Arial";
    ctx.fillText("GAME OVER",180,235);
    ctx.font = "16px Arial";
    ctx.fillText("Nhấn Chơi lại để thử lần nữa",180,265);
  }
}

function loop() {
  if (running) {
    frame++;
    bird.v += 0.32;
    bird.y += bird.v;

    if (frame % 95 === 0) {
      const top = 65 + Math.random()*235;
      pipes.push({x:360, top, passed:false});
    }

    for (const p of pipes) {
      p.x -= 2.5;

      if (!p.passed && p.x+52 < bird.x) {
        p.passed = true;
        score++;
      }

      if (
        bird.x+10 > p.x && bird.x-10 < p.x+52 &&
        (bird.y-10 < p.top || bird.y+10 > p.top+135)
      ) running = false;
    }

    pipes = pipes.filter(p => p.x > -60);

    if (bird.y > 477 || bird.y < 0) running = false;
  }

  draw();
  requestAnimationFrame(loop);
}

reset();
loop();
</script>
"""

components.html(game_html, height=610)
