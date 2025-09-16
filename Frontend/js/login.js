
document.addEventListener("DOMContentLoaded", () => {
  // Handle Signup
  const signupForm = document.querySelector('.sign-up-container form');
  signupForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = {
      name: signupForm.name.value,
      email: signupForm.email.value,
      password: signupForm.password.value
    };

    try {
      const response = await fetch("/api/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      if (response.ok) {
        alert("✅ Account created successfully!");
        // Redirect or show login form
      } else {
        alert("❌ Signup failed: " + (data.detail || JSON.stringify(data)));
      }
    } catch (error) {
      console.error("Error:", error);
    }
  });

  // Handle Login
  const loginForm = document.getElementById("loginForm");
  loginForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = {
      email: loginForm.email.value,
      password: loginForm.password.value
    };

    try {
      const response = await fetch("/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      if (response.ok) {
        alert("✅ Login successful!");
        localStorage.setItem("token", data.token); // store JWT for later
        window.location.href = "index.html"; // redirect to home
      } else {
        alert("❌ Login failed: " + (data.detail || JSON.stringify(data)));
      }
    } catch (error) {
      console.error("Error:", error);
    }
  });
});

