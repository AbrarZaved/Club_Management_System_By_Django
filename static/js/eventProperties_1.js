// Get DOM elements
var searchBar = document.getElementById("searchBar");
var allEvents = document.getElementById("all_events");
var searchResults = document.getElementById("search_results");
document.addEventListener("DOMContentLoaded", () => {
  let glowed = false;
  filterEvents("All Events").then(() => {
    const urlParams = window.location.pathname;
    const eventId = urlParams.slice(20); // Assuming event ID is at position 20 in the path
    console.log(eventId);
    if (eventId & !glowed) {
      Glow(eventId);
      glowed = true;
    }
  });
});

var selectedValue = "All Events";
document.querySelectorAll("#filterValues .dropdown-item").forEach((item) => {
  item.addEventListener("click", function (event) {
    event.preventDefault();
    selectedValue = this.getAttribute("data-value");
    document.getElementById("dropdownMenuButton").innerText = selectedValue;
    console.log(selectedValue);
    filterEvents(selectedValue);
  });
});

function filterEvents(selectedClub) {
  return fetch("http://127.0.0.1:8000/event/event_filter", {
    method: "POST",
    body: JSON.stringify({ selectedClub: selectedClub }),
    headers: { "Content-Type": "application/json" },
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      searchResults.innerHTML = "";
      if (data.length > 0) {
        allEvents.style.display = "none"; // Hide all events
        searchResults.style.display = "block"; // Show search results

        let cardsHTML = ""; // Initialize an empty string for the cards
        cardsHTML += render_events(data);

        // Wrap all the cards inside a row
        searchResults.innerHTML = `<div class="row">${cardsHTML}</div>`;
      }
    });
}
// Style for glow effect
const style = document.createElement("style");
style.innerHTML = `
    .glow-effect {
      transition: transform 0.5s ease-in-out, box-shadow .6s ease-in-out;
      box-shadow: 0 0 30px rgba(169, 169, 169, 0.8); /* Gray outline */
      transform: scale(1.05); /* Make the element bigger */
    }

    .glow-effect.shrink {
      transform: scale(1); /* Shrink back to normal size */
      box-shadow: 0 0 10px rgba(169, 169, 169, 0.5); /* Slight gray outline when shrunk */
    }
`;

document.head.appendChild(style);

// Glow effect function

// Search text truncation function
function truncate(text) {
  if (!text) return ""; // Handle empty or null text
  const words = text.split(" "); // Split text into words
  if (words.length <= 10) {
    return text; // If text has 10 or fewer words, return as is
  }
  return words.slice(0, 10).join(" ") + "..."; // Return the first 10 words followed by "..."
}

// Add event listener to search bar
searchBar.addEventListener("keyup", (e) => {
  const text = e.target.value.trim(); // Get input value and trim whitespace

  if (text.length > 0) {
    glowed = true;
    fetch("http://127.0.0.1:8000/event/event_search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Network response was not ok");
        }
        return res.json();
      })
      .then((data) => {
        console.log(data);
        searchResults.innerHTML = "";
        if (data.length > 0) {
          allEvents.style.display = "none"; // Hide all events
          searchResults.style.display = "block"; // Show search results

          let cardsHTML = ""; // Initialize an empty string for the cards
          cardsHTML += render_events(data);

          // Wrap all the cards inside a row
          searchResults.innerHTML = `<div class="row">${cardsHTML}</div>`;

          // Apply glow effect to the event found in the search results
          // Ensure this works after rendering search results
        } else {
          allEvents.style.display = "none";
          searchResults.style.display = "block";
          searchResults.innerHTML = `
              <div class="card">
                <div class="card-body" style="text-align:center;color:white">
                  <h5><b>No Events Found</b></h5>
                </div>
              </div>`;
        }
      })
      .catch((error) => {
        console.error("Error fetching search results:", error);
        searchResults.innerHTML = "<p>Error fetching search results.</p>";
      });
  } else {
    // Clear results and show all events when input is cleared
    searchResults.innerHTML = "";
    filterEvents(selectedValue);
    searchResults.style.display = "block";
    allEvents.style.display = "none";
  }
});
function render_events(data) {
  let cardsHTML = "";
  data.forEach((element) => {
    cardsHTML += `
                <div class="col-md-4 mb-4">
                  <div class="card" style="width: 18rem;" id="event-${
                    element.id
                  }">
                    <!-- Carousel for Images -->
                    <div id="carousel-${
                      element.id
                    }" class="carousel slide" data-ride="carousel">
                      <div class="carousel-inner">
                        <div class="carousel-item active">
                          <img src="/media/${
                            element.event_image1
                          }" class="d-block w-100" alt="Event Image 1">
                        </div>
                        ${
                          element.event_image2
                            ? `
                          <div class="carousel-item">
                            <img src="/media/${element.event_image2}" class="d-block w-100" alt="Event Image 2">
                          </div>
                        `
                            : ""
                        }
                        ${
                          element.event_image3
                            ? `
                          <div class="carousel-item">
                            <img src="/media/${element.event_image3}" class="d-block w-100" alt="Event Image 3">
                          </div>
                        `
                            : ""
                        }
                      </div>
                      <!-- Carousel controls -->
                      <a class="carousel-control-prev" href="#carousel-${
                        element.id
                      }" role="button" data-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="sr-only">Previous</span>
                      </a>
                      <a class="carousel-control-next" href="#carousel-${
                        element.id
                      }" role="button" data-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="sr-only">Next</span>
                      </a>
                    </div>
                    <div class="card-body">
                      <h5 class="card-title">${element.event_name}</h5>
                      <p class="card-text">${truncate(
                        element.event_description
                      )}</p>
                      <div class="d-flex justify-content-between">
                        <button type="button" class="btn btn-info" data-toggle="modal" data-target="#previewModal-${
                          element.id
                        }">
                          View More
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              `;
  });
  return cardsHTML;
}
function Glow(eventId) {
  const targetNotice = document.getElementById(`event-${eventId}`);
  if (targetNotice) {
    targetNotice.classList.add("glow-effect");

    // Remove glow effect after 0.5 seconds
    setTimeout(() => {
      targetNotice.classList.remove("glow-effect");
    }, 600);
    return true;
  } else {
    console.error(`Element with id 'event-${eventId}' not found`);
  }
  return false;
}
