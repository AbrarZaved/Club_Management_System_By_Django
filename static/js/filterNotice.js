var resNotice = document.getElementById("result_notices");
resNotice.style.display = "none";
const urlParams = window.location.pathname;
const noticeId = urlParams.slice(8); // Adjust according to your URL structure
console.log(noticeId);
if (noticeId) {
  // Call Glow after DOM content has loaded
  document.addEventListener("DOMContentLoaded", () => {
    filterNotices("All"); // Initialize with default filter
  });
}

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
  var previewModal = document.getElementById("previewModal");

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

          const formattedDate = date.toLocaleString("en-US", options);

          rowContainer += `
            <div class="col-6" id="notice-${element.id}">
              <div class="card text-white bg-success col-12">
                <h4 class="card-body text-white"><strong>${
                  element.title
                }</strong></h4>
                <p class="card-body text-white">${element.description
                  .split(" ")
                  .slice(0, 10)
                  .join(" ")}...</p>
                <div class="d-flex justify-content-between align-items-center">
                  <span class="badge bg-light text-success">${
                    element.club_name
                  } | ${formattedDate}</span>
                  <button class="btn btn-success btn-sm preview-button" data-toggle="modal" data-target="#previewModal" data-title="${
                    element.title
                  }" data-description="${element.description}" data-club="${
            element.club_name
          }" data-time="${formattedDate}">
                    <i class="material-icons">preview</i>
                  </button>
                </div>
              </div>
            </div>
          `;
        });

        rowContainer += "</div>";
        resNotice.innerHTML = rowContainer;

        // Call Glow function for the specific notice
        if (noticeId) {
          Glow(noticeId); // Pass the noticeId to the Glow function
        }

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

// Glowing a Notice
function Glow(noticeId) {
  const targetNotice = document.getElementById(`notice-${noticeId}`);
  if (targetNotice) {
    // Apply glow effect
    targetNotice.style.transition = "box-shadow .5s ease-in-out";
    targetNotice.style.boxShadow = "0 0 20px gray";

    // Remove glow effect after .25 second
    setTimeout(() => {
      targetNotice.style.boxShadow = "none";
    }, 500);
  }
}

// Search Notice
var searchBar = document.getElementById("searchBar");
searchBar.addEventListener("keyup", (e) => {
  console.log(e.target.value);
});

// Call filterNotices on page load for "All" category
document.addEventListener("DOMContentLoaded", () => {
  filterNotices("All");
});
