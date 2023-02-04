const urlParams = new URLSearchParams(window.location.search);
const username = urlParams.get('username');
const sessionId = urlParams.get('sessionId');

let init = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json'},
    body: JSON.stringify({ username, sessionId }),
};

fetch('/totalcart', init)
.then(response => response.json())
.then(data => {
    if (data.status === "success") {
        //console.log(data.totalcart); debug
        show_data(data.totalcart, "totalcart", "totalcart-menu");
        document.getElementById("login-info").innerHTML = "Logged in as : " + username;
    } else {
        alert(data.message);
    }
})
.catch(error =>{
    console.log(error);
});