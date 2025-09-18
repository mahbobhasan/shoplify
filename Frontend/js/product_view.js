document.addEventListener("DOMContentLoaded", async () => {
  const queryString = window.location.search; // "?id=1&category=2"

  // Create URLSearchParams object
  const urlParams = new URLSearchParams(queryString);

  // Get specific params
  const productId = urlParams.get("id");
  const API_URL = `http://127.0.0.1:8000/products/${productId}/`;
  const container = document.getElementById("product-details-container");

  fetch(API_URL)
    .then((response) => response.json())
    .then((product) => {
      const productHTML = `
              <!-- Image Section -->
              <div class="col-lg-5">
                <div class="border rounded p-3 text-center">
                  <img src="${
                    product.image_url
                  }" class="img-fluid rounded" alt="${product.product_name}">
                </div>
                <!-- Small thumbnails (for now repeat main image) -->
                <div class="d-flex justify-content-center gap-2 mt-3">
                  <img src="${
                    product.image_url
                  }" width="80" class="border rounded cursor-pointer" alt="">
                  <img src="${
                    product.image_url
                  }" width="80" class="border rounded cursor-pointer" alt="">
                  <img src="${
                    product.image_url
                  }" width="80" class="border rounded cursor-pointer" alt="">
                </div>
              </div>

              <!-- Product Info -->
              <div class="col-lg-7">
                <h3 class="mb-3">${product.product_name}</h3>
                <div class="d-flex mb-3">
                  <i class="fa fa-star text-warning"></i>
                  <i class="fa fa-star text-warning"></i>
                  <i class="fa fa-star text-warning"></i>
                  <i class="fa fa-star text-warning"></i>
                  <i class="fa fa-star-half-alt text-warning"></i>
                  <span class="ms-2">(120 Reviews)</span>
                </div>
                <h4 class="text-primary mb-3">৳${product.unit_price}</h4>
                <p class="mb-4">
                  This is a ${
                    product.product_name
                  }. Perfect choice for daily use with amazing features.
                </p>

                <!-- Quantity + Buttons -->
                <form class="d-flex align-items-center mb-4" id="product-to-cart" method="POST">
                  <input type="number" class="form-control w-25 me-3" value="1" min="1" max="${
                    product.quantity
                  }" id="quantity">
                  <button class="btn btn-primary me-2" type="submit"><i class="fa fa-shopping-cart me-1" ></i> Add to Cart</button>
                </form>

                <ul class="list-unstyled">
                  <li><strong>Category:</strong> ${product.category}</li>
                  <li><strong>Availability:</strong> ${
                    product.quantity > 0 ? "In Stock" : "Out of Stock"
                  }</li>
                  <li><strong>Shipping:</strong> Free Shipping on orders over $100</li>
                </ul>
              </div>
            `;

      container.innerHTML = productHTML;
      document
    .getElementById("product-to-cart")
    .addEventListener("submit", function (e) {
      e.preventDefault(); // prevent default form submission

      const quantity = document.getElementById("quantity").value;
      console.log(quantity);
      const data = {
        product: productId,
        quantity: quantity,
      };

      fetch("http://127.0.0.1:8000/orders/order-items/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: localStorage.getItem("Authorization"),
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (!response.ok) throw new Error("Network response was not ok");
          return response.json();
        })
        .then((result) => {
          if (result.ok) {
            console.log("Order placed successfully:", result.json());
            alert("Order placed!");
            window.location.href="../cart.html"
          }
          else {
            alert("Failed to place order.",result.json());
          }
        })
        .catch((error) => {
          console.error("Error placing order:", error);
          alert("Failed to place order.");
        });
    });
    })
    .catch((error) => console.error("Error fetching product:", error));

  
});

