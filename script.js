document.addEventListener("DOMContentLoaded", () => {
    const phoneInput = document.getElementById("phone");
    const otpInput = document.getElementById("otp");
    const otpGroup = document.getElementById("otp-group");
    const otpBtn = document.getElementById("otp-btn");
    const status = document.getElementById("status");
  
    let otpSent = false;
  
    otpBtn.addEventListener("click", async () => {
      const phone = phoneInput.value;
  
      if (!otpSent) {
        // Send OTP
        try {
          const response = await fetch("http://localhost:5000/send-otp", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ phone })
          });
          const result = await response.json();
          if (result.success) {
            otpGroup.style.display = "block";
            otpBtn.textContent = "Verify OTP";
            otpSent = true;
            status.textContent = "OTP sent!";
          } else {
            status.textContent = "Failed to send OTP";
          }
        } catch (err) {
          console.error(err);
          status.textContent = "Server error";
        }
      } else {
        // Verify OTP
        const otp = otpInput.value;
        try {
          const response = await fetch("http://localhost:5000/verify-otp", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ phone, otp })
          });
          const result = await response.json();
          if (result.verified) {
            status.textContent = "OTP Verified!";
            window.location.href = `details.html?phone=${encodeURIComponent(phone)}`;
          } else {
            status.textContent = "Invalid OTP";
          }
        } catch (err) {
          console.error(err);
          status.textContent = "Verification error";
        }
      }
    });
  });
  