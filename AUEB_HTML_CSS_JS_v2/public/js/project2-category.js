const url = new URL(window.location.href);
const id = url.searchParams.get("categoryId"); //apothikeuoume to id tis katigorias pou eimaste wste na fortonoume kathe fora ta sosta dedomena

function show_data(data, handlebar, show){ //geniki function gia emfanisi dedomenon sto html arxeio
    var source = document.getElementById(handlebar).innerHTML;
    var template = Handlebars.compile(source);
    var html = template(data);
    document.getElementById(show).innerHTML = html;
}
async function getData() { // bazoume async me await wste prota na fortothoun ta dedomena protou ektelestei otidipote allo sth selida
    try {
        const response_pr = await fetch('https://wiki-shop.onrender.com/categories/' + id + '/products');
        const pr_data = await response_pr.json();
        localStorage.setItem('pr_data', JSON.stringify(pr_data));
        show_data(pr_data, "products", "product-menu");
    } catch (error) {
        console.error('Error:', error);
    }

    try {
        const response_sub = await fetch('https://wiki-shop.onrender.com/categories/' + id + '/subcategories');
        const sub_data = await response_sub.json();
        show_data(sub_data, "filters", "filter-menu");
    } catch (error) {
        console.error('Error:', error);
    }
}

if (url.pathname === "/category.html") {
    getData();
} /* h arxiki fortosi twn dedomenwn stin selida, topotheteitai synthiki kathos xrisimopoioume 
to arxeio auto kai sto cart.html opote den theloume na ekteleitai se ekeino to arxeio*/


function filter(id){ // filtrarise analoga ti pataei o xristis sti forma
    var saved_pr_data = JSON.parse(localStorage.getItem('pr_data'));
    //console.log(saved_pr_data);
    var data = [];
    for (let i=0; i<saved_pr_data.length; i++){
        if (id == saved_pr_data[i].subcategory_id) {
            data.push(saved_pr_data[i]);
        }
    }
    //console.log(data); debug
    var source = document.getElementById("products").innerHTML;
    var template = Handlebars.compile(source);
    var html = template(data);
    document.getElementById("product-menu").innerHTML = html;
}

function filter_reset(){ //pata to all sta filters gia na ta emfanisei ola 
    var saved_pr_data = JSON.parse(localStorage.getItem('pr_data'));
    var source = document.getElementById("products").innerHTML;
    var template = Handlebars.compile(source);
    var html = template(saved_pr_data);
    document.getElementById("product-menu").innerHTML = html;
}

