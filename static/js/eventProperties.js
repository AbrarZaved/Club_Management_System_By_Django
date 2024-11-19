document.addEventListener("DOMContentLoaded", () => {
  const accordion = document.getElementById("accordionExample");

  // Object to store total counts for each event
  let eventTotalCounts = {};

  // Define a set of colors
  const colors = [
    "#4B0082",
    "#2C3E50",
    "#8B0000",
    "#006400",
    "#800080",
    "#4B0082",
    "#D2691E",
    "#4F4A4A",
    "#3E2723",
    "#2E4053",
  ];

  // Fetch data from the server on page load
  fetch("event_properties", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      accordion.innerHTML = ""; // Clear existing content

      if (data && data.length > 0) {
        data.forEach((element, index) => {
          eventTotalCounts[element.event_name] = element.total_count;

          // Prepare the attendees table or fallback message
          let attendees = "";
          let tableHeader = "";
          let attendeesHTML = "";
          if (element.attendees && element.attendees.length > 0) {
            element.attendees.forEach((attendee) => {
              attendees = `Attendees`;
              tableHeader = `<thead class="small text-uppercase bg-dark text-white">
                              <tr>
                                <th class="text-center">Name</th>
                                <th class="text-center">ID</th>
                                <th class="text-center">Email</th>
                                <th class="text-center">Phone Number</th>
                                <th class="text-center">Attended Date</th>
                                <th class="text-center">Action</th>
                              </tr>
                            </thead>`;
              attendeesHTML += ` 
                <tr class="align-middle attendee-row" data-attendee-id="${attendee.id}">
                  <td class="text-center">${attendee.full_name}</td>
                  <td class="text-center">${attendee.student_id}</td>
                  <td class="text-center">${attendee.email}</td>
                  <td class="text-center">${attendee.phone_number}</td>
                  <td class="text-center">${attendee.attended_at}</td>
                  <td class="text-center">
                    <a class="btn btn-info" href="javascript:void(0);" role="button">
                      <i class="material-icons">preview</i>
                    </a>
                    <a class="btn btn-danger delete-button" href="javascript:void(0);" role="button" data-attendee-id="${attendee.student_id}" data-event-name="${element.event_name}">
                      <i class="material-icons">delete</i>
                    </a>
                  </td>
                </tr>`;
            });
          } else {
            attendeesHTML = `
              <div class="card">
                <div class="card-body" style="text-align:center;color:white">
                  <h5><b>No Attendees</b></h5>
                </div>
              </div>`;
          }

          // Assign a color to the card based on its index
          const cardColor = colors[index % colors.length];

          // Add the event card to the accordion
          accordion.innerHTML += `
            <div class="card mb-3 shadow">
              <div class="card-header d-flex justify-content-between align-items-center text-white" id="heading${index}" style="border-radius: 0.5rem; background-color:${cardColor};">
                <h4 class="mb-0">
                  <button class="btn btn-link text-white text-decoration-none" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${index}" aria-expanded="false" aria-controls="collapse${index}" style="font-size: 1.1rem; padding-left: 0;">
                    <i class="material-icons">arrow_forward_ios</i> ${
                      element.event_name
                    }
                  </button>
                </h4>
                <span class="badge bg-light text-dark py-2 px-3 rounded-pill" style="font-size: 0.9rem;" id="total-count-${
                  element.event_name
                }">
                  Total Attendees: ${eventTotalCounts[element.event_name]}
                </span>
              </div>

              <div id="collapse${index}" class="collapse" aria-labelledby="heading${index}" data-parent="#accordionExample">
                <div class="container py-3">
                  <div class="row">
                    <div class="col-12 mb-3">
                      <div class="overflow-hidden card table-nowrap table-card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                          <h5 class="mb-0" style="color:white">${attendees}</h5>
                        </div>
                        <div class="table-responsive">
                          <table class="table table-bordered mb-0">
                            ${tableHeader}
                            <tbody>
                              ${attendeesHTML}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>`;

          // Add delete button functionality
          const deleteButtons = document.querySelectorAll(".delete-button");
          deleteButtons.forEach((button) => {
            button.addEventListener("click", function () {
              const attendeeId = this.getAttribute("data-attendee-id");
              const eventName = this.getAttribute("data-event-name");
              const row = this.closest(".attendee-row");

              const csrftoken = document.querySelector(
                "[name=csrfmiddlewaretoken]"
              ).value;

              fetch(`delete_event_attendee/${attendeeId}/${eventName}`, {
                method: "DELETE",
                headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": csrftoken,
                },
              })
                .then((response) => response.json())
                .then((data) => {
                  if (data.message) {
                    eventTotalCounts[eventName] -= 1;

                    const totalCountElement = document.getElementById(
                      `total-count-${eventName}`
                    );
                    totalCountElement.textContent = `Total Attendees: ${eventTotalCounts[eventName]}`;

                    if (eventTotalCounts[eventName] === 0) {
                      const table = row.closest(".card");
                      if (table) {
                        table.innerHTML = `
                          <tr>
                            <td colspan="6" class="text-center text-white">
                              <div class="card">
                                <div class="card-body" style="text-align:center;color:white">
                                  <h5><b>No Attendees</b></h5>
                                </div>
                              </div>
                            </td>
                          </tr>`;
                      }
                    }

                    row.style.transition =
                      "opacity 0.5s ease-out, height 0.5s ease-out";
                    row.style.opacity = "0";
                    row.style.height = "0";

                    setTimeout(() => row.remove(), 500);
                  } else {
                    console.error(data.error);
                    alert("Error: " + data.error);
                  }
                });
            });
          });
        });
      }
    })
    .catch((err) => console.error("Error fetching data:", err));
});
