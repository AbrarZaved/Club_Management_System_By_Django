// Add glow effect CSS rule dynamically
const style = document.createElement("style");
style.innerHTML = `
  .glow-effect {
    transition: box-shadow 0.5s ease-in-out;
    box-shadow: 0 0 20px gray;
  }
`;
document.head.appendChild(style);

// Initialize result container and hide it initially
const resNotice = document.getElementById("result_notices");
resNotice.style.display = "none";

// Wait for the DOM to load, then filter notices and apply glow effect if needed
document.addEventListener("DOMContentLoaded", () => {
  // Flag to ensure glow effect only runs once
  let glowExecuted = false;

  // Filter notices and apply glow effect once notices are rendered
  filterNotices("All").then(() => {
    const urlParams = window.location.pathname;
    const noticeId = urlParams.slice(8); // Adjust according to your URL structure
    console.log(
      "Glowing notice with ID:",
      noticeId,
      "on page load",
      glowExecuted
    );

    if (noticeId && !glowExecuted) {
      Glow(noticeId);
      glowExecuted = true; // Set to true after first execution
    }
  });
});

// Dropdown item selection for filtering notices
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
  return fetch("/filter_notices", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: selectedClub }),
  })
    .then((res) => res.json())
    .then((data) => {
      renderNotices(data);
    })
    .catch((error) => {
      console.error("Error fetching notices:", error);
    });
}

// Render notices in result container
function renderNotices(data) {
  resNotice.innerHTML = "";
  resNotice.style.display = "block";

  if (data.length) {
    const rowContainer = data
      .map((element) => createNoticeCard(element))
      .join("");
    resNotice.innerHTML = `<div class="row">${rowContainer}</div>`;
    addPreviewListeners();
  } else {
    resNotice.innerHTML = `<div class="card">
                                    <div class="card-body" style="text-align:center;color:white">
                                        <h5><b>No Notices Found</b></h5>
                                    </div>
                                </div>`;
  }
}

// Function to create a notice card
function createNoticeCard(element) {
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

  return `
    <div class="col-6" id="notice-${element.id}">
      <div class="card text-white bg-success col-12">
        <h4 class="card-body text-white"><strong>${element.title}</strong></h4>
        <p class="card-body text-white">${element.description
          .split(" ")
          .slice(0, 10)
          .join(" ")}...</p>
        <div class="d-flex justify-content-between align-items-center">
          <span class="badge bg-light text-success">${
            element.club_name
          } | ${formattedDate}</span>
          <button class="btn btn-success btn-sm preview-button" data-toggle="modal" data-target="#previewModal"
                  data-title="${element.title}" data-description="${
    element.description
  }" data-club="${element.club_name}"
                  data-time="${formattedDate}">
            <i class="material-icons">preview</i>
          </button>
        </div>
      </div>
    </div>`;
}

// Add event listeners to preview buttons
function addPreviewListeners() {
  const previewButtons = resNotice.querySelectorAll(".preview-button");
  previewButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const title = this.getAttribute("data-title");
      const description = this.getAttribute("data-description");
      const club = this.getAttribute("data-club");
      const time = this.getAttribute("data-time");

      // Update the modal with sliced title
      document.getElementById("preview-title").innerText =
        sliceFromLastUnderscore(title);
      document.getElementById("preview-description").innerText = description;
      document.getElementById("preview-club").innerText = club;
      document.getElementById("preview-time").innerText = time;
    });
  });
}

// Function to slice title from the last underscore and limit to 15 characters
function sliceFromLastUnderscore(title) {
  const lastUnderscoreIndex = title.lastIndexOf("_");
  return lastUnderscoreIndex > -1 ? title.slice(0, lastUnderscoreIndex) : title;
}

// Function to apply a glowing effect to a notice element
function Glow(noticeId) {
  const targetNotice = document.getElementById(`notice-${noticeId}`);
  if (targetNotice) {
    targetNotice.classList.add("glow-effect");

    // Remove glow effect after 0.5 second
    setTimeout(() => {
      targetNotice.classList.remove("glow-effect");
    }, 500);
    return true;
  }
  return false;
}

// Search functionality for notices
const searchBar = document.getElementById("searchBar");
searchBar.addEventListener("keyup", (e) => {
  const searchValue = e.target.value.trim();
  console.log(searchValue);
  if (searchValue.length === 0) {
    filterNotices("All");
  } else {
    fetch("/filter_notices", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ search_value: searchValue }),
    })
      .then((res) => res.json())
      .then((result) => {
        console.log(result);
        renderNotices(result);
      })
      .catch((error) => {
        console.error("Error searching notices:", error);
      });
  }
});