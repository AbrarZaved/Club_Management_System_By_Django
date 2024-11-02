var resNotice = document.getElementById("result_notices");
resNotice.style.display = "none";

const previewButtons = document.querySelectorAll(".preview-button");
document.querySelectorAll("#filterValues .dropdown-item").forEach((item) => {
  item.addEventListener("click", function (event) {
    event.preventDefault();
    const selectedValue = this.getAttribute("data-value");
    document.getElementById("dropdownMenuButton").textContent =
      selectedValue === "All" ? "All Notices" : selectedValue;

    filterNotices(selectedValue);
  });
});

// Function to filter notices based on the selected club
function filterNotices(selectedClub) {
  var all_notices = document.getElementById("all_notices");
  var previewModal = document.getElementById("previewModal");

  // Listen for the modal's 'hidden' event

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
      console.log(data);
      resNotice.innerHTML = "";
      resNotice.style.display = "block";
      all_notices.style.display = "none";
      if (data.length > 0) {
        let rowContainer = '<div class="row">';

        data.forEach((element) => {
          const createdAt = element.created_at;
          const date = new Date(createdAt);

          const options = {
            year: "numeric",
            month: "long",
            day: "numeric",
            hour: "numeric",
            minute: "numeric",
            hour12: true,
          };

          // Format the date to a readable string
          const formattedDate = date.toLocaleString("en-US", options);

          // Update the rowContainer with formatted date
          rowContainer += `
            <div class="col-6">
              <div class="card text-white bg-success col-12">
                <h4 class="card-body text-white"><strong>${element.title}</strong></h4>
                <p class="card-body text-white">${element.description}</p>
                <div class="d-flex justify-content-between align-items-center">
                  <span class="badge bg-light text-success">${element.club_name} | ${formattedDate}</span>
                  <button class="btn btn-success btn-sm preview-button" data-toggle="modal" data-target="#previewModal" data-title="${element.title}" data-description="${element.description}" data-club="${element.club_name}" data-time="${formattedDate}">
                    <i class="material-icons">preview</i>
                  </button>
                </div>
              </div>
            </div>
          `;
        });

        rowContainer += "</div>";
        resNotice.innerHTML = rowContainer;

        // Add event listeners to preview buttons
        const newPreviewButtons = resNotice.querySelectorAll(".preview-button");
        newPreviewButtons.forEach((button) => {
          button.addEventListener("click", function () {
            const title = this.getAttribute("data-title");
            const description = this.getAttribute("data-description");
            const club = this.getAttribute("data-club");
            const time = this.getAttribute("data-time");

            // Update the modal with sliced title
            document.getElementById("preview-title").innerText =
              sliceFromLastUnderscore(title);
            document.getElementById("preview-description").innerText =
              description;
            document.getElementById("preview-club").innerText = club;
            document.getElementById("preview-time").innerText = time;
          });
        });
      } else {
        resNotice.innerHTML =
          "<p class='text-white'>No notices found for this club.</p>";
      }
    })
    .catch((error) => {
      console.error("Error fetching notices:", error);
    });
}

// Function to slice title from the last underscore and limit to 15 characters
function sliceFromLastUnderscore(title) {
  const lastUnderscoreIndex = title.lastIndexOf("_");
  return lastUnderscoreIndex > -1 ? title.slice(0, lastUnderscoreIndex) : title;
}

// Reset preview elements on page load
previewButtons.forEach((button) => {
  button.addEventListener("click", function () {
    const title = button.getAttribute("data-title");
    const description = button.getAttribute("data-description");
    const club = button.getAttribute("data-club");
    const time = button.getAttribute("data-time");

    // Update the modal with sliced title
    document.getElementById("preview-title").innerText =
      sliceFromLastUnderscore(title);
    document.getElementById("preview-description").innerText = description;
    document.getElementById("preview-club").innerText = club;
    document.getElementById("preview-time").innerText = time;
  });
});

// Glowing a Notice
document.addEventListener("DOMContentLoaded", function () {
  const urlParams = window.location.pathname;
  const noticeId = urlParams.slice(8); // Replace 'id' with your parameter name
  console.log(noticeId);
  if (noticeId) {
    const targetNotice = document.getElementById(`notice-${noticeId}`);
    if (targetNotice) {
      // Apply glow effect
      targetNotice.style.transition = "box-shadow .5s ease-in-out";
      targetNotice.style.boxShadow = "0 0 20px gray";

      // Remove glow effect after .25 second
      setTimeout(() => {
        targetNotice.style.boxShadow = "none";
      }, 250);
    }
  }
});
