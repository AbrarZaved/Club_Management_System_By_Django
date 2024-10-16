console.log("hello boys");
var all_clubs = document.getElementById("all_clubs");
var searchText = document.getElementById("searchBar");
var resClub = document.getElementById("result_clubs");
resClub.style.display = "none";
searchText.addEventListener("keyup", (e) => {
  text = e.target.value.trim();
  console.log(text);
  if (text.length > 0) {
    fetch("/search_clubs", {
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
          let rowContainer = '<div class="row">';
          resClub.style.display = "block";
          // Loop through the data and add each card to the row container
          data.forEach((element) => {
            rowContainer += `
                                <div class="col-md-4">
                                <div class="card mb-3" style="width: 18rem;">
                                    <img src="/media/${element.image}" class="card-img-top" alt="...">
                                    <div class="card-body">
                                    <h5 class="card-title">${element.club_name}</h5>
                                    <p class="card-text">${element.about_club}</p>
                                    <div class="d-flex justify-content-between">
                                        <a href="${element.club_link}" class="btn btn-primary">View More</a>
                                        <button type="button" class="btn btn-success" data-toggle="modal" data-target="#exampleModalCenter" data-club-name="${element.club_name}">
                                        Join
                                        </button>
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
      });
  } else {
    resClub.style.display = "none";
    all_clubs.style.display = "block";
  }
});
