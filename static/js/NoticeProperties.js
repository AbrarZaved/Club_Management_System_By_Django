// Initialize result container and hide it initially
const resNotice = document.getElementById("result_notices");
resNotice.style.display = "none";

// Get notice ID from URL path
const noticeId = window.location.pathname.slice(8); // Adjust according to your URL structure

// Initialize page content and set up listeners
document.addEventListener("DOMContentLoaded", () => {
  filterNotices("All"); // Default filter
  if (noticeId) Glow(noticeId); // Apply glow effect if noticeId exists
});

// Dropdown filter for notices
document.querySelectorAll("#filterValues .dropdown-item").forEach((item) => {
  item.addEventListener("click", function (event) {
    event.preventDefault();
    const selectedValue = this.getAttribute("data-value");
    document.getElementById("dropdownMenuButton").textContent =
      selectedValue === "All" ? "All Notices" : selectedValue;
    filterNotices(selectedValue);
  });
});

// Fetch and display notices based on selected filter or search
function filterNotices(filter) {
  fetch("/filter_notices", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: filter }),
  })
    .then((res) => res.json())
    .then((data) => renderNotices(data))
    .catch((error) => console.error("Error fetching notices:", error));
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
                                </div>`;;
  }
}

// Create notice card HTML
function createNoticeCard(element) {
  const formattedDate = new Date(element.created_at).toLocaleString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
    hour12: true,
  });
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
  }" data-club="${element.club_name}" data-time="${formattedDate}">
            <i class="material-icons">preview</i>
          </button>
        </div>
      </div>
    </div>`;
}

// Add preview modal listeners
function addPreviewListeners() {
  resNotice.querySelectorAll(".preview-button").forEach((button) => {
    button.addEventListener("click", () => {
      const title = button.getAttribute("data-title");
      document.getElementById("preview-title").innerText =
        sliceFromLastUnderscore(title);
      document.getElementById("preview-description").innerText =
        button.getAttribute("data-description");
      document.getElementById("preview-club").innerText =
        button.getAttribute("data-club");
      document.getElementById("preview-time").innerText =
        button.getAttribute("data-time");
    });
  });
}

// Search functionality
document.getElementById("searchBar").addEventListener("keyup", (e) => {
  const searchValue = e.target.value.trim();
  if (searchValue) {
    fetch("/filter_notices", {
      method: "POST",
      body: JSON.stringify({ search_value: searchValue }),
    })
      .then((res) => res.json())
      .then((result) => renderNotices(result));
  } else {
    filterNotices("All");
  }
});

// Apply a glowing effect to a notice element
function Glow(noticeId) {
  const targetNotice = document.getElementById(`notice-${noticeId}`);
  if (targetNotice) {
    targetNotice.style.transition = "box-shadow .5s ease-in-out";
    targetNotice.style.boxShadow = "0 0 20px gray";
    setTimeout(() => (targetNotice.style.boxShadow = "none"), 500);
  }
}

// Slice title from the last underscore
function sliceFromLastUnderscore(title) {
  const lastUnderscoreIndex = title.lastIndexOf("_");
  return lastUnderscoreIndex > -1 ? title.slice(0, lastUnderscoreIndex) : title;
}
