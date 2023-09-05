const openModalButton = document.getElementById("open-modal-button");
const walletnumber = document.getElementById("wallet-number");
const bankModal = document.getElementById("bankModal");
const walletModal = document.getElementById("walletModal");
const closeButton = document.querySelector(".close-button");
const walletcloseButton = document.querySelector(".walletclose-button");

openModalButton.addEventListener("click", () => {
  document.getElementById("bankform").style.display = "block";
 bankModal.style.display = "block";
});

walletnumber.addEventListener("click", () => {
  document.getElementById("walletform").style.display = "block";
  walletModal.style.display ="block";
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

