document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission

    // Gather form data
    const formData = new FormData(event.target);

    // Send POST request using fetch
    fetch("/login", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Handle response from the server (e.g., show success message)
        console.log(data);
    })
    .catch(error => {
        // Handle errors (e.g., show error message)
        console.error("Error:", error);
    });
});
