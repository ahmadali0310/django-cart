updateButtons = Array.from(document.querySelectorAll(".update-cart"));
console.log(user);


const setQuantityInCart = (item, quantity) => {
  localStorage.setItem(item, quantity);
  document.getElementById("cart-total").textContent =
    localStorage.getItem(item);
    return;
};


(function () {
  if (user == "AnonymousUser") {
    localStorage.setItem["quantity"] = {};
  } else {
    axios({
      method: "GET",
      url: "/cart_quantity/",
    }).then((res) => {
      let quantity = JSON.parse(res.data);    
      setQuantityInCart("quantity", quantity.quantity);
    });
  }
})();




updateButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    productId = e.srcElement.getAttribute("data-id");
    action = e.srcElement.getAttribute("data-action");
    if (user == "AnonymousUser") {
      console.log("AnonymousUser");
    } else {
      let data = new FormData();
      data.append("productId", productId);
      data.append("action", action);
      userUpdateOrder(data);
    }
  });
});

const userUpdateOrder = (data) => {
  axios({
    method: "POST",
    url: "/update_cart/",
    headers: {
      contentType: "application/json",
      "X-CSRFToken": csrftoken,
    },
    data: data,
  }).then((res) => {
    let data = JSON.parse(res.data);
    if (data.quantity <= 0) {
      document.querySelector(`.item-${data.id}`).textContent = 0;
      document.querySelector(`.cart_item_${data.id}`).remove();
      document.querySelector(`.total_items_worth`).textContent =
        data.get_items_total;
      document.querySelector(`.total_items_quantity`).textContent =
        data.get_items_quantity;
      document.querySelector(
        `.total_items_worth`
      ).innerHTML = `Total: <strong>$${data.get_items_total}</strong>`;

      document.querySelector(
        `.total_items_quantity`
      ).innerHTML = `Items: <strong>${data.get_items_quantity}</strong>`;
      setQuantityInCart("quantity", data.get_items_quantity);


    } else {
      if (window.location.pathname == "/cart/") {
        console.log(`item-${data.id}`);
        document.querySelector(`.item-${data.id}`).textContent = data.quantity;
        document.querySelector(`.product_total_${data.id}`).textContent =
          data.get_product_total;
        document.querySelector(
          `.total_items_worth`
        ).innerHTML = `Total: <strong>$${data.get_items_total}</strong>`;

        document.querySelector(
          `.total_items_quantity`
        ).innerHTML = `Items: <strong>${data.get_items_quantity}</strong>`;
          setQuantityInCart("quantity", data.get_items_quantity);
      }
          setQuantityInCart("quantity", data.get_items_quantity);

    }
  });
};
