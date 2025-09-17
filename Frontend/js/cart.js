document.addEventListener("DOMContentLoaded", function () {
  // Fetch order items from API
  fetch("http://127.0.0.1:8000/orders/order-items/", {
    method: "GET",
    headers: {
      Authorization: localStorage.getItem("Authorization"),
      "Content-type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((orderItems) => {
      const tbody = document.getElementById("cart-table-body"); // 👈 tbody where rows will be appended
      const total = 0;
      tbody.innerHTML = ""; // clear old rows

      orderItems.forEach((item) => {
        const row = `
        <tr>
          <th scope="row">
            <p class="mb-0 py-4">${item.product_name}</p>
          </th>
          <td>
            <p class="mb-0 py-4">${item.product_price} Taka</p>
          </td>
          <td>
            <div class="input-group quantity py-4" style="width: 100px;">
              <div class="input-group-btn">
                
              </div>
              <input type="text" class="form-control form-control-sm text-center border-0"
                     value="${item.quantity}" disabled=true>
              <div class="input-group-btn">
                
              </div>
            </div>
          </td>
          <td>
            <p class="mb-0 py-4">${(
              parseFloat(item.product_price) * item.quantity
            ).toFixed(2)} Taka</p>
          </td>
          <td class="py-4">
            <button class="btn btn-md rounded-circle bg-light border delete-btn" data-id="${
              item.product
            }">
              <i class="fa fa-times text-danger"></i>
            </button>
          </td>
        </tr>
      `;

        tbody.insertAdjacentHTML("beforeend", row);
      });

      // Quantity increase/decrease handlers
      tbody.addEventListener("click", async function (e) {
        if (e.target.closest(".btn-plus")) {
          const input = e.target.closest("tr").querySelector("input");
          input.value = parseInt(input.value) + 1;
        }
        if (e.target.closest(".btn-minus")) {
          const input = e.target.closest("tr").querySelector("input");
          if (parseInt(input.value) > 1) {
            input.value = parseInt(input.value) - 1;
          }
        }
        if (e.target.closest(".delete-btn")) {
          const row = e.target.closest("tr");
          row.remove();
          const btn = e.target.closest(".delete-btn");
          const orderId = btn.getAttribute("data-id");
          if (confirm("Are you sure you want to delete this item?")) {
            try {
              const response = await fetch(
                `http://127.0.0.1:8000/orders/order-items/${orderId}`,
                {
                  method: "DELETE",
                  headers: {
                    "Content-Type": "application/json",
                    Authorization: localStorage.getItem("Authorization"),
                  },
                }
              );

              if (response.ok) {
                // remove row from DOM
                btn.closest("tr").remove();
                alert("Item deleted successfully!");
              } else {
                alert("Failed to delete item.");
              }
            } catch (error) {
              console.error("Error deleting item:", error);
              alert("Something went wrong.");
            }
          }
        }
      });

      let subtotal = 0;
      orderItems.forEach((item) => {
        subtotal += parseFloat(item.product_price) * item.quantity;
      });

      console.log(subtotal);

      const cart_subtotal = document.getElementById("cart-subtotal");
      const cart_total = document.getElementById("cart-total");
      cart_subtotal.innerText = `${subtotal} Taka`;
      cart_total.innerText = `${subtotal + 100} Taka`;
    })
    .catch((err) => console.error("Error fetching order items:", err));
});
