document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/cart/")   // 👈 your backend API endpoint
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector("table tbody");
            tbody.innerHTML = ""; // clear old rows

            data.forEach(item => {
                const total = (item.price * item.quantity).toFixed(2);
                const row = `
                    <tr>
                        <th scope="row"><p class="mb-0 py-4">${item.name}</p></th>
                        <td><p class="mb-0 py-4">${item.price} Taka</p></td>
                        <td>
                            <div class="input-group quantity py-4" style="width: 100px;">
                                <div class="input-group-btn">
                                    <button class="btn btn-sm btn-minus rounded-circle bg-light border">
                                        <i class="fa fa-minus"></i>
                                    </button>
                                </div>
                                <input type="text" class="form-control form-control-sm text-center border-0" value="${item.quantity}">
                                <div class="input-group-btn">
                                    <button class="btn btn-sm btn-plus rounded-circle bg-light border">
                                        <i class="fa fa-plus"></i>
                                    </button>
                                </div>
                            </div>
                        </td>
                        <td><p class="mb-0 py-4">${total} Taka</p></td>
                        <td class="py-4">
                            <button class="btn btn-md rounded-circle bg-light border">
                                <i class="fa fa-times text-danger"></i>
                            </button>
                        </td>
                    </tr>
                `;
                tbody.insertAdjacentHTML("beforeend", row);
            });
        })
        .catch(error => console.error("Error fetching cart:", error));
});