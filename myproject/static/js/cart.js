document.addEventListener('DOMContentLoaded', function () {
    // Event delegation for dynamic content
    document.body.addEventListener('click', function (event) {
      if (event.target.closest('#add-to-cart-button')) {
        event.preventDefault();
        const button = event.target.closest('#add-to-cart-button');
        addToCart(button);
      }
    });
  
    // Function to add item to the cart
    function addToCart(button) {
      const productId = button.getAttribute('data-product-id');
      const productName = button.getAttribute('data-product-name');
      const productPrice = parseFloat(button.getAttribute('data-product-price'));
      const quantityInput = document.getElementById('unit_numbers');
      let quantity = parseInt(quantityInput.value);
  
      if (quantity <= 0 || isNaN(quantity)) {
        alert('Por favor, ingresa una cantidad válida.');
        return;
      }
  
      // Check if the item is already in the cart
      let existingRow = document.querySelector(`#cart-item-${productId}`);
      if (existingRow) {
        // Update quantity and total
        let quantityCell = existingRow.querySelector('.cart-item-quantity');
        let totalCell = existingRow.querySelector('.cart-item-total');
  
        let currentQuantity = parseInt(quantityCell.textContent);
        let newQuantity = currentQuantity + quantity;
        quantityCell.textContent = newQuantity;
  
        let newTotal = newQuantity * productPrice;
        totalCell.textContent = `$${newTotal.toFixed(2)}`;
      } else {
        // Add new row to the cart table
        const cartTableBody = document.querySelector('#cart-table-body');
        const newRow = document.createElement('tr');
        newRow.setAttribute('id', `cart-item-${productId}`);
  
        newRow.innerHTML = `
          <td class="py-2 px-4 border-b">${productName}</td>
          <td class="py-2 px-4 border-b cart-item-quantity">${quantity}</td>
          <td class="py-2 px-4 border-b">$${productPrice.toFixed(2)}</td>
          <td class="py-2 px-4 border-b cart-item-total">$${(productPrice * quantity).toFixed(2)}</td>
        `;
        cartTableBody.appendChild(newRow);
      }
    }
  });
  