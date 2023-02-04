
function check(){ 
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    let init = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({ username, password }),
    }

    fetch('/connect', init)
    .then(response => response.json())
    .then(data => {
        //console.log(data); debug
        if (data.status === "success") {
            sessionStorage.setItem('sessionId', data.sessionId);
            cartsize();
        } else {
            sessionStorage.setItem('sessionId', '');
            alert(data.message);
            document.getElementById("cart-size").innerHTML = null;
            document.getElementById("login-info").innerHTML = null;
            document.getElementById("username").value = null;
            document.getElementById("password").value = null;
        }
    })
    .catch(error =>{
        console.log(error);
    });
}

function addtocart(id,cost,title) {
    const username = document.getElementById('username').value;
    const sessionId = sessionStorage.getItem('sessionId');
    const productId = id;
    const productCost= cost;
    const productTitle= title;

    let init = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({ username, productId, productCost, productTitle, sessionId}),
    }

    fetch('/addproduct', init)
    .then(response => response.json())
    .then(data => {
        //console.log(data); debug
        if (data.status === "success") {
            cartsize();
        } else {
            alert(data.message);
        }
    })
    .catch(error =>{
        console.log(error);
    });
}

function cartsize() {
    const username = document.getElementById('username').value;
    const sessionId = sessionStorage.getItem('sessionId');

    let init = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({ username, sessionId }),
    }
    
    fetch('/cartsize', init)
    .then(response => response.json())
    .then(data => {
        //console.log(data); debug
        if (data.status === "success") {
            document.getElementById("cart-size").innerHTML =  `Products in Cart 🛒: ${data.size} <br><br>
            <a href="cart.html?username=${username}&sessionId=${sessionId}">View Cart</a>`;
            document.getElementById("login-info").innerHTML = "Logged in as : " + data.username;
        } else {
            alert(data.message);
        }
    })
    .catch(error =>{
        console.log(error);
    });
}


