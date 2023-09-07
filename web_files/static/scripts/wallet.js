const openModalButton = document.getElementById("open-modal-button");
const walletnumber = document.getElementById("wallet-number");
const bankModal = document.getElementById("bankModal");
const walletModal = document.getElementById("walletModal");
const closeButton = document.querySelector(".close-button");
const walletcloseButton = document.querySelector(".walletclose-button");

openModalButton.addEventListener("click", () => {
  document.getElementById("bankform").style.display = "block";
 bankModal.style.display = "block";
 walletModal.style.display = "none";
});

walletnumber.addEventListener("click", () => {
  document.getElementById("walletform").style.display = "block";
  walletModal.style.display ="block";
  bankModal.style.display = "none";
});

closeButton.addEventListener("click", () => {
  bankModal.style.display = "none";
});

walletcloseButton.addEventListener("click", () => {
  walletModal.style.display = "none";
});

window.addEventListener("click", function (event) {
  if (event.target === bankModal || event.target === walletModal) {
    bankModal.style.display = "none";
    walletModal.style.display = "none";
  }
});

document.addEventListener("DOMContentLoaded", () => {
    const apiKey = '17ea4ccf9f2fec4dff3d12d76a361030'; // Replace with your API key
    const apiUrl = `https://api.apilayer.com/exchangerates_data/latest?access_key=${apiKey}`;
    const exchangeRateList = document.getElementById('exchange-rate-list');

    fetch(apiUrl)
        .then((response) => response.json())
        .then((data) => {
            const rates = data.rates;
            for (const currency in rates) {
                if (rates.hasOwnProperty(currency)) {
                    const listItem = document.createElement('li');
                    listItem.className = 'exchange-rate-item';
                    listItem.innerHTML = `<span>${currency}:</span> ${rates[currency]}`;
                    exchangeRateList.appendChild(listItem);
                }
            }
        })
        .catch((error) => {
            console.error('Error fetching exchange rates:', error);
        });
});

