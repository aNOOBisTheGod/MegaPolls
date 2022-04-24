const canvas = document.getElementById("canvas1");
const ctx = canvas.getContext("2d");
ctx.canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particlesArray;

let mouse = {
  x: null,
  y: null,
  radius: (canvas.height / 80) * (canvas.width / 80),
};

// window.addEventListener('click',
// 	function(event){
// 		x = event.pageX;
// 		y = event.pageY;
// 		let directionX = Math.random() * 5 - 2.5;
// 		let directionY = Math.random() * 5 - 2.5;
// 		let size = 10;
// 		particlesArray.push(new Particle(x, y, directionX, directionY, size));
// 		particlesArray.splice(0, 1);
// 	}
// )

class Particle {
  constructor(x, y, directionX, directionY, size) {
    this.x = x;
    this.y = y;
    this.directionX = directionX;
    this.directionY = directionY;
    this.size = size;
  }

  draw() {
    ctx.save();
    ctx.beginPath();
    // if (themeVal != 1) {
    //   ctx.shadowColor = "#000";
    // } else {
    //   ctx.shadowColor = "#f3214f";
    // }

    // ctx.shadowOffsetX = 0;
    // ctx.shadowOffsetY = 0;
    // ctx.shadowBlur = 100;
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, true);
    ctx.fillStyle = "#444";
    ctx.fill();
    ctx.restore();
  }
  update() {
    if (this.x > canvas.width + 200 || this.x < -200) {
      this.directionX = -this.directionX;
    }
    if (this.y > canvas.height + 200 || this.y < -200) {
      this.directionY = -this.directionY;
    }

    this.x += this.directionX;
    this.y += this.directionY;
    this.draw();
  }
}

function init() {
  particlesArray = [];
  let numberOfParticles = (canvas.height * canvas.width) / 9000;
  for (let i = 0; i < numberOfParticles; i++) {
    let size = 1;
    let x = Math.random() * innerWidth - size * 2 - size * 2;
    let y = Math.random() * innerHeight - size * 2 - size * 2;
    let directionX = Math.random() * 2 - 1;
    let directionY = Math.random() * 2 - 1;
    let color = "#FFF";
    particlesArray.push(
      new Particle(x, y, directionX, directionY, size, color)
    );
  }
}

function animate() {
  requestAnimationFrame(animate);
  var ss = document.styleSheets[0];
  if (isScrollVisisble > 0){
    isScrollVisisble -= 1
  } else {
    ss.insertRule('::-webkit-scrollbar-thumb {background-color: transparent}', ss.rules.length)
  }
  ctx.clearRect(0, 0, innerWidth, innerHeight);
  for (let i = 0; i < particlesArray.length; i++) {
    particlesArray[i].update();
  }
  connect();
}

function connect() {
  for (let a = 0; a < particlesArray.length; a++) {
    for (let b = a; b < particlesArray.length; b++) {
      let distance =
        (particlesArray[a].x - particlesArray[b].x) *
          (particlesArray[a].x - particlesArray[b].x) +
        (particlesArray[a].y - particlesArray[b].y) *
          (particlesArray[a].y - particlesArray[b].y);
      if (distance < (canvas.width / 7) * (canvas.height / 7)) {
        let opacity = 1 - distance / ((canvas.width / 7) * (canvas.height / 7)); //lines will appear with opacity
        ctx.strokeStyle = "rgba(111, 111, 111, " + opacity + ")";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
        ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
        ctx.stroke();
      }
    }
  }
}

window.addEventListener("resize", function () {
  canvas.width = innerWidth;
  canvas.height = innerHeight;
  mouse.radius = (canvas.height / 80) * (canvas.width / 80);
});

window.addEventListener("mouseout", function () {
  mouse.x = undefined;
  mouse.y = undefined;
});

function getThemeVal() {
  allCookies = document.cookie.split("; ");
  for (let i = 0; i < allCookies.length; i++) {
    if (allCookies[i].includes("darkTheme")) {
      return parseInt(allCookies[i].split("=")[1]);
    }
  }
}
var themeVal = getThemeVal();
function changeTheme() {
  themeVal = getThemeVal();
  if (themeVal != 1) {
    document.cookie = "darkTheme=1";
  } else {
    document.cookie = "darkTheme=0";
  }
  iconButton = document.getElementById("changeThemeButton");
  if (themeVal != 1) {
    changeColorsSchemeWhite();
    if (iconButton != null) iconButton.innerHTML = '<i class="bi-moon" ></i>';
  } else {
    changeColorsSchemeBlack();
    if (iconButton != null) iconButton.innerHTML = '<i class="bi-sun" ></i>';
  }
}

function changeColorsSchemeWhite() {
  let all = document.getElementsByTagName("*");
  for (let i = 0; i < all.length; i++) {
    if (
      all[i].id != "clauseInput" &&
      all[i].id != "swal2-title" &&
      all[i].id != "swal2-html-container"
    ) {
      all[i].style.color = "black";
    }
  }
  let canvas = document.getElementById("canvas1");
  canvas.style.background = "white";
  let allButtons = document.getElementsByClassName("simple-button");
  for (let i = 0; i < allButtons.length; i++) {
    allButtons[i].style.background = "#a3a3a3af";
  }
  let allInputs = document.getElementsByTagName("input");
  for (let i = 0; i < allInputs.length; i++) {
    if (allInputs[i].id != "clauseInput") {
      allInputs[i].style.color = "black";
      allInputs[i].style.background = "white";
    }
  }
  let allBlurs = document.getElementsByClassName("text-blur-wrapper");
  for (let i = 0; i < allBlurs.length; i++) {
      allBlurs[i].style.boxShadow = "0px 0px 100px 0px #0000002b";
      allBlurs[i].style.background = "#9c9b9bb4";
  }
}
function changeColorsSchemeBlack() {
  let all = document.getElementsByTagName("*");
  for (let i = 0; i < all.length; i++) {
    all[i].style.color = "white";
  }
  let canvas = document.getElementById("canvas1");
  canvas.style.background = "black";
  let allButtons = document.getElementsByClassName("simple-button");
  for (let i = 0; i < allButtons.length; i++) {
    allButtons[i].style.background = "#707070af";
  }
  let allInputs = document.getElementsByTagName("input");
  for (let i = 0; i < allInputs.length; i++) {
    if (allInputs[i].id != "clauseInput") {
      allInputs[i].style.color = "white";
      allInputs[i].style.background = "black";
    }
  }
  let allBlurs = document.getElementsByClassName("text-blur-wrapper");
  for (let i = 0; i < allBlurs.length; i++) {
    allBlurs[i].style.boxShadow = "0px 0px 100px 0px #FFFFFF2b";
    allBlurs[i].style.background = "#292929b4";
  }
}
if (themeVal != 1) {
  changeColorsSchemeWhite();
}

isScrollVisisble = 0

window.addEventListener("scroll",function() {
  isScrollVisisble = 60
  var ss = document.styleSheets[0];
  ss.insertRule('::-webkit-scrollbar-thumb {background-color: rgba(125, 125, 125, 0.5);}', ss.rules.length);
})

window.addEventListener('mousemove', function(e){
  if (window.innerWidth - e.x <= 100){
    isScrollVisisble = 60;
    var ss = document.styleSheets[0];
    ss.insertRule('::-webkit-scrollbar-thumb {background-color: rgba(125, 125, 125, 0.5);}', ss.rules.length);
  }
  for (let i = 0; i < particlesArray.length; i++){
    particlesArray[i].x += Math.random() * e.movementX / 100;
    particlesArray[i].y += Math.random() * e.movementY / 100;
  }
})
theme = ''
isMenu = false
pollInsert = false
pollId = ''
function openPollPage(){
  pollId = '';
  var div = document.querySelector('.menu')
  div.innerHTML = 'Insert id of poll: <div class="idInsert"><a class="inputCursor">|</a><div>';
  pollInsert = true

}

function keyDown(e){
  if (e.key == "Escape"){
    if (!isMenu){
    var div = document.createElement("div");
    div.innerHTML = "\
    Choose Page\
    <div class='menuComponent' onclick=\"location.href='./';\">Main Page</div>\
    <div class='menuComponent' onclick=\"location.href='./account';\">Account Page</div>\
    <div class='menuComponent' onclick=\"location.href='./create_account';\">Create Account Page</div>\
    <div class='menuComponent' onclick=\"location.href='./create_poll';\">Create Poll Page</div>\
    <div class='menuComponent' onclick=\"openPollPage()\">Poll Page</div>\
    Choose Theme\
    <div class='menuComponent'onclick=\"changeColorsSchemeBlack();\">Dark Theme</div>\
    <div class='menuComponent'onclick=\"changeColorsSchemeWhite()\">White Theme</div>\
    ";
    div.setAttribute("class", "menu");
    var shadow = document.createElement("div");
    shadow.setAttribute("class", "shadow");
    this.document.body.appendChild(div);
    this.document.body.appendChild(shadow);
    isMenu = !isMenu
    }
    else {
      document.querySelectorAll('.menu').forEach(e => e.remove());
      document.querySelectorAll('.shadow').forEach(e => e.remove());
      isMenu = !isMenu
    }
  }
  if (pollInsert) {
    var div = document.querySelector('.idInsert');
    if (e.key.length == 1){
      pollId += e.key;
      div.innerHTML = pollId + '<a class="inputCursor">|</a>';
    } if (e.key == "Backspace"){
      console.log('slice')
      pollId = pollId.slice(0, -1);
      div.innerHTML = pollId + '<a class="inputCursor">|</a>';
    } if (e.key == "Enter"){
      window.open('./poll?poll=' + pollId, "_self")
    }
    return
  } 
  theme += e.key;
  if (theme.includes('white')){
    changeColorsSchemeWhite();
    theme = '';
  } else if (theme.includes('black')) {
    changeColorsSchemeBlack();
    theme = '';
  }
}

window.addEventListener('keydown', (e) => keyDown(e))



changeTheme();
changeTheme();
init();
animate();
