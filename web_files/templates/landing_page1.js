  // Get the modal and the login button
    function openLoginModal() {
        loginModal.style.display = "block";
    }
    const modal = document.getElementById("loginModal");
    const loginButton = document.querySelector(".login-button");
    const loginButton1 = document.querySelector(".login-button1");
    const closeBtn = document.getElementById("closeLoginModal");

    loginButton.addEventListener("click", openLoginModal);
    loginButton1.addEventListener("click", openLoginModal);

    // When the user clicks on the login button, open the modal
    loginButton.addEventListener("click", function () {
        modal.style.display = "block";
    });

    // When the user clicks on <span> (x), close the modal
    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // When the user clicks anywhere outside of the modal, close it
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    // JavaScript for the sign-up form popup
    function openSignupModal() {
        signupModal.style.display = "block";
    }
    const signupModal = document.getElementById("signupModal");
    const signupButton = document.querySelector(".signup-button");
    const signupButton1 = document.querySelector(".signup-button1");
    const closeSignupBtn = document.getElementById("closeSignupModal");

    signupButton.addEventListener("click", openSignupModal);
    signupButton1.addEventListener("click", openSignupModal);

    closeSignupBtn.addEventListener("click", function () {
        signupModal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target === signupModal) {
            signupModal.style.display = "none";
        }
    });

