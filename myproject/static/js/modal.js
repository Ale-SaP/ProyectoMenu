// modal.js

// Variables to keep track of focus
let lastFocusedElement;

// Function to close the modal
function closeModal() {
  const modal = document.getElementById("modal");
  if (modal) {
    modal.classList.add("hidden");
  }
  document.body.classList.remove("overflow-hidden");

  // Remove event listeners when modal is closed
  document.removeEventListener("keydown", handleKeyDown);
  modal.removeEventListener("click", handleOverlayClick);

  // Restore focus to the last focused element
  if (lastFocusedElement) {
    lastFocusedElement.focus();
  }
}

// Function to handle keydown events
function handleKeyDown(event) {
  if (event.key === "Escape" || event.key === "Esc") {
    event.preventDefault();
    closeModal();
  } else if (event.key === "Tab") {
    trapFocus(event);
  }
}

// Function to handle clicks on the overlay
function handleOverlayClick(event) {
  const modal = document.getElementById("modal");
  if (event.target === modal) {
    closeModal();
  }
}

// Function to trap focus within the modal
function trapFocus(event) {
  const modalContent = document.getElementById("modal-content");
  const focusableElementsString =
    'a[href], area[href], input:not([disabled]), select:not([disabled]), \
    textarea:not([disabled]), button:not([disabled]), iframe, object, embed, \
    [tabindex="0"], [contenteditable]';
  const focusableElements = modalContent.querySelectorAll(focusableElementsString);
  const firstFocusableElement = focusableElements[0];
  const lastFocusableElement = focusableElements[focusableElements.length - 1];

  if (event.shiftKey) {
    // Shift + Tab
    if (document.activeElement === firstFocusableElement) {
      event.preventDefault();
      lastFocusableElement.focus();
    }
  } else {
    // Tab
    if (document.activeElement === lastFocusableElement) {
      event.preventDefault();
      firstFocusableElement.focus();
    }
  }
}

// Function to initialize modal event listeners
function initializeModalEventListeners() {
  // Save the last focused element
  lastFocusedElement = document.activeElement;

  const modal = document.getElementById("modal");
  const modalContent = document.getElementById("modal-content");

  if (modal && modalContent) {
    modal.classList.remove("hidden");
    document.body.classList.add("overflow-hidden");

    // Add event listeners
    document.addEventListener("keydown", handleKeyDown);
    modal.addEventListener("click", handleOverlayClick);

    // Wait for the modal content to render
    setTimeout(() => {
      // Find the first focusable element in the modal
      const focusableElementsString =
        'a[href], area[href], input:not([disabled]), select:not([disabled]), \
        textarea:not([disabled]), button:not([disabled]), iframe, object, embed, \
        [tabindex="0"], [contenteditable]';
      const focusableElements = modalContent.querySelectorAll(focusableElementsString);

      if (focusableElements.length > 0) {
        focusableElements[0].focus();
      } else {
        // If no focusable element, focus the modal itself
        modalContent.setAttribute("tabindex", "-1");
        modalContent.focus();
      }
    }, 0);

    // Initialize quantity buttons
    initializeQuantityButtons();
  }
}

// Function to initialize quantity button event listeners
function initializeQuantityButtons() {
  const incrementButton = document.getElementById("increment-button");
  const decrementButton = document.getElementById("decrement-button");
  const quantityInput = document.getElementById("unit_numbers_modal");

  if (incrementButton && decrementButton && quantityInput) {
    incrementButton.addEventListener("click", function () {
      let currentValue = parseInt(quantityInput.value) || 0;
      if (currentValue < parseInt(quantityInput.max)) {
        quantityInput.value = currentValue + 1;
      }
    });

    decrementButton.addEventListener("click", function () {
      let currentValue = parseInt(quantityInput.value) || 0;
      if (currentValue > parseInt(quantityInput.min)) {
        quantityInput.value = currentValue - 1;
      }
    });

    // Ensure the input value stays within min and max when manually changed
    quantityInput.addEventListener("input", function () {
      let value = parseInt(quantityInput.value) || 0;
      const min = parseInt(quantityInput.min);
      const max = parseInt(quantityInput.max);

      if (value < min) {
        quantityInput.value = min;
      } else if (value > max) {
        quantityInput.value = max;
      }
    });
  }
}

document.addEventListener("htmx:afterSwap", function (event) {
  if (event.detail.target && event.detail.target.id === "modal-content") {
    // Initialize modal event listeners
    initializeModalEventListeners();
  }
});

// Expose closeModal function to global scope
window.closeModal = closeModal;
