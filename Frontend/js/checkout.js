document.addEventListener("DOMContentLoaded", () => {
    fetch("http://127.0.0.1:8000/orders/order-items/", {
        method: "GET",
        headers: {
            Authorization: localStorage.getItem("Authorization"),
            "Content-type": "application/json",
        }
    })
        .then((res) => res.json())
        .then((orderItems) => {
            const tbody = document.getElementById("cart-table-body"); // 👈 tbody where rows will be appended
            let total = 0;
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
    
        </tr>
      `;

                tbody.insertAdjacentHTML("beforeend", row);
                total+=(parseFloat(item.product_price) * item.quantity)
            });
            const cart_total = document.getElementById("cart-total");
            cart_total.innerText = `${total+100} Taka`;
        })
    .catch((err) => console.error("Error fetching order items:", err));
    console.log(total)

    const checkout_form = document.getElementById("checkout-form")
    checkout_form.addEventListener("submit", async (event) => {
        event.preventDefault()
        const frm = event.target
        const frm_data = new FormData(frm)
        const res = await fetch("http://127.0.0.1:8000/orders/", {
            method: "POST",
            body: frm_data,
            headers: {
                Authorization: localStorage.getItem("Authorization"),
            }
        });
        if (res.ok) {
            alert("Order successfully placed. Redirecting to your dashboard")
            window.location.href = "../my_account.html"
            
        }
        else {
          alert("Error occured")  
        }
    })
});

