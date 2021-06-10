function slideMenuOut(){
	document.getElementById('side-menu').style.width = '250px';
	document.getElementById('content').style.paddingLeft = '280px';
	document.getElementById('side-menu').style.transition = '.5s ease';
}

function slideMenuIn(){
	document.getElementById('side-menu').style.width = '0px';
	document.getElementById('content').style.paddingLeft = '0px';
	document.getElementById('side-menu').style.transition = '.5s ease';	
}