const canvas = document.getElementById("canvas1");
const ctx = canvas.getContext('2d');
ctx.canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particlesArray;


let mouse = {
	x: null,
	y: null,
	radius: (canvas.height / 80) * (canvas.width / 80)
}

window.addEventListener('click',
	function(event){
		x = event.pageX;
		y = event.pageY;
		let directionX = Math.random() * 5 - 2.5;
		let directionY = Math.random() * 5 - 2.5;
		let size = 10;
		particlesArray.push(new Particle(x, y, directionX, directionY, size));
		particlesArray.splice(0, 1);
	}
)

class Particle {
	constructor(x, y, directionX, directionY, size){
		this.x = x;
		this.y = y;
		this.directionX = directionX;
		this.directionY = directionY;
		this.size = size;
	}

	draw(){
		ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, true);
        ctx.fillStyle = "#444";
        ctx.fill();
	}
	update(){
		if (this.x > canvas.width || this.x < 0){
			this.directionX = -this.directionX;
		}
		if (this.y > canvas.height || this.y < 0){
			this.directionY = -this.directionY;
		}

	this.x += this.directionX;
	this.y += this.directionY;
	this.draw();
	}
}

function init(){
	particlesArray = [];
	let numberOfParticles = (canvas.height * canvas.width) / 9000;
	for (let i = 0; i < numberOfParticles; i++){
		let size = 10;
		let x = Math.random() * innerWidth - size * 2 - size * 2;
		let y = Math.random() * innerHeight - size * 2 - size * 2;
		let directionX = Math.random() * 5 - 2.5;
		let directionY = Math.random() * 5 - 2.5;
		let color = '#FFF'
		particlesArray.push(new Particle(x, y, directionX, directionY, size, color));
	}
}

function animate(){
	requestAnimationFrame(animate);
	ctx.clearRect(0, 0, innerWidth, innerHeight);
	for (let i = 0; i < particlesArray.length; i++){
		particlesArray[i].update();
	}
	connect();
}

function connect() {
	for (let a = 0; a < particlesArray.length; a++){
		for (let b = a; b < particlesArray.length; b++){
			let distance = ((particlesArray[a].x - particlesArray[b].x) * (particlesArray[a].x - particlesArray[b].x))
			 + ((particlesArray[a].y - particlesArray[b].y) * (particlesArray[a].y - particlesArray[b].y));
			if (distance < (canvas.width / 7) * (canvas.height / 7)){
				let opacity = 1 - distance / ((canvas.width / 7) * (canvas.height / 7)); //lines will appear with transition
				ctx.strokeStyle = 'rgba(111, 111, 111, ' + opacity + ')'
				ctx.lineWidth = 5;
				ctx.beginPath();
				ctx.moveTo(particlesArray[a].x, particlesArray[a].y);
				ctx.lineTo(particlesArray[b].x, particlesArray[b].y);
				ctx.stroke();
			}
		}
	}
}

window.addEventListener('resize', 
	function(){
		canvas.width = innerWidth;
		canvas.height= innerHeight;
		mouse.radius = (canvas.height / 80) * (canvas.width / 80);
	}
)

window.addEventListener('mouseout',
	function() {
		mouse.x = undefined;
		mouse.y = undefined;
	}
)

init();
animate();