var joystick;
var changed = false;
function start()
{
	setInterval(readDistance, 300);
  joystick = createJoystick(document.getElementById('wrapper'));
  setInterval(moveLoop, 200);
}

function moveLoop(){
  if (changed){
    sendPosition();
    changed=false;
  }
}

function sendPosition(){
	var xhr = new XMLHttpRequest();
	xhr.open("POST", '/move', true);
	xhr.send(joystick.getPosition().x+","+joystick.getPosition().y);

}

function readDistance(){ 
	var txt = '';
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function(){
		if(xmlhttp.status == 200 && xmlhttp.readyState == 4){
			txt = xmlhttp.responseText;
			document.getElementById("distanta").innerHTML=parseInt(txt)+" cm";
			document.getElementById("slider").value=400-parseInt(txt);
		}
	};
xmlhttp.open("GET","/distanta",true);
xmlhttp.send();
}






function createJoystick(parent) {
  const maxDiff = 100;
  const stick = document.createElement('div');
  stick.classList.add('joystick');

  stick.addEventListener('mousedown', handleMouseDown);
  document.addEventListener('mousemove', handleMouseMove);
  document.addEventListener('mouseup', handleMouseUp);
  stick.addEventListener('touchstart', handleMouseDown);
  document.addEventListener('touchmove', handleMouseMove);
  document.addEventListener('touchend', handleMouseUp);

  let dragStart = null;
  let currentPos = { x: 0, y: 0 };

  function handleMouseDown(event) {
    stick.style.transition = '0s';
    if (event.changedTouches) {
      dragStart = {
        x: event.changedTouches[0].clientX,
        y: event.changedTouches[0].clientY,
      };
      return;
    }
    dragStart = {
      x: event.clientX,
      y: event.clientY,
    };
  }
  function handleMouseMove(event) {
    if (dragStart === null) {
      changed = false;
      return;
    }
    changed = true;
    event.preventDefault();
    if (event.changedTouches) {
      event.clientX = event.changedTouches[0].clientX;
      event.clientY = event.changedTouches[0].clientY;
    }
    const xDiff = event.clientX - dragStart.x;
    const yDiff = event.clientY - dragStart.y;
    const angle = Math.atan2(yDiff, xDiff);
		const distance = Math.min(maxDiff, Math.hypot(xDiff, yDiff));
		const xNew = distance * Math.cos(angle);
		const yNew = distance * Math.sin(angle);
	
	stick.style.transform = `translate3d(${xNew}px, ${yNew}px, 0px)`;
	var angle1=angle+Math.PI/2;
	stick.style.transform+= 'rotate('+angle1+'rad)';
	
    currentPos = { x: xNew/100, y: yNew/100 };
  }

  function handleMouseUp(event) {
    if (dragStart === null) return;
    stick.style.transition = '.2s';
    stick.style.transform = `translate3d(0px, 0px, 0px)`;
    dragStart = null;
    currentPos = { x: 0, y: 0 };
    sendPosition();
    changed=false;
  }

  parent.appendChild(stick);
  return {
    getPosition: () => currentPos,
  };
}
