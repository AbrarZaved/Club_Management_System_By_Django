document.addEventListener("DOMContentLoaded", function () {
  var rows = document.getElementById("clubTable").getElementsByTagName("tr");
  var hasRequests = false;

  // Check if there are any rows with the "requests" class
  for (var i = 0; i < rows.length; i++) {
    if (rows[i].classList.contains("requests")) {
      hasRequests = true;
      break; // Exit loop early if we find a request
    }
  }

  // Call filterTable based on the presence of request rows
  if (hasRequests) {
    filterTable("requests");
  } else {
    filterTable("members");
  }
});

function filterTable(filter) {
  var rows = document.getElementById("clubTable").getElementsByTagName("tr");
  var update_button = document.getElementById("update_button");
  var noReq = document.getElementById("no-req");
  var noMem = document.getElementById("no-mem");
  var header = document.getElementById("header");
  var approve = document.getElementById("approve");
  var rowLength = rows.length;
  var anyRequestsVisible = false;
  var anyMembersVisible = false;

  for (var i = 0; i < rowLength; i++) {
    var row = rows[i];

    if (filter === "members") {
      if (row.classList.contains("members")) {
        row.style.display = "";
        anyMembersVisible = true;
      } else {
        row.style.display = "none";
      }
    } else if (filter === "requests") {
      if (row.classList.contains("requests")) {
        row.style.display = "";
        anyRequestsVisible = true;
      } else {
        row.style.display = "none";
      }
    }
  }

  // Header and other elements visibility
  if (filter === "members") {
    header.style.display = anyMembersVisible ? "table-row" : "none";
    approve.style.display = "none";
    noMem.style.display = anyMembersVisible ? "none" : "block";
    noReq.style.display = "none";
    update_button.style.display = "none"; // Hide button for members
  } else if (filter === "requests") {
    header.style.display = anyRequestsVisible ? "table-row" : "none";
    noReq.style.display = anyRequestsVisible ? "none" : "block";
    approve.style.display = anyRequestsVisible ? "block" : "none";
    noMem.style.display = "none";
    update_button.style.display = anyRequestsVisible ? "block" : "none"; // Show/hide based on requests
  }
}
