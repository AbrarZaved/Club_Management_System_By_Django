console.log("hello boys");

const all_clubs = document.getElementById("all_clubs");
const searchText = document.getElementById("searchBar");
const resClub = document.getElementById("result_clubs");

let clubs = [];
let selectedClub = "joined"; // default club selection

// Fetch clubs data when the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  fetchClubs(selectedClub);
});

// Fetch clubs data based on selected club or search text
function fetchClubs(query) {
  const bodyData = query === "search" ? { text: searchText.value.trim() } : { selectedClub: query };
  
  fetch("/club_properties", {
    method: "POST",
    body: JSON.stringify(bodyData),
  })
  .then(res => res.json())
  .then(data => {
    console.log(data);
    renderClubs(data, query);
  });
}

// Render clubs based on the fetched data
function renderClubs(data, clubType) {
  resClub.innerHTML = "";
  all_clubs.style.display = data.length ? "none" : "block";
  resClub.style.display = data.length ? "block" : "none";
  
  if (!data.length) {
    resClub.innerHTML = `<div class="card"><div class="card-body" style="text-align:center;color:white"><h5><b>No Clubs Found</b></h5></div></div>`;
    return;
  }

  const rowContainer = data.map(element => {
    const button = getClubButton(clubType, element.club_name);
    return `
      <div class="col-md-4">
        <div class="card mb-3" style="width: 18rem;">
          <img src="/media/${element.image}" class="card-img-top" alt="...">
          <div class="card-body">
            <h5 class="card-title">${element.club_name}</h5>
            <p class="card-text">${element.about_club}</p>
            <div class="d-flex justify-content-between">
              <a href="${element.club_link}" class="btn btn-primary">View More</a>
              ${button}
            </div>
          </div>
        </div>
      </div>
    `;
  }).join("");

  resClub.innerHTML = `<div class="row">${rowContainer}</div>`;
}

// Generate button based on club status
function getClubButton(clubType, clubName) {
  const isJoined = clubs.includes(clubName);
  const isDisabled = clubType === "joined" || (clubType !== "explore" && isJoined);
  const buttonText = isJoined ? "Joined" : "Join";
  const buttonClass = isDisabled ? "btn-success" : "btn-primary";
  const dataAttributes = isDisabled ? "" : `data-club-name="${clubName}"`;

  return `<button type="button" class="btn ${buttonClass}" ${dataAttributes} ${isDisabled ? 'disabled' : ''}>${buttonText}</button>`;
}

// Handle filter and search events
document.querySelectorAll("#filterValues .dropdown-item").forEach(item => {
  item.addEventListener("click", function (e) {
    e.preventDefault();
    selectedClub = this.getAttribute("data-value");
    document.getElementById("dropdownMenuButton").textContent = selectedClub;
    fetchClubs(selectedClub);
  });
});

searchText.addEventListener("keyup", (e) => {
  if (e.target.value.trim()) {
    fetchClubs("search");
  } else {
    resClub.style.display = "none";
    all_clubs.style.display = "block";
  }
});
