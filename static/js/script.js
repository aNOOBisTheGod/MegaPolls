const canvas = document.getElementById("canvas1");
const ctx = canvas.getContext("2d");
ctx.canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particlesArray; //array with all particles

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
  //class of floating particle on canvas
  constructor(x, y, directionX, directionY, size) {
    this.x = x;
    this.y = y;
    this.directionX = directionX;
    this.directionY = directionY;
    this.size = size;
  }

  draw() {
    //function that draws arr particles
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
    //function that move particles
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
  //initialization of array of floating particles
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
  //function that triggers every time
  //connects particles, clears everything from canvas and checks cursor position
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
  //function that connect all particles
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
  //if user resizes window, used for canvas not to be weird
  canvas.width = innerWidth;
  canvas.height = innerHeight;
});

function getThemeVal() {
  //getting value of theme from cookies
  allCookies = document.cookie.split("; ");
  for (let i = 0; i < allCookies.length; i++) {
    if (allCookies[i].includes("darkTheme")) {
      return parseInt(allCookies[i].split("=")[1]);
    }
  }
}
var themeVal = getThemeVal();
function changeTheme() {
  //changes theme(used in button press)
  themeVal = getThemeVal();
  iconButton = document.getElementById("changeThemeButton");
  if (themeVal != 0) {
    changeColorsSchemeWhite();
    if (iconButton != null) iconButton.innerHTML = '<i class="bi-moon" ></i>';
  } else {
    changeColorsSchemeBlack();
    if (iconButton != null) iconButton.innerHTML = '<i class="bi-sun" ></i>';
  }
}

function changeColorsSchemeWhite() {
  //changes color pallete to white
  document.cookie = "darkTheme=0";
  let all = document.getElementsByTagName("*");
  for (let i = 0; i < all.length; i++) {
    if (
      all[i].id != "clauseInput" &&
      all[i].id != "swal2-title" &&
      all[i].id != "swal2-html-container" &&
      !all[i].classList.contains('menuComponent') &&
      !all[i].classList.contains('menu') &&
      !all[i].classList.contains('swal2-icon-content')
    ) {
      all[i].style.color = "black";
    } else {
      all[i].style.color = "white";
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
  //changes color pallete to black
  document.cookie = "darkTheme=1";
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

isScrollVisisble = 0 //if scrollbar is visible then not 0
var theme = ''; //for theme to be typed from keyboard

window.addEventListener("scroll",function() {
  //appears scrollbar on scroll
  isScrollVisisble = 60
  var ss = document.styleSheets[0];
  ss.insertRule('::-webkit-scrollbar-thumb {background-color: rgba(125, 125, 125, 0.5);}', ss.rules.length);
})

window.addEventListener('mousemove', function(e){
  //appears scrollbar on scroll and moves particles
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
isMenu = false //if menu opened
pollInsert = false //if poll id insertion is opened 
pollId = '' //poll id text
function openPollPage(){
  //opens poll page
  pollId = '';
  var div = document.querySelector('.menu')
  div.innerHTML = 'Insert id of poll: <div class="idInsert"><a class="inputCursor">|</a><div>';
  pollInsert = true

}
var keys = {37: 1, 38: 1, 39: 1, 40: 1};
function preventDefault(e) {
  e.preventDefault();
}
function preventDefaultForScrollKeys(e) {
  if (keys[e.keyCode]) {
    preventDefault(e);
    return false;
  }
}
var supportsPassive = false;
try {
  window.addEventListener("test", null, Object.defineProperty({}, 'passive', {
    get: function () { supportsPassive = true; } 
  }));
} catch(e) {}
//to enableScroll
//functions that disable or enable scrolling effects. Used in menu
var wheelOpt = supportsPassive ? { passive: false } : false;
var wheelEvent = 'onwheel' in document.createElement('div') ? 'wheel' : 'mousewheel';

function disableScroll() {
  window.addEventListener('DOMMouseScroll', preventDefault, false);
  window.addEventListener(wheelEvent, preventDefault, wheelOpt);
  window.addEventListener('touchmove', preventDefault, wheelOpt);
  window.addEventListener('keydown', preventDefaultForScrollKeys, false);
}

function enableScroll() {
  window.removeEventListener('DOMMouseScroll', preventDefault, false);
  window.removeEventListener(wheelEvent, preventDefault, wheelOpt); 
  window.removeEventListener('touchmove', preventDefault, wheelOpt);
  window.removeEventListener('keydown', preventDefaultForScrollKeys, false);
}

var menuComponentsSelected = -1; //index of selected item in menu
function keyDown(e){
  //doin' manipulations with heys
  if (e.key == "Escape" || e == "Escape"){
    //triggers on escape
    if (!isMenu){
      //opens menu
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
    <div class='menuComponent'onclick=\"changeColorsSchemeWhite()\">Bright Theme</div>\
    ";
    div.setAttribute("class", "menu");
    var shadow = document.createElement("div");
    shadow.setAttribute("class", "shadow");
    shadow.setAttribute('onclick', 'keyDown("Escape")')
    this.document.body.appendChild(div);
    this.document.body.appendChild(shadow);
    isMenu = !isMenu
    document.body.classList.add('.no-scroll');
    disableScroll();
    pollInsert = false;
    }
    else {
      //closes menu
      document.querySelectorAll('.menu').forEach(e => e.remove());
      document.querySelectorAll('.shadow').forEach(e => e.remove());
      isMenu = !isMenu
      menuComponentsSelected = -1;
      document.body.classList.remove('.no-scroll');
      enableScroll();
    }
  }
  if (isMenu && e.key == 'ArrowDown'){
    //selection of menu components
    let menuComponents = document.querySelectorAll('.menuComponent');
    if (menuComponentsSelected < menuComponents.length - 1){
      menuComponentsSelected++
      menuComponents[menuComponentsSelected].style.cursor = 'pointer';
      menuComponents[menuComponentsSelected].style.background = 'rgb(125, 125, 125, 0.7)';
      if (menuComponentsSelected > 0){
      menuComponents[menuComponentsSelected - 1].style.cursor = 'default';
      menuComponents[menuComponentsSelected - 1].style.background = '#29292900'
      }
    }
  }
  if (isMenu && e.key == 'ArrowUp'){
    //selection of menu components
    let menuComponents = document.querySelectorAll('.menuComponent');
    if (menuComponentsSelected > 0){
      menuComponentsSelected--;
      menuComponents[menuComponentsSelected].style.cursor = 'pointer';
      menuComponents[menuComponentsSelected].style.background = 'rgb(125, 125, 125, 0.7)';
      menuComponents[menuComponentsSelected + 1].style.cursor = 'default';
      menuComponents[menuComponentsSelected + 1].style.background = '#29292900'
    }
  }
  if (pollInsert) {
    //if opened a tab where you need to insert poll id
    pollInsert = true;
    var div = document.querySelector('.idInsert');
    if (e.key.length == 1){
      pollId += e.key;
      div.innerHTML = pollId + '<a class="inputCursor">|</a>';
    } if (e.key == "Backspace"){
      pollId = pollId.slice(0, -1);
      div.innerHTML = pollId + '<a class="inputCursor">|</a>';
    } if (e.key == "Enter"){
      window.open('./poll?poll=' + pollId, "_self")
      pollInsert = false;
    }
    return
  }
  if (isMenu && e.key == 'Enter' && !pollInsert){
    //shows alert when used didn't select component and clicking on components using Enter
    try{
      let menuComponents = document.querySelectorAll('.menuComponent');
      menuComponents[menuComponentsSelected].click();
    return
    } catch(e){
      if (!e instanceof TypeError){
        throw e;
      } else {
        showAlert('info', 'Choose something or press Escape to exit menu.')
        return;
      }
    }
  } 
  theme += e.key;
  if (theme.includes('white')){
    changeColorsSchemeWhite();
    theme = '';
  } else if (theme.includes('black')) {
    changeColorsSchemeBlack();
    theme = '';
  }
  themeVal = getThemeVal();
}

window.addEventListener('keydown', (e) => keyDown(e)) //adding eventlistener to window


//calling animation functions
init();
animate();
