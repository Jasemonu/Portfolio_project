document.addEventListener('DOMContentLoaded', function() {
            // Get the form and button elements
            var transferForm = document.getElementById('transferForm');
            var transferButton = document.getElementById('transferButton');

            // Add an event listener to the transfer button
            transferButton.addEventListener('click', function() {
                // Get the entered amount
                var amount = parseFloat(document.getElementById('amount').value);

                // Perform your transfer logic here
                // For this example, we'll just display an alert with the amount
                alert('Transferring ' + amount + ' dollars.');
            });
        });
