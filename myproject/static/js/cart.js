document.addEventListener("DOMContentLoaded", function () {
  // Event delegation for dynamically added elements

  // Añadir items al carrito
  document.body.addEventListener("click", function (event) {
    if (event.target.closest("#add-to-cart-button")) {
      event.preventDefault();
      const button = event.target.closest("#add-to-cart-button");
      addToCart(button);
    }
  });

  // Borrar items desde la tabla del carrito
  document.body.addEventListener("click", function (event) {
    if (event.target.closest(".delete-item-button")) {
      event.preventDefault();
      const button = event.target.closest(".delete-item-button");
      deleteCartItem(button);
    }
  });

  // Cambios en el input desde la table
  document.body.addEventListener("input", function (event) {
    if (event.target.classList.contains("cart-item-quantity-input")) {
      const input = event.target;
      updateCartItemQuantity(input);
    }
  });

  // Function to format currency
  function currencyFormatter(amount) {
    try {
      if (isNaN(amount) || amount === null) {
        throw new Error("Invalid number");
      }
      return (
        "$" +
        parseFloat(amount).toLocaleString("en-US", {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        })
      );
    } catch (error) {
      return "- -";
    }
  }

  // Function to add an item to the cart
  function addToCart(button) {
    const productId = button.getAttribute("data-product-id");
    const productName = button.getAttribute("data-product-name");
    const productPrice = parseFloat(button.getAttribute("data-product-price"));
    const quantityInput = document.getElementById("unit_numbers");
    let quantity = parseInt(quantityInput.value);

    if (quantity <= 0 || isNaN(quantity)) {
      alert("Por favor, ingresa una cantidad válida.");
      return;
    }

    // Si existe...
    let existingRow = document.querySelector(`#cart-item-${productId}`);
    if (existingRow) {
      // Actualizar cantidad y precio
      let quantityInputField = existingRow.querySelector(
        ".cart-item-quantity-input"
      );
      let totalCell = existingRow.querySelector(".cart-item-total");

      let currentQuantity = parseInt(quantityInputField.value);
      let newQuantity = currentQuantity + quantity;
      quantityInputField.value = newQuantity;

      let newTotal = newQuantity * productPrice;
      totalCell.textContent = currencyFormatter(newTotal);
    } else {
      // Nueva fila
      const cartTableBody = document.querySelector("#cart-table-body");
      const newRow = document.createElement("tr");
      newRow.setAttribute("id", `cart-item-${productId}`);

      newRow.innerHTML = `
        <td class="py-2 px-4 border-b text-center">
          <button class="delete-item-button" data-product-id="${productId}">
            <!-- Trash Icon SVG -->
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6 text-red-500 cursor-pointer"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 7l-.867 12.142A2 2 0 0 1 16.138 21H7.862a2 2 0 0 1-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v3m-4 0h14"
              />
            </svg>
          </button>
        </td>
        <td class="py-2 px-4 border-b">${productName}</td>
        <td class="py-2 px-4 border-b">
          <input type="number" min="1" value="${quantity}" class="cart-item-quantity-input w-16 text-center border border-gray-300 rounded-md" data-product-id="${productId}" data-product-price="${productPrice}">
        </td>
        <td class="py-2 px-4 border-b">${currencyFormatter(productPrice)}</td>
        <td class="py-2 px-4 border-b cart-item-total">${currencyFormatter(
          productPrice * quantity
        )}</td>
      `;
      cartTableBody.appendChild(newRow);
    }

    // Actualiza el total
    updateCartTotal();
  }

  // Borra la fila
  function deleteCartItem(button) {
    const productId = button.getAttribute("data-product-id");
    const row = document.getElementById(`cart-item-${productId}`);
    if (row) {
      row.remove();
      // Update the cart total
      updateCartTotal();
    }
  }

  // Actualiza las cantidades
  function updateCartItemQuantity(input) {
    let quantity = parseInt(input.value);
    const productId = input.getAttribute("data-product-id");
    const productPrice = parseFloat(input.getAttribute("data-product-price"));
    const totalCell = document.querySelector(
      `#cart-item-${productId} .cart-item-total`
    );

    if (isNaN(quantity) || quantity <= 0) {
      // Remueve si invalido
      deleteCartItem(
        document.querySelector(`#cart-item-${productId} .delete-item-button`)
      );
    } else {
      // Actualiza el precio total
      let newTotal = quantity * productPrice;
      totalCell.textContent = currencyFormatter(newTotal);

     // Actualiza el total del carrito
      updateCartTotal();
    }
  }

  // Actualiza el total del carrito
  function updateCartTotal() {
    let total = 0;
    document.querySelectorAll("#cart-table-body tr").forEach(function (row) {
      const totalCell = row.querySelector(".cart-item-total");
      if (totalCell) {
        const itemTotalText = totalCell.textContent
          .replace("$", "")
          .replace(/,/g, "");
        const itemTotal = parseFloat(itemTotalText);
        if (!isNaN(itemTotal)) {
          total += itemTotal;
        }
      }
    });
    document.getElementById("cart-total").textContent =
      currencyFormatter(total);
  }
});
