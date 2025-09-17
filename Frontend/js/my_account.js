document.addEventListener("DOMContentLoaded", async () => {
    await loadProfile();
    await loadOrders();
    setupPasswordForm();
});

// --------------------
// Load Profile
// --------------------
async function loadProfile() {
    try {
        const res = await fetch('/accounts/api/profile/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + localStorage.getItem('token')
            }
        });

        if (!res.ok) throw new Error('Failed to fetch profile');

        const data = await res.json();

        const profileCard = document.querySelector(".card-body.text-center");
        if (profileCard) {
            profileCard.querySelector("h4").textContent = data.name;
            profileCard.querySelector("p").textContent = data.email;
        }
    } catch (err) {
        console.error(err);
        alert("Failed to load profile. Please login again.");
    }
}

// --------------------
// Load Orders
// --------------------
async function loadOrders() {
    const tableBody = document.getElementById("order-history-table");

    try {
        const res = await fetch("http://127.0.0.1:8000/orders/order-history/", {
            headers: {
                Authorization: localStorage.getItem("Authorization") || ""
            }
        });
        if (!res.ok) throw new Error("Failed to fetch order history");

        const data = await res.json();

        // Clear the table first
        tableBody.innerHTML = "";

        data.forEach(item => {
            // Map status to badge classes
            let badgeClass = "";
            switch(item.status) {
                case "pending":
                    badgeClass = "bg-warning text-dark";
                    break;
                case "delivered":
                    badgeClass = "bg-success";
                    break;
                case "cancelled":
                    badgeClass = "bg-danger";
                    break;
                case "shipped":
                    badgeClass = "bg-info text-dark";
                    break;
                default:
                    badgeClass = "bg-secondary";
            }

            const row = document.createElement("tr");
            row.innerHTML = `
                <td>#${item.order}</td>
                <td> ${item.product_name} (Qty: ${item.quntity})</td>
                <td><span class="badge ${badgeClass}">${item.status.charAt(0).toUpperCase() + item.status.slice(1)}</span></td>
            `;
            tableBody.appendChild(row);
        });

    } catch (err) {
        console.error(err);
        tableBody.innerHTML = `<tr><td colspan="3">Failed to load order history</td></tr>`;
    }
}

// Helper to set badge color
function getStatusClass(status) {
    switch (status.toLowerCase()) {
        case 'delivered': return 'bg-success';
        case 'pending': return 'bg-warning text-dark';
        case 'cancelled': return 'bg-danger';
        case 'shipped': return 'bg-info text-dark';
        default: return 'bg-secondary';
    }
}

// --------------------
// Update Password
// --------------------
function setupPasswordForm() {
    const form = document.querySelector("#passwordForm");
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const current = document.getElementById('currentPassword').value;
        const newPass = document.getElementById('newPassword').value;
        const confirm = document.getElementById('confirmPassword').value;

        if (newPass !== confirm) {
            alert("New password and confirm password do not match");
            return;
        }

        try {
            const res = await fetch('/accounts/api/update-password/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + localStorage.getItem('token')
                },
                body: JSON.stringify({
                    current_password: current,
                    new_password: newPass,
                    confirm_password: confirm
                })
            });

            const data = await res.json();

            if (!res.ok) {
                // Format error messages nicely
                const messages = Object.values(data).flat().join('\n');
                alert(messages || "Failed to update password");
            } else {
                alert("Password updated successfully!");
                form.reset();
            }
        } catch (err) {
            console.error(err);
            alert("Error updating password. Try again.");
        }
    });
}
