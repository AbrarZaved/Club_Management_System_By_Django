console.log("Notification Loaded");

document.addEventListener("DOMContentLoaded", (event) => {
  var notifications = document.getElementById("navbarDropdownMenuLink");

  var notificationCount = document.querySelector(".notification");

  notifications.addEventListener("click", function () {
    console.log("clicked");
    notificationCount.innerText = 0;
  });
});
