const lang = Config[Config.lang];

const Cart = {
  items: [],
  cartEl: document.getElementById("cart"),
  totalEl: document.getElementById("total"),

  add(event){
    const button = event.target;
    const item = button.parentNode;

    // Check if the item is already in the cart
    var itemInCart = Cart.items.find(function(cartItem) {
      return cartItem.id === item.id;
    });

    if (itemInCart) {
        // If the item is already in the cart, update the quantity
        itemInCart.quantity += 1;
    } else {
      Cart.items.push({
        id: item.id,
        name: item.querySelector('h3').textContent,
        price: item.getAttribute('data-price'),
        quantity: 1
      });
    }
    Cart.updateCartDisplay();
  },

  remove(id){
      this.items = this.items.filter(item => item.id !== id);
      this.updateCartDisplay();
  },

  updateCartDisplay(){
    // Clear the cart element
    this.cartEl.innerHTML = "";

    // Loop through the items in the cart and add them to the cart element
    this.items.forEach(function(item) {
      var el = document.createElement("div");
      el.id = `item-${item.id}`;
      el.innerHTML = `${item.name}
      <input type='number' value='${item.quantity}' onchange='Cart.updateTotal()'>
      <span class='lineprice'>${Config.currency}${item.price * item.quantity}</span>
      <button onclick='Cart.remove("${item.id}")'>&times;</button>`;
      this.cartEl.appendChild(el);
    }.bind(this));
    this.updateTotal();
    CartData.save();
  },

  updateTotal(){
    // Calculate the new total price
    const totalPrice = this.items.reduce((total, item) => {
      const lineitem = document.getElementById('item-'+item.id);
      const input = lineitem.querySelector('input');
      const price = lineitem.querySelector('.lineprice');
      item.quantity = parseFloat(input.value);
      var linePrice = (item.quantity * item.price);
      price.innerText = `${Config.currency}${linePrice}`
      return total + linePrice;
    }, 0);
    // Update the total price element
    this.totalEl.innerText = `${lang.total}: ${Config.currency}${totalPrice}`;
  }
}

// saving and retrieving state of cart using localStorage
const CartData = {
  save(){
    const cartdata = JSON.stringify(Cart.items);
    localStorage.setItem("cart", cartdata);
  },
  load(){
    Cart.items = JSON.parse(localStorage.getItem("cart")) || [];
    Cart.updateCartDisplay();
  },
  clear(){
    localStorage.removeItem('cart');
  }
}

// loading prices from CSV and plugging them to pages
const PriceData = {
  load() {
      fetch(Config.product_csv)
          .then(response => response.text())
          .then(data => {
              var products = data.split("\n").slice(0, -1);
              products = products.map(function(product) {
                  return product.split(',');
              });
              PriceData.update(products);
          });
  },
  update(products) {
      // Update the DOM with the product prices
      products.forEach(function(product) {
          var productId = product[0];
          var productPrice = product[1];
          var product = document.getElementById(productId);
          product.setAttribute('data-price', productPrice);

          // create price and button elements
          var button = document.createElement('button');
          var pricep = document.createElement('p');
          pricep.innerHTML = `${lang.price}: ${Config.currency}${productPrice}`;
          button.innerHTML = lang.add;
          button.addEventListener('click', Cart.add);
          product.appendChild(pricep);
          product.appendChild(button);
      });
  }
}

function trans(){
  document.querySelectorAll('form h3,label,.t').forEach(t => {
    let slug = t.innerText.toLowerCase().replace(/\s+/g, '_');
    t.textContent = lang[slug];
  });
}

window.addEventListener("load", CartData.load);
window.addEventListener("load", trans);
