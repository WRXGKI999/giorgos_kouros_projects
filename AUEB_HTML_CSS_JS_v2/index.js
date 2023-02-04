const express = require('express')
const path = require('path')
const app = express()
const port = 8080
const uuid = require('uuid')
const xrhstes = [
    {username: 'manos', password: 'pwd1', sessionId: '', cart: []},
    {username: 'geo', password: 'pwd2', sessionId: '', cart: []}
];

app.listen(port)

app.use(express.static('public'))

app.use(express.urlencoded({ extended: false }))

app.use(express.json())

app.get('/', function(req, res){

    var options = {
        root: path.join(__dirname, 'public')
    }

    res.sendFile('index.html', options, function(err){
        console.log(err)
    })
})

app.post('/connect' , (req,res) => { // Login Service LS
    const {username, password} = req.body;
    let flag = false;

    for (let i = 0; i < xrhstes.length; i++) {
        if (username === xrhstes[i].username && password === xrhstes[i].password) {
            flag = true;
            sessionId = uuid.v4();
            xrhstes[i].sessionId = sessionId;
            //console.log(xrhstes[i]); debug
            res.status(200).json({username, sessionId, status: "success"});
        }
    }
    if (!flag){
        res.status(401).json({sessionId:"", message: "Wrong Credentials, please try again.", status: "error"});
    }
});

app.post('/addproduct', (req,res) => { // Cart Item Service CIS
    const {username, productId, productCost, productTitle, sessionId} = req.body;
    let flag = false;
    let cart = [];

    for (let i = 0; i < xrhstes.length; i++) {
        if (username === xrhstes[i].username && sessionId === xrhstes[i].sessionId) {
            flag = true;
            cart = xrhstes[i].cart;
            break;
        }
    }

    if (!flag) {
        res.status(401).json({message: "Please login in order to add products to your cart.", status: "error"});
        return;
    }

    let existingProduct = cart.find(item => item.productId === productId && item.Cost === Number(productCost) && item.Title === productTitle);

    if (existingProduct) {
        existingProduct.quantity++;
        //console.log(username + " cart is : "); debug
        //console.log(cart); debug
    } else {
        cart.push({productId, Cost: Number(productCost), Title: productTitle, quantity: 1});
        //console.log(username + " cart is : "); debug
        //console.log(cart); debug
    }

    res.status(200).json({message: "Product added to cart successfully.", status: "success"});

});

app.post('/cartsize', (req,res) => { //Cart Size Service CSS
    const {username, sessionId} = req.body;
    let flag = false;
    let cart = [];
    let size = 0;

    for (let i = 0; i < xrhstes.length; i++) {
        if (username === xrhstes[i].username && sessionId === xrhstes[i].sessionId) {
            flag = true;
            cart = xrhstes[i].cart;
            break;
        }
    }

    if (!flag) {
        res.status(401).json({message: "Please login in order to view your cart size.", status: "error"});
        return;
    }

    for (let i = 0; i < cart.length; i++) {
        size += cart[i].quantity;
    }
    res.status(200).json({username, size, status: "success"});
});

app.post('/totalcart', (req,res) =>{ //Cart Retrieval Service CRS
    const {username, sessionId} = req.body;
    let flag = false;
    let cart = [];
    let totalCost = 0;

    for (let i = 0; i < xrhstes.length; i++) {
        if (username === xrhstes[i].username && sessionId === xrhstes[i].sessionId) {
            flag = true;
            cart = xrhstes[i].cart;
            break;
        }
    }

    if (!flag) {
        res.status(401).json({message: "Please login in order to view your cart.", status: "error"});
        return;
    }

    cart.forEach(item => {
        totalCost += item.Cost * item.quantity;
    });
    let totalcart = Object.assign({}, { cart }, { totalCost }); // dimourgia enos antikeimenou totalcart oste na metatrapei se json gia ton pinaka tou kalathiou
    //console.log(totalcart); debug
    res.status(200).json({totalcart, status: "success"});
})