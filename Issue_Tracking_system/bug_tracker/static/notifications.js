window.addEventListener("DOMContentLoaded", (event) => {
  const dismissAll = document.getElementById("dismiss-all");

  dismissAll.addEventListener("click", function (e) {
    e.preventDefault();

    // Make an AJAX request to delete all notifications
    fetch("/delete_all_notifications/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => {
        if (response.ok) {
          // Remove all the notification cards from the UI
          const notificationCards =
            document.querySelectorAll(".notification-card");
          notificationCards.forEach((card) => {
            card.remove();
          });

          // Hide the "Today" and "Older" headings
          const today = document.querySelector(".today");
          const older = document.querySelector(".older");
          today.style.display = "none";
          older.style.display = "none";

          // Hide the "Dismiss All" link
          dismissAll.style.display = "none";

          // Add the "All caught up!" message
          const row = document.querySelector(".notification-container");
          const message = document.createElement("h4");
          message.classList.add("text-center");
          message.innerHTML = "All caught up!";
          row.appendChild(message);
        } else {
          console.log("Error:", response.status);
        }
      })
      .catch((error) => {
        console.log("Error:", error);
      });
  });
});
