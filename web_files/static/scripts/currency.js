document.addEventListener("DOMContentLoaded", () => {
    const fromCurrencySelect = document.getElementById('fromCurrency');
    const toCurrencySelect = document.getElementById('toCurrency');
    const amountInput = document.getElementById('amount');
    const convertedAmountSpan = document.querySelector('#convertedAmount span');

    // Define hardcoded exchange rates (replace with your rates)
    const exchangeRates = {
        USD: 1,
        EUR: 0.93,
        GBP: 0.80,
		NGN: 784.50,
		GHS: 11.25,
        // Add more exchange rates as needed
    };

    // Function to perform currency conversion
    function convertCurrency() {
        const fromCurrency = fromCurrencySelect.value;
        const toCurrency = toCurrencySelect.value;
        const amount = parseFloat(amountInput.value);

        if (exchangeRates[fromCurrency] && exchangeRates[toCurrency]) {
            const conversionRate = exchangeRates[toCurrency] / exchangeRates[fromCurrency];
            const convertedAmount = (amount * conversionRate).toFixed(2);
            convertedAmountSpan.textContent = convertedAmount + ' ' + toCurrency;
        } else {
            convertedAmountSpan.textContent = 'Invalid conversion';
        }
    }

    // Attach event listeners for input and select changes
    amountInput.addEventListener('input', convertCurrency);
    fromCurrencySelect.addEventListener('change', convertCurrency);
    toCurrencySelect.addEventListener('change', convertCurrency);
});

