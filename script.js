// Mock backend user list
const users = [
  { email: "john.doe@example.com", password: "Strong@123" },
  { email: "alice.smith@example.com", password: "Password@2025" }
];

let loginAttempts = 0;

function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

function checkPasswordStrength(password) {
  if (password.length < 6) return "Weak";
  if (/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/.test(password)) return "Medium";
  if (/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(password)) return "Strong";
  return "Weak";
}

// Live password strength checker
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("password").addEventListener("input", function() {
    const strengthText = document.getElementById("passStrength");
    const strength = checkPasswordStrength(this.value);
    strengthText.textContent = "Strength: " + strength;
    strengthText.className = "strength " + strength.toLowerCase();
  });

  // Show/Hide password
  document.getElementById("togglePass").addEventListener("change", function() {
    const passField = document.getElementById("password");
    passField.type = this.checked ? "text" : "password";
  });

  // Auto login if remembered
  const savedUser = localStorage.getItem("loggedInUser");
  if (savedUser) {
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("logoutBtn").style.display = "inline-block";
    document.getElementById("message").textContent = "Welcome back, " + savedUser;
    document.getElementById("message").className = "success";
  }
});

function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const emailError = document.getElementById("emailError");
  const passError = document.getElementById("passError");
  const message = document.getElementById("message");

  emailError.textContent = "";
  passError.textContent = "";
  message.textContent = "";

  if (!validateEmail(email)) {
    emailError.textContent = "Invalid email format!";
    return;
  }

  // Check if user exists
  const user = users.find(u => u.email === email && u.password === password);

  if (!user) {
    loginAttempts++;
    passError.textContent = "Invalid credentials! Attempt " + loginAttempts + " of 3.";
    
    if (loginAttempts >= 3) {
      passError.textContent = "Account locked due to multiple failed attempts!";
      document.querySelector("button").disabled = true;
    }
    return;
  }

  // Reset attempts on success
  loginAttempts = 0;

  message.textContent = "✅ Login successful!";
  message.className = "success";
  document.getElementById("loginForm").style.display = "none";
  document.getElementById("logoutBtn").style.display = "inline-block";

  if (document.getElementById("rememberMe").checked) {
    localStorage.setItem("loggedInUser", email);
  }
}

function logout() {
  localStorage.removeItem("loggedInUser");
  document.getElementById("loginForm").style.display = "block";
  document.getElementById("logoutBtn").style.display = "none";
  document.getElementById("message").textContent = "You have logged out.";
  document.getElementById("message").className = "error";
  document.getElementById("email").value = "";
  document.getElementById("password").value = "";
}
