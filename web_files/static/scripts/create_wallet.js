const openModalButton = document.getElementById("open-modal-button");
const walletModal = document.getElementById("walletModal");
const closeButton = document.querySelector(".close-button");

openModalButton.addEventListener("click", () => {
  walletModal.style.display ="block";
});

closeButton.addEventListener("click", () => {
  walletModal.style.display = "none";
});

window.addEventListener("click", function (event) {
  if (event.target === bankModal || event.target === walletModal) {
    walletModal.style.display = "none";
  }
});

