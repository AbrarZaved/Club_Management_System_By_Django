console.log("hello boys");
var all_clubs = document.getElementById("all_clubs");
var searchText = document.getElementById("searchBar");
var resClub = document.getElementById("result_clubs");
let clubs = [];
document.addEventListener("DOMContentLoaded", () => {
  selectedClub = "joined";
  fetch("/club_properties", {
    method: "POST",
    body: JSON.stringify({ selectedClub: selectedClub }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      if (data.length > 0) {
        data.forEach((element) => {
          clubs.push(element.club_name);
        });
      }
    });
});

resClub.style.display = "none";
document.querySelectorAll("#filterValues .dropdown-item").forEach((item) => {
  item.addEventListener("click", function (e) {
    e.preventDefault();
    const selectedClub = this.getAttribute("data-value");
    document.getElementById("dropdownMenuButton").textContent = selectedClub;
    filterClub(selectedClub);
  });
});
function all(club_name) {
  if (clubs.includes(club_name)) return true;
  else return false;
}
function filterClub(selectedClub) {
  fetch("/club_properties", {
    method: "POST",
    body: JSON.stringify({ selectedClub: selectedClub }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      if (data.length > 0) {
        resClub.innerHTML = "";
        all_clubs.style.display = "none";

        renderClub(data, selectedClub);
      }
    });
}
function searchClub(text) {
  fetch("/club_properties", {
    body: JSON.stringify({ text: text }),
    method: "POST",
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("data: ", data);
      resClub.innerHTML = "";
      all_clubs.style.display = "none";

      if (data.length === 0) {
        resClub.innerHTML = `<div class="card">
                                    <div class="card-body" style="text-align:center;color:white">
                                        <h5><b>No Clubs Found</b></h5>
                                    </div>
                                </div>`;
      } else {
        renderClub(data, searchClub);
      }
    });
}

searchText.addEventListener("keyup", (e) => {
  text = e.target.value.trim();
  console.log(text);
  if (text.length > 0) {
    searchClub(text);
  } else {
    resClub.style.display = "none";
    all_clubs.style.display = "block";
  }
});
function renderClub(data, selectedClub) {
  console.log(selectedClub);
  let rowContainer = '<div class="row">';
  resClub.style.display = "block";
  // Loop through the data and add each card to the row container

  data.forEach((element) => {
    if (selectedClub === "joined") {
      var button = ` <button type="button" class="btn btn-success" disabled="True" data-toggle="modal" data-target="#exampleModalCenter" data-club-name="">Joined</button>`;
    } else if (selectedClub === "explore") {
      var button = ` <button type="button" class="btn btn-success" data-toggle="modal" data-target="#exampleModalCenter" data-club-name="${element.club_name}">Join</button>`;
    } else {
      if (all(element.club_name)) {
        var button = ` <button type="button" class="btn btn-success" disabled="True" data-toggle="modal" data-target="#exampleModalCenter" data-club-name="">Joined</button>`;
      } else {
        var button = ` <button type="button" class="btn btn-success" data-toggle="modal" data-target="#exampleModalCenter" data-club-name="${element.club_name}">Join</button>`;
      }
    }
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
  // Close the row container
  rowContainer += "</div>";

  // Add the row container to the resClub element
  resClub.innerHTML = rowContainer;
}
