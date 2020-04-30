function start()
{
	setInterval(readDistance, 200);
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