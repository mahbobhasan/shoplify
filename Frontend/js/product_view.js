const productId = 1; // Example: you can get this from URL or Django context

// Fetch Product Details
fetch(`/api/products/${productId}/`)
  .then(res => res.json())
  .then(data => {
    document.querySelector(".product-title").textContent = data.name;
    document.querySelector(".product-price").textContent = `$${data.price}`;
    document.querySelector(".product-desc").textContent = data.description;
    document.querySelector(".product-img").src = data.images[0];
  });

//pore review er ta add korte hobe
// // Fetch Reviews
// fetch(`/api/products/${productId}/reviews/`)
//   .then(res => res.json())
//   .then(data => {
//     const reviewsContainer = document.querySelector("#reviewsContainer");
//     reviewsContainer.innerHTML = "";
//     data.forEach(review => {
//       reviewsContainer.innerHTML += `
//         <div class="border p-3 mb-3 rounded">
//           <div class="d-flex align-items-center mb-2">
//             <i class="fa fa-user-circle fa-2x me-2"></i>
//             <strong>${review.username}</strong>
//           </div>
//           <p class="mb-1">${"⭐".repeat(review.rating)} - ${review.comment}</p>
//         </div>
//       `;
//     });
//   });

// Add to Cart
document.querySelector("#addToCartBtn").addEventListener("click", () => {
  const quantity = document.querySelector("#quantityInput").value;
  fetch("/api/cart/add/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("token")}`
    },
    body: JSON.stringify({ product_id: productId, quantity: quantity })
  })
  .then(res => res.json())
  .then(data => alert(data.message));
});

///wishlist add kori nai 
// Fetch Related Products
fetch(`/api/products/${productId}/related/`)
  .then(res => res.json())
  .then(data => {
    const relatedContainer = document.querySelector("#relatedProductsContainer");
    relatedContainer.innerHTML = "";
    data.forEach(product => {
      relatedContainer.innerHTML += `
        <div class="col-md-3">
          <div class="card shadow-sm">
            <a href="/products/${product.id}/">
              <img src="${product.image}" class="card-img-top img-fluid" alt="${product.name}">
            </a>
            <div class="card-body text-center">
              <h6 class="card-title">${product.name}</h6>
              <p class="text-primary mb-2">$${product.price}</p>
              <a href="/products/${product.id}/" class="btn btn-sm btn-outline-primary">View</a>
            </div>
          </div>
        </div>
      `;
    });
  });


// #Fetch product list
  fetch('http://127.0.0.1:8000/products/')
  .then(response => response.json())
  .then(data => {
    const productList = document.getElementById('product-list');
    data.forEach(product => {
      const productItem = document.createElement('div');
      productItem.innerHTML = `
        <h3>${product.product_name}</h3>
        <img src="${product.image_url}" width="150" />
        <p>Price: $${product.unit_price}</p>
      `;
      productList.appendChild(productItem);
    });
  })
  .catch(error => console.error('Error:', error));

  // search products
  function searchProducts() {
    const query = document.getElementById('search-input').value;
    fetch(`http://127.0.0.1:8000/products/search/?q=${query}`)
      .then(response => response.json())
      .then(data => {
        const results = document.getElementById('search-results');
        results.innerHTML = '';
        data.forEach(product => {
          const item = document.createElement('div');
          item.innerHTML = `
            <h4>${product.product_name}</h4>
            <img src="${product.image_url}" width="100" />
            <p>Price: $${product.unit_price}</p>
          `;
          results.appendChild(item);
        });
      });
  }