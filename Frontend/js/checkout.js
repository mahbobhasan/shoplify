document.addEventListener("DOMContentLoaded", () => {
    const cartTableBody = document.querySelector("table tbody");
    const placeOrderBtn = document.querySelector(".btn.btn-primary.border-secondary");

    // 1️⃣ Fetch cart items
    fetch("/orders/api/cart/")
        .then(res => res.json())
        .then(data => {
            cartTableBody.innerHTML = "";
            let subtotal = 0;

            data.forEach(item => {
                const total = item.price * item.quantity;
                subtotal += total;

                cartTableBody.innerHTML += `
                    <tr class="text-center">
                        <th scope="row" class="text-start py-4">${item.name}</th>
                        <td class="py-4">${item.model}</td>
                        <td class="py-4">$${item.price.toFixed(2)}</td>
                        <td class="py-4 text-center">${item.quantity}</td>
                        <td class="py-4">$${total.toFixed(2)}</td>
                    </tr>
                `;
            });

            const shipping = 100; // example shipping
            const total = subtotal + shipping;

            cartTableBody.innerHTML += `
                <tr>
                    <th scope="row"></th>
                    <td class="py-4"></td>
                    <td class="py-4"></td>
                    <td class="py-4">
                        <p class="mb-0 text-dark py-2">Subtotal</p>
                    </td>
                    <td class="py-4">
                        <div class="py-2 text-center border-bottom border-top">
                            <p class="mb-0 text-dark">$${subtotal.toFixed(2)}</p>
                        </div>
                    </td>
                </tr>
                <tr>
                    <th scope="row"></th>
                    <td class="py-4">
                        <p class="mb-0 text-dark py-4">Shipping Cost: <span>${shipping} Taka</span></p>
                    </td>
                </tr>
                <tr>
                    <th scope="row"></th>
                    <td class="py-4">
                        <p class="mb-0 text-dark text-uppercase py-2">TOTAL</p>
                    </td>
                    <td class="py-4"></td>
                    <td class="py-4"></td>
                    <td class="py-4">
                        <div class="py-2 text-center border-bottom border-top">
                            <p class="mb-0 text-dark">$${total.toFixed(2)}</p>
                        </div>
                    </td>
                </tr>
            `;
        })
        .catch(err => console.error("Error fetching cart:", err));

    // 2️⃣ Fetch user billing info
    fetch("/accounts/api/profile/")
        .then(res => res.json())
        .then(data => {
            // Map fields correctly
            document.getElementById("billing-name").value = data.name || "";
            document.getElementById("billing-company")?.value = data.company || "";
            document.getElementById("billing-address").value = data.address || "";
            document.getElementById("billing-city").value = data.city || "";
            document.getElementById("billing-country")?.value = data.country || "";
            document.getElementById("billing-postcode")?.value = data.postcode || "";
            document.getElementById("billing-mobile").value = data.mobile || "";
            document.getElementById("billing-email").value = data.email || "";
        })
        .catch(err => console.error("Error fetching profile:", err));

    // 3️⃣ Place order
    placeOrderBtn.addEventListener("click", () => {
        const billing = {
            name: document.getElementById("billing-name").value,
            company: document.getElementById("billing-company")?.value || "",
            address: document.getElementById("billing-address").value,
            city: document.getElementById("billing-city").value,
            country: document.getElementById("billing-country")?.value || "",
            postcode: document.getElementById("billing-postcode")?.value || "",
            mobile: document.getElementById("billing-mobile").value,
            email: document.getElementById("billing-email").value,
            notes: document.getElementById("order-notes").value
        };

        const payment_method = document.querySelector("input[type='checkbox']:checked")?.value || "";

        fetch("/orders/api/checkout/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ billing, payment_method })
        })
            .then(res => {
                if (!res.ok) throw new Error("Network response was not ok");
                return res.json();
            })
            .then(data => {
                alert("Order placed successfully!");
                window.location.href = "thankyou.html";
            })
            .catch(err => {
                console.error("Error placing order:", err);
                alert("Failed to place order. Try again!");
            });
    });

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
