console.clear();

const loginBtn = document.getElementById("login");
const signupBtn = document.getElementById("signup");

loginBtn.addEventListener("click", (e) => {
	let parent = e.target.parentNode.parentNode;
	Array.from(e.target.parentNode.parentNode.classList).find((element) => {
		if (element !== "slide-up") {
			parent.classList.add("slide-up");
		} else {
			signupBtn.parentNode.classList.add("slide-up");
			parent.classList.remove("slide-up");
		}
	});
});

signupBtn.addEventListener("click", (e) => {
	let parent = e.target.parentNode;
	Array.from(e.target.parentNode.classList).find((element) => {
		if (element !== "slide-up") {
			parent.classList.add("slide-up");
		} else {
			loginBtn.parentNode.parentNode.classList.add("slide-up");
			parent.classList.remove("slide-up");
		}
	});
});

document.getElementById('sign').onclick = function() {
	var frm1 =document.getElementById('form') || null;
	if(frm1){
		frm1.action = '/sign'
	}
	
	
}

document.getElementById('login').onclick = function() {
	var frm1 =document.getElementById('form') || null;
	if(frm1){
		frm1.action = '/login'
	}
	
}




// var frm1 = document.getElementById('form') || null;
// if(frm) {
//    frm.action = '/login' 
// }

