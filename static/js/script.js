document.addEventListener("DOMContentLoaded", function () {
  /*** Hide All Modals on Page Load ***/
  document
    .querySelectorAll(".modals")
    .forEach((modal) => (modal.style.display = "none"));

  /*** MODALS & ELEMENTS ***/
  const modals = {
    register: document.getElementById("registerModal"),
    status: document.getElementById("statusModal"),
    delete: document.getElementById("deleteModal"),
    flagStar: document.getElementById("flagStarModal"),
  };

  const buttons = {
    create: document.querySelector(".create-btn"),
    registerForm: document.getElementById("registerForm"),
    confirmStatus: document.getElementById("confirmStatus"),
    confirmDelete: document.getElementById("confirmDelete"),
  };

  const popups = {
    success: document.getElementById("successPopup"),
    error: document.getElementById("errorPopup"),
    toast: document.getElementById("toast"),
  };

  const searchInput = document.getElementById("searchInput");
  const filterIcon = document.querySelector(".filter-icon");
  const filterOptions = document.querySelector(".filter-options");
  const filterItems = document.querySelectorAll(".filter-option");
  const tableRows = document.querySelectorAll("#memberTable tbody tr");

  function toggleSidebar() {
    document.querySelector(".sidebar").classList.toggle("active");
  }

  let selectedUserRow = null;
  let selectedStatus = null;
  let selectedMember = null;

  /*** UTILITY FUNCTIONS ***/
  function showModal(modal) {
    modal.style.display = "flex";
  }

  function closeModal(modal) {
    modal.style.display = "none";
  }

  function showToast(message) {
    popups.toast.textContent = message;
    popups.toast.style.display = "block";
    setTimeout(() => {
      popups.toast.style.display = "none";
    }, 3000);
  }

  /*** MODAL CLOSE EVENTS ***/
  document.querySelectorAll(".cancel-btn, .modals .close").forEach((btn) => {
    btn.addEventListener("click", function () {
      closeModal(this.closest(".modals"));
    });
  });

  window.addEventListener("click", function (event) {
    document.querySelectorAll(".modals").forEach((modal) => {
      if (event.target === modal) closeModal(modal);
    });
  });

  /*** SEARCH & FILTER FUNCTIONALITY ***/
  filterIcon.addEventListener("click", function (event) {
    filterOptions.style.display =
      filterOptions.style.display === "block" ? "none" : "block";
    event.stopPropagation();
  });

  document.addEventListener("click", function (event) {
    if (
      !filterIcon.contains(event.target) &&
      !filterOptions.contains(event.target)
    ) {
      filterOptions.style.display = "none";
    }
  });

  filterItems.forEach((item) => {
    item.addEventListener("click", function () {
      filterTable(this.getAttribute("data-filter"));
      filterOptions.style.display = "none";
    });
  });

  function filterTable(filter) {
    tableRows.forEach((row) => {
      const statusElement = row.querySelector(".status");
      if (!statusElement) return;
      const status = statusElement.textContent.trim().toLowerCase();
      row.style.display =
        filter === "all" || status.includes(filter) ? "" : "none";
    });
  }

  searchInput.addEventListener("keyup", function () {
    const searchTerm = searchInput.value.toLowerCase();
    tableRows.forEach((row) => {
      const name = row.querySelector("td span").textContent.toLowerCase();
      const email = row
        .querySelector("td:nth-child(2)")
        .textContent.toLowerCase();
      row.style.display =
        name.includes(searchTerm) || email.includes(searchTerm) ? "" : "none";
    });
  });

  /*** STATUS CHANGE FUNCTIONALITY ***/
  function updateStatusUI(statusElement, newStatus) {
    if (newStatus === "Deactivated") {
      statusElement.textContent = "● Deactivated";
      statusElement.classList.remove("available");
      statusElement.classList.add("deactivated");
      statusElement.style.color = "red";
    } else {
      statusElement.textContent = "● Available";
      statusElement.classList.remove("deactivated");
      statusElement.classList.add("available");
      statusElement.style.color = "green";
    }
  }

  document.addEventListener("click", function (event) {
    if (event.target.classList.contains("status")) {
      selectedStatus = event.target;
      selectedMember = event.target
        .closest("tr")
        .querySelector("td span")
        .textContent.trim();

      document.getElementById("modalTitle").innerHTML =
        selectedStatus.classList.contains("available")
          ? `You are about to deactivate <span>${selectedMember}</span>`
          : `You are about to make <span>${selectedMember}</span> available again`;

      document.getElementById("modalMessage").innerHTML =
        selectedStatus.classList.contains("available")
          ? "Are you sure you want to deactivate this member?"
          : "Are you sure you want to reactivate this member?";

      buttons.confirmStatus.textContent = selectedStatus.classList.contains(
        "available"
      )
        ? "Yes, Deactivate"
        : "Yes, Make Available";

      showModal(modals.status);
    }
  });

  buttons.confirmStatus.addEventListener("click", function () {
    if (selectedStatus && selectedMember) {
      let storedStatuses =
        JSON.parse(localStorage.getItem("memberStatuses")) || {};
      updateStatusUI(
        selectedStatus,
        selectedStatus.classList.contains("available")
          ? "Deactivated"
          : "Available"
      );
      storedStatuses[selectedMember] = selectedStatus.classList.contains(
        "available"
      )
        ? "Available"
        : "Deactivated";
      localStorage.setItem("memberStatuses", JSON.stringify(storedStatuses));
    }
    closeModal(modals.status);
  });

  /*** DELETE USER FUNCTIONALITY ***/
  document.addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-user")) {
      selectedUserRow = event.target.closest("tr");
      document.getElementById("deleteMemberName").textContent =
        selectedUserRow.querySelector("span").textContent;
      showModal(modals.delete);
    }
  });

  buttons.confirmDelete.addEventListener("click", function () {
    if (selectedUserRow) {
      selectedUserRow.remove();
      showToast("User Deleted");
    }
    closeModal(modals.delete);
  });

  /*** ACTION MENU HANDLING ***/
  document.addEventListener("click", function (event) {
    if (event.target.classList.contains("action-icon")) {
      const menu = event.target.nextElementSibling;
      menu.style.display = menu.style.display === "block" ? "none" : "block";
      event.stopPropagation();
    } else {
      document
        .querySelectorAll(".action-list")
        .forEach((menu) => (menu.style.display = "none"));
    }
  });

  /*** FLAG & STAR FUNCTIONALITY ***/
  document.addEventListener("click", function (event) {
    if (event.target.classList.contains("flag-star")) {
      const userRow = event.target.closest("tr");
      document.getElementById("flagStarName").textContent =
        userRow.querySelector("span").textContent;
      document.getElementById("flagStarEmail").textContent =
        userRow.querySelector("td:nth-child(2)").textContent;
      showModal(modals.flagStar);
    }

    if (
      event.target.classList.contains("flag-icon") ||
      event.target.classList.contains("star-icon")
    ) {
      event.target.classList.toggle("active");
      showToast(
        event.target.classList.contains("active")
          ? `User ${
              event.target.classList.contains("flag-icon")
                ? "Flagged"
                : "Starred"
            }`
          : `User ${
              event.target.classList.contains("flag-icon")
                ? "Unflagged"
                : "Unstarred"
            }`
      );
    }
  });

  /*** LOAD ACTIVE MENU ***/
  const menuItems = document.querySelectorAll(".menu-item");
  function loadActiveMenu() {
    const activeMenu = localStorage.getItem("activeMenu");
    menuItems.forEach((item) =>
      item.classList.toggle(
        "active",
        item.getAttribute("data-page") === activeMenu
      )
    );
  }

  menuItems.forEach((item) => {
    item.addEventListener("click", function () {
      localStorage.setItem("activeMenu", this.getAttribute("data-page"));
      loadActiveMenu();
    });
  });

  loadActiveMenu();
});
