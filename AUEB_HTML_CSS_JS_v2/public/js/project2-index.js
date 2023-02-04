
async function categories(){
        const response = await fetch('https://wiki-shop.onrender.com/categories');
        const data = await response.json();
        var source = document.getElementById("categories").innerHTML;
        var template = Handlebars.compile(source);
        var html = template(data);
        document.getElementById("category-menu").innerHTML = html;
    }
categories();



