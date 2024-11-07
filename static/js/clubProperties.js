console.log("hello boys");

var all_clubs = document.getElementById("all_clubs");
var searchText = document.getElementById("searchBar");
var resClub = document.getElementById("result_clubs");
let clubs = [];

// Wait until the DOM is fully loaded before making the fetch call
document.addEventListener("DOMContentLoaded", () => {
  selectedClub = "joined"; // Default selection
  fetch("/club_properties", {
    method: "POST",
    body: JSON.stringify({ selectedClub: selectedClub }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      if (data.length > 0) {
        data.forEach((element) => {
          clubs.push(element.club_name); // Push club names into the array
        });
      }
    });
});

// Initially hide the result container
resClub.style.display = "none";

// Add event listeners to filter options
document.querySelectorAll("#filterValues .dropdown-item").forEach((item) => {
  item.addEventListener("click", function (e) {
    e.preventDefault();
    const selectedClub = this.getAttribute("data-value");
    document.getElementById("dropdownMenuButton").textContent = selectedClub;
    filterClub(selectedClub); // Filter clubs based on selection
  });
});

// Function to check if a club is in the list of joined clubs
function all(club_name) {
  if (clubs.includes(club_name)) return true;
  else return false;
}

// Function to filter clubs based on selected category
function filterClub(selectedClub) {
  fetch("/club_properties", {
    method: "POST",
    body: JSON.stringify({ selectedClub: selectedClub }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      if (data.length > 0) {
        resClub.innerHTML = ""; // Clear previous results
        all_clubs.style.display = "none"; // Hide the club list

        renderClub(data, selectedClub); // Render filtered clubs
      }
    });
}

// Function to search clubs based on input text
function searchClub(text) {
  fetch("/club_properties", {
    body: JSON.stringify({ text: text }),
    method: "POST",
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("data: ", data);
      resClub.innerHTML = ""; // Clear previous results
      all_clubs.style.display = "none"; // Hide the club list

      // Show message if no clubs are found
      if (data.length === 0) {
        resClub.innerHTML = `<div class="card">
                                    <div class="card-body" style="text-align:center;color:white">
                                        <h5><b>No Clubs Found</b></h5>
                                    </div>
                                </div>`;
      } else {
        renderClub(data, searchClub); // Render the clubs found
      }
    });
}

// Event listener for search input
searchText.addEventListener("keyup", (e) => {
  text = e.target.value.trim(); // Get trimmed search text
  console.log(text);
  if (text.length > 0) {
    searchClub(text); // Call search function if there's input
  } else {
    resClub.style.display = "none"; // Hide results if search bar is empty
    all_clubs.style.display = "block"; // Show all clubs
  }
});

// Function to render the club cards dynamically
function renderClub(data, selectedClub) {
  console.log(selectedClub);
  let rowContainer = '<div class="row">'; // Start the row for clubs
  resClub.style.display = "block"; // Show the result container

  // Loop through the data and add each card to the row container
  data.forEach((element) => {
    // Set button text based on the selected club type
    let button;
    if (selectedClub === "joined") {
      button = ` <button type="button" class="btn btn-success" disabled="True" data-toggle="modal" data-target="#exampleModalCenter" data-club-name="">Joined</button>`;
    } else if (selectedClub === "explore") {
      button = ` <button type="button" class="btn btn-success" data-toggle="modal" data-target="#exampleModalCenter" data-club-name="${element.club_name}">Join</button>`;
    } else {
      // If club is already joined, disable button
      if (all(element.club_name)) {
        button = ` <button type="button" class="btn btn-success" disabled="True" data-toggle="modal" data-target="#exampleModalCenter" data-club-name="">Joined</button>`;
      } else {
        button = ` <button type="button" class="btn btn-success" data-toggle="modal" data-target="#exampleModalCenter" data-club-name="${element.club_name}">Join</button>`;
      }
    }

    // Add club card to the row container
    rowContainer += `
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
  });

  rowContainer += "</div>"; // Close the row container

  // Add the row container to the resClub element
  resClub.innerHTML = rowContainer;
}
