
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flappy Bird Family",
    page_icon="🐤",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(#72d9ef, #f0fff0);
}
header, footer, #MainMenu {
    visibility: hidden;
}
.block-container {
    max-width: 650px;
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🐤 Flappy Bird Family")
st.caption("Chọn chim • Chạm để bay • Né ống • Lập kỷ lục")

components.html(r"""
<div style="max-width:480px;margin:auto;font-family:Arial,sans-serif">
<canvas id="game" width="420" height="650"
style="width:100%;display:block;border:4px solid white;
border-radius:18px;box-shadow:0 8px 24px #286b8b55;
touch-action:manipulation"></canvas>
<div style="display:flex;gap:8px;margin-top:12px">
<button id="menuBtn">🏠 MENU</button>
<button id="soundBtn">🔊 ÂM THANH</button>
</div>
<style>
button {
 flex:1;padding:12px 5px;border:3px solid white;
 border-radius:12px;background:#68c83c;color:white;
 font-weight:900;font-size:14px;box-shadow:0 3px #43862d;
}
</style>
</div>
<script>
(()=>{
const c=document.getElementById('game');
const ctx=c.getContext('2d');
const W=420,H=650,G=570;
let state='menu',color=0,bird,pipes,particles,score,best=0,frame=0;
let sound=true,audio=null;
try{best=+(localStorage.getItem('flappyFamilyBest')||0)}catch(e){}
function init(){
 bird={x:105,y:280,vy:0,rot:0};
 pipes=[];particles=[];score=0;frame=0;
}
init();
function tone(f,d=.12,type='sine',v=.035,delay=0){
 if(!sound)return;
 try{
 if(!audio)audio=new(window.AudioContext||window.webkitAudioContext)();
 audio.resume();
 const o=audio.createOscillator(),g=audio.createGain();
 o.type=type;o.frequency.value=f;
 g.gain.setValueAtTime(v,audio.currentTime+delay);
 g.gain.exponentialRampToValueAtTime(.001,audio.currentTime+delay+d);
 o.connect(g);g.connect(audio.destination);
 o.start(audio.currentTime+delay);o.stop(audio.currentTime+delay+d);
 }catch(e){}
}
function flapSound(){
 tone(520,.08,'triangle');tone(760,.09,'sine',.025,.04);
}
function loseSound(){
 tone(330,.2,'sawtooth',.04);
 tone(240,.25,'triangle',.045,.18);
 tone(150,.45,'triangle',.05,.4);
}
function start(){
 init();state='play';bird.vy=-6;flapSound();
}
function flap(){
 if(state==='menu'){start();return}
 if(state==='over'){start();return}
 bird.vy=-6.7;flapSound();
 for(let i=0;i<5;i++)particles.push({
 x:bird.x-12,y:bird.y,vx:-Math.random()*2-1,
 vy:Math.random()*2-1,life:20
 });
}
function end(){
 if(state!=='play')return;
 state='over';loseSound();
 if(score>best){
 best=score;
 try{localStorage.setItem('flappyFamilyBest',best)}catch(e){}
 }
}
c.addEventListener('pointerdown',e=>{
 e.preventDefault();
 const r=c.getBoundingClientRect();
 const px=(e.clientX-r.left)*W/r.width;
 const py=(e.clientY-r.top)*H/r.height;
 if(state==='menu'){
  if(py>360&&py<450){color=px<W/2?0:1;return}
  if(py>460&&py<560){start();return}
  start();return;
 }
 if(state==='over'){start();return}
 flap();
},{passive:false});
document.addEventListener('keydown',e=>{
 if(e.code==='Space'||e.code==='ArrowUp'){
  e.preventDefault();
  if(state!=='play')start();else flap();
 }
});
document.getElementById('menuBtn').onclick=()=>state='menu';
document.getElementById('soundBtn').onclick=()=>{
 sound=!sound;
 document.getElementById('soundBtn').textContent=sound?'🔊 ÂM THANH':'🔇 TẮT TIẾNG';
 if(sound)tone(600,.1);
};
function rr(x,y,w,h,r,col){
 ctx.fillStyle=col;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill();
}
function bg(){
 let g=ctx.createLinearGradient(0,0,0,H);
 g.addColorStop(0,'#51c8e9');g.addColorStop(.72,'#d8f7ef');
 g.addColorStop(1,'#fff0c1');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 // Sun
 ctx.fillStyle='#fff4a7';ctx.beginPath();ctx.arc(340,80,32,0,7);ctx.fill();
 // Clouds
 for(let i=0;i<5;i++){
  let xx=((i*120-frame*.2)%(W+100)+W+100)%(W+100)-40;
  ctx.fillStyle='#ffffffb8';ctx.beginPath();
  ctx.arc(xx,125+i%3*65,18,0,7);
  ctx.arc(xx+20,113+i%3*65,23,0,7);
  ctx.arc(xx+44,126+i%3*65,17,0,7);ctx.fill();
 }
 // City skyline
 for(let i=0;i<12;i++){
  let xx=i*40-(frame*.28%40),hh=65+(i*23%90);
  rr(xx,G-85-hh,34,hh+85,2,i%2?'#9edfc4':'#b5e9d2');
  for(let j=0;j<3;j++)rr(xx+7,G-70-hh+j*19,5,6,1,'#e5f9d9');
 }
 // Bushes
 ctx.fillStyle='#7bdc62';ctx.beginPath();ctx.moveTo(0,510);
 for(let xx=0;xx<=W;xx+=8)
  ctx.lineTo(xx,500+Math.sin(xx*.045+frame*.025)*9);
 ctx.lineTo(W,G);ctx.lineTo(0,G);ctx.fill();
 ctx.fillStyle='#37b94a';ctx.beginPath();ctx.moveTo(0,530);
 for(let xx=0;xx<=W;xx+=8)
  ctx.lineTo(xx,520+Math.sin(xx*.065+frame*.02)*6);
 ctx.lineTo(W,G);ctx.lineTo(0,G);ctx.fill();
 // Ground
 rr(0,G,W,H-G,0,'#ead38a');
 rr(0,G,W,8,0,'#6cce43');
 for(let i=-1;i<15;i++)
  rr(i*32-(frame*2%32),G+12,28,24,3,'#9bdd48');
}
function drawPipe(p){
 const pw=58,gap=160;
 function section(y,h,capY){
  let g=ctx.createLinearGradient(p.x,0,p.x+pw,0);
  g.addColorStop(0,'#35a923');g.addColorStop(.28,'#a0f44b');
  g.addColorStop(.55,'#65d330');g.addColorStop(1,'#26851f');
  rr(p.x,y,pw,h,1,g);
  ctx.strokeStyle='#205a20';ctx.lineWidth=4;
  ctx.strokeRect(p.x+1,y+1,pw-2,Math.max(1,h-2));
  rr(p.x+9,y+4,7,Math.max(0,h-8),1,'#b5ff6c');
  rr(p.x-5,capY,pw+10,22,3,'#78e33a');
  ctx.strokeStyle='#205a20';ctx.lineWidth=4;
  ctx.strokeRect(p.x-4,capY+1,pw+8,20);
  rr(p.x+5,capY+3,7,15,1,'#b5ff6c');
 }
 section(0,p.top,p.top-22);
 section(p.top+gap,G-p.top-gap,p.top+gap);
}
function drawBird(){
 ctx.save();ctx.translate(bird.x,bird.y);ctx.rotate(bird.rot);
 ctx.shadowColor=color?'#ff71bb':'#ffdd55';ctx.shadowBlur=14;
 const body=color?'#ff8dbf':'#ffe05a';
 const wing=color?'#e94e91':'#f4a22b';
 // Tail
 ctx.fillStyle=wing;ctx.beginPath();
 ctx.moveTo(-12,0);ctx.lineTo(-24,-8);ctx.lineTo(-22,7);ctx.fill();
 // Body
 ctx.fillStyle=body;ctx.beginPath();
 ctx.ellipse(0,0,18,14,0,0,7);ctx.fill();
 ctx.shadowBlur=0;ctx.lineWidth=2.5;ctx.strokeStyle='#493c36';ctx.stroke();
 // Flapping wing
 ctx.fillStyle=wing;ctx.beginPath();
 ctx.ellipse(-5,Math.sin(frame*.45)*5,10,7,-.25,0,7);
 ctx.fill();ctx.stroke();
 // Eye
 ctx.fillStyle='white';ctx.beginPath();
 ctx.ellipse(8,-6,6,7,0,0,7);ctx.fill();ctx.stroke();
 ctx.fillStyle='#222';ctx.beginPath();ctx.arc(10,-5,2.4,0,7);ctx.fill();
 // Beak
 ctx.fillStyle='#ff713c';ctx.beginPath();
 ctx.moveTo(12,0);ctx.lineTo(25,4);ctx.lineTo(12,7);ctx.closePath();
 ctx.fill();ctx.stroke();
 ctx.restore();
}
function text(t,y,size,col='#fff'){
 ctx.font='900 '+size+'px Arial';
 ctx.textAlign='center';
 ctx.lineWidth=5;ctx.strokeStyle='#3d624d';
 ctx.strokeText(t,W/2,y);
 ctx.fillStyle=col;ctx.fillText(t,W/2,y);
}
function button(x,y,w,h,label){
 rr(x,y,w,h,12,'#66c934');
 ctx.strokeStyle='#fff';ctx.lineWidth=4;ctx.strokeRect(x+2,y+2,w-4,h-4);
 ctx.fillStyle='#fff';ctx.font='bold 18px Arial';ctx.textAlign='center';
 ctx.fillText(label,x+w/2,y+h/2+6);
}
function overlay(){
 ctx.fillStyle='#14394d66';ctx.fillRect(0,0,W,H);
 rr(30,135,W-60,355,22,'#fff8db');
 if(state==='menu'){
  ctx.textAlign='center';ctx.fillStyle='#ffcf43';
  ctx.font='900 37px Arial';ctx.strokeStyle='#6a5934';ctx.lineWidth=5;
  ctx.strokeText('FLAPPY BIRD',W/2,205);
  ctx.fillText('FLAPPY BIRD',W/2,205);
  ctx.fillStyle='#548d46';ctx.font='bold 21px Arial';
  ctx.fillText('FAMILY',W/2,240);
  ctx.fillStyle='#4a6570';ctx.font='bold 15px Arial';
  ctx.fillText('CHỌN NHÂN VẬT',W/2,305);
  button(50,325,145,92,'🐤 VÀNG');
  button(225,325,145,92,'🐦 HỒNG');
  button(70,445,280,55,'▶  BẮT ĐẦU');
  ctx.fillStyle='#537c75';ctx.font='13px Arial';
  ctx.fillText('Chạm màn hình hoặc nhấn SPACE',W/2,525);
 }else{
  text('GAME OVER',225,34,'#ffcf43');
  ctx.fillStyle='#4b6570';ctx.font='bold 20px Arial';
  ctx.fillText('Điểm: '+score,W/2,290);
  ctx.fillText('Kỷ lục: '+best,W/2,325);
  button(70,370,280,60,'↻  CHƠI LẠI');
  ctx.font='14px Arial';ctx.fillStyle='#537c75';
  ctx.fillText('Chạm để chơi lại',W/2,465);
 }
}
function loop(){
 requestAnimationFrame(loop);
 frame++;
 bg();
 if(state==='play'){
  bird.vy+=.31;bird.y+=bird.vy;
  bird.rot=clamp(bird.vy*.06,-.55,1.15);
  if(frame%92===0)pipes.push({
   x:W,top:65+Math.random()*220,passed:false
  });
  for(const p of pipes){
   p.x-=2.5;
   const gap=160;
   if(!p.passed&&p.x+58<bird.x){
    p.passed=true;score++;tone(880,.13,'sine',.035);
   }
   if(bird.x+12>p.x&&bird.x-12<p.x+58&&
      (bird.y-11<p.top||bird.y+11>p.top+gap))end();
  }
  pipes=pipes.filter(p=>p.x>-70);
  if(bird.y>G-13||bird.y<0)end();
  for(const p of particles){
   p.x+=p.vx;p.y+=p.vy;p.life--;
   ctx.globalAlpha=Math.max(0,p.life/20);
   rr(p.x,p.y,4,4,2,'#fff7ad');
  }
  ctx.globalAlpha=1;particles=particles.filter(p=>p.life>0);
 }
 for(const p of pipes)drawPipe(p);
 drawBird();
 if(state==='play'){
  ctx.textAlign='center';ctx.font='900 36px Arial';
  ctx.lineWidth=4;ctx.strokeStyle='#36774d';
  ctx.strokeText(score,W/2,58);
  ctx.fillStyle='white';ctx.fillText(score,W/2,58);
  ctx.textAlign='left';ctx.font='bold 14px Arial';
  ctx.fillStyle='#285c48';ctx.fillText('BEST '+best,12,27);
 }
 if(state==='menu'||state==='over')overlay();
}
loop();
})();
</script>
""", height=790, scrolling=False)
