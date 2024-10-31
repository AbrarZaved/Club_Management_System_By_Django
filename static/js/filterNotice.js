var resNotice = document.getElementById("result_notices");
resNotice.style.display = "none";

document.querySelectorAll("#filterValues .dropdown-item").forEach((item) => {
  item.addEventListener("click", function (event) {
    event.preventDefault();
    const selectedValue = this.getAttribute("data-value");
    if (selectedValue === "All") {
      document.getElementById("dropdownMenuButton").textContent = "All Notices";
    } else {
      document.getElementById("dropdownMenuButton").textContent = selectedValue;
    }

    filterNotices(selectedValue);
  });
});

// Function to filter notices based on the selected club
function filterNotices(selectedClub) {
  var all_notices = document.getElementById("all_notices");

  if (selectedClub === "All") {
    all_notices.style.display = "block";
    resNotice.style.display = "none";
    return;
  }

  fetch("/filter_notices", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: selectedClub }),
  })
    .then((res) => res.json())
    .then((data) => {
      resNotice.innerHTML = "";
      resNotice.style.display = "block";
      all_notices.style.display = "none";
      if (data.length > 0) {
        let rowContainer = '<div class="row">';

        data.forEach((element) => {
          rowContainer += `
            <div class="col-6">
              <div class="card text-white bg-success col-12">
                <h4 class="card-body text-white"><strong>${element.title}</strong></h4>
                <p class="card-body text-white">${element.description}</p>
              </div>
            </div>
          `;
        });

        rowContainer += "</div>";
        resNotice.innerHTML = rowContainer;
      } else {
        resNotice.innerHTML =
          "<p class='text-white'>No notices found for this club.</p>";
      }
    })
    .catch((error) => {
      console.error("Error fetching notices:", error);
    });
}
