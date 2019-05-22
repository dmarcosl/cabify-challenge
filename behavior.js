/**
 * Retrieve the products
 */
function loadProducts() {

    // Create a request
    var http_request = new XMLHttpRequest();

    // Function to handle the output
    http_request.onreadystatechange = function () {

        if (http_request.readyState === 4 && http_request.status === 200) {
            // Parse the json data
            const jsonObj = JSON.parse(http_request.responseText);

            jsonObj.forEach(product => {
                // Get the product list and create a structure to add each product to the basket
                const ul = document.querySelectorAll('div.product-list ul')[0];
                const li = document.createElement("li");
                const div = document.createElement("div");
                div.appendChild(document.createTextNode(product.name));

                const p = document.createElement("p");
                p.appendChild(document.createTextNode(product.price + '€'));
                div.appendChild(p);

                const buttonDiv = document.createElement("div");

                const plusButton = document.createElement('input');
                plusButton.setAttribute('type', 'button');
                plusButton.setAttribute('value', 'Add 1 unit');
                plusButton.onclick = function () {
                    addProduct(product.code, 1)
                };
                buttonDiv.appendChild(plusButton);

                const minusButton = document.createElement('input');
                minusButton.setAttribute('type', 'button');
                minusButton.setAttribute('value', 'Remove 1 unit');
                minusButton.onclick = function () {
                    addProduct(product.code, -1)
                };
                buttonDiv.appendChild(minusButton);

                div.appendChild(buttonDiv);
                li.appendChild(div);
                ul.appendChild(li);
            });
        }
    };

    // Send the request
    http_request.open("GET", "http://127.0.0.1:5000/shop/products", true);
    http_request.send();
}

/**
 * Create a new basket
 */
function createBasket() {

    var http_request = new XMLHttpRequest();
    http_request.onreadystatechange = function () {

        if (http_request.readyState === 4 && http_request.status === 200) {
            // Parse the basket id and set it in the hidden input
            const basketId = JSON.parse(http_request.responseText).basket_id;
            document.getElementsByName("basket-id")[0].value = basketId;

            // Change the basket button text and onclick
            const button = document.getElementsByName("basket-button")[0];
            button.value = "Delete basket";
            button.onclick = deleteBasket;
        }
    };

    http_request.open("POST", "http://127.0.0.1:5000/shop/create-basket", true);
    http_request.send();
}

/**
 * Remove the current basket
 */
function deleteBasket() {

    var basketId = document.getElementsByName("basket-id")[0].value;

    if (!basketId) {
        alert('You have to create a basket in order to delete it.');
        return;
    }

    const http_request = new XMLHttpRequest();
    http_request.onreadystatechange = function () {

        if (http_request.readyState === 4 && http_request.status === 200) {
            // Remove the basket id from the hidden input
            document.getElementsByName("basket-id")[0].value = null;

            // Empty the basket list
            document.querySelectorAll('div.basket ul')[0].innerHTML = "";

            // Empty the checkout price
            document.getElementById("price").innerHTML = "";

            // Change the basket button text and onclick
            const button = document.getElementsByName("basket-button")[0];
            button.value = "Create basket";
            button.onclick = createBasket;
        } else if (http_request.readyState === 4 && http_request.status === 400) {
            const jsonObj = JSON.parse(http_request.responseText);
            if (jsonObj.msg) {
                alert(jsonObj.msg);
            }
        }
    };

    http_request.open("DELETE", "http://127.0.0.1:5000/shop/" + basketId, true);
    http_request.send();
}

/**
 * Add a product to the basket
 *
 * @param code Code of the product
 * @param units Number of units of the product
 */
function addProduct(code, units) {

    var basketId = document.getElementsByName("basket-id")[0].value;

    if (!basketId) {
        alert('You have to create a basket in order to add a product.');
        return;
    }

    var http_request = new XMLHttpRequest();
    http_request.onreadystatechange = function () {

        if (http_request.readyState === 4 && http_request.status === 200) {
            const jsonObj = JSON.parse(http_request.responseText);

            // Empty the basket list
            const ul = document.querySelectorAll('div.basket ul')[0];
            ul.innerHTML = "";

            for (var prop in jsonObj) {
                const li = document.createElement("li");
                li.appendChild(document.createTextNode(prop + ' (' + jsonObj[prop] + ')'));
                ul.appendChild(li);
            }
            checkout();
        } else if (http_request.readyState === 4 && http_request.status === 400) {
            const jsonObj = JSON.parse(http_request.responseText);
            if (jsonObj.msg) {
                alert(jsonObj.msg);
            }
        }
    };

    http_request.open("PUT", "http://127.0.0.1:5000/shop/" + basketId + "/update-product?product_code=" + code + '&quantity=' + units, true);
    http_request.send();
}

/**
 * Calculate the price of the products of the basket applying discounts
 */
function checkout() {

    var basketId = document.getElementsByName("basket-id")[0].value;

    if (!basketId) {
        alert('You have to create a basket in order to checkout.');
        return;
    }

    var http_request = new XMLHttpRequest();
    http_request.onreadystatechange = function () {

        if (http_request.readyState === 4 && http_request.status === 200) {
            // Parse the price and set it in the div
            const price = JSON.parse(http_request.responseText).price;
            const priceDiv = document.getElementById("price");
            priceDiv.innerHTML = "";
            priceDiv.appendChild(document.createTextNode(price + '€'));

        } else if (http_request.readyState === 4 && http_request.status === 400) {
            const jsonObj = JSON.parse(http_request.responseText);
            if (jsonObj.msg) {
                alert(jsonObj.msg);
            }
        }
    };

    http_request.open("GET", "http://127.0.0.1:5000/shop/" + basketId + "/checkout", true);
    http_request.send();
}

window.onload = loadProducts;
