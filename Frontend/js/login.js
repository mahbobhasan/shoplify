
document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById('container');
  document.getElementById('signUp').addEventListener('click', () => {
    container.classList.add("right-panel-active");
  });
  document.getElementById('signIn').addEventListener('click', () => {
    container.classList.remove("right-panel-active");
  });
  // Handle Signup
  const signupForm = document.getElementById('sign-up-form');
  signupForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const frrm=e.target
    const frm=new FormData(frrm)
    frm.append("password2",signupForm.elements['password'].value)
    

    console.log(JSON.stringify(frm))
    try {
      const response = await fetch("http://127.0.0.1:8000/accounts/register/", {
        method: "POST", 
        body: frm
      });

      const data = await response.json();
     console.log(await data)
      if ( response.ok) {
      const user=await data.user
      localStorage.setItem("user",await user)
      alert("✅ Account created successfully!");
      window.location.href="verify_otp.html"
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
      const response = await fetch("http://127.0.0.1:8000/accounts/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      if (response.ok) {
        alert("✅ Login successful!");
        localStorage.setItem("Authorization", `Bearer ${data.access}`); // store JWT for later
        window.location.href = "index.html"; // redirect to home
      } else {
        alert("❌ Login failed: " + (data.detail || JSON.stringify(data)));
      }
    } catch (error) {
      console.error("Error:", error);
    }
  });
});

