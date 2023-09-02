const openModalButton = document.getElementById("open-modal-button");
const modal = document.getElementById("walletModal");
const closeButton = document.querySelector(".close-button");

openModalButton.addEventListener("click", (event) => {
  modal.style.display = "block";
});

closeButton.addEventListener("click", () => {
  modal.style.display = "none";
});

window.addEventListener("click", (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
});

