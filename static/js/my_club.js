function filterTable(filter) {
  var rows = document.getElementById("clubTable").getElementsByTagName("tr");
  console.log(rows);
  var noReq = document.querySelector("#no-req");
  var memReq = document.querySelector("#mem-req");
  var update_button = document.getElementById("update");
  var rowLength = rows.length;

  if (rows.length == 0) {
    memReq.style.display = "none";
    if (filter === "members") {
      noReq.innerHTML = "No Members";
      update_button.style.display = "none";
    } else if (filter === "requests") {
      noReq.innerHTML = "No Join Requests";
      update_button.style.display = "none";
    }
  } else {
    noReq.style.display = "none";
    for (var i = 0; i < rowLength; i++) {
      if (filter === "members") {
        if (rows[i].classList.contains("members")) {
          console.log(rows[i]);
          rows[i].style.display = "";
          update_button.style.display = "none";
        } else {
          rows[i].style.display = "none";
          update_button.style.display = "none";
        }
      } else if (filter === "requests") {
        if (rows[i].classList.contains("requests")) {
          rows[i].style.display = "";
          update_button.style.display = "block";
        } else {
          rows[i].style.display = "none";
          update_button.style.display = "none";
        }
      }
    }
  }
}
document.addEventListener("DOMContentLoaded", function () {
  filterTable("members");
});
