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
    try {
        const res = await fetch('/orders/api/my-orders/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + localStorage.getItem('token')
            }
        });

        if (!res.ok) throw new Error('Failed to fetch orders');

        const data = await res.json();
        const orders = data.results || data; // support paginated or direct list
        const tbody = document.querySelector(".table tbody");
        tbody.innerHTML = ''; // clear existing rows

        orders.forEach(order => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>#${order.id}</td>
                <td>${order.product_name}</td>
                <td><span class="badge ${getStatusClass(order.status)}">${order.status}</span></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error(err);
        alert("Failed to load orders.");
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
