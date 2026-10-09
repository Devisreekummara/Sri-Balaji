// Show or hide the navigation menu on small screens.
const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");

if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", function () {
        navLinks.classList.toggle("show");
    });
}

// Basic phone number check before the enquiry form is sent.
const enquiryForm = document.getElementById("enquiryForm");

if (enquiryForm) {
    enquiryForm.addEventListener("submit", function (event) {
        const phoneInput = document.getElementById("phone");
        const phone = phoneInput.value.trim();

        if (!/^[0-9+\-\s()]{7,20}$/.test(phone)) {
            event.preventDefault();
            alert("Please enter a valid phone number.");
            phoneInput.focus();
        }
    });
}

// Automatically hide status messages after a few seconds.
const flashMessages = document.querySelectorAll(".flash");

flashMessages.forEach(function (message) {
    setTimeout(function () {
        message.style.display = "none";
    }, 5000);
});
