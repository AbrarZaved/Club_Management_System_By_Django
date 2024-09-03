console.log("Hello Boys");

var noRes = document.getElementById("no-res");
var serTable = document.getElementById("searchTable");
var memTable = document.getElementById("memberTable");
var resultTable = document.getElementById("resultTable");
var header = document.getElementById("serHeader"); // Corrected variable name
var total = document.getElementById("total-students");

header.style.display = "none";
serTable.style.display = "none";
noRes.style.display = "none";

var search = document.getElementById("searchBar");
search.addEventListener("keyup", (e) => {
  const searchText = e.target.value.trim();
  console.log(searchText);

  if (searchText.length > 0) {
    fetch("http://127.0.0.1:8000/member/search_member", {
      body: JSON.stringify({ searchText: searchText }),
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        resultTable.innerHTML = ""; // Clear previous results
        memTable.style.display = "none";
        serTable.style.display = "table"; // Show the search table
        console.log("data: ",data);
        if (data.length === 0) {
          //alert("No Results Found");
          noRes.style.display = "block";
          noRes.style.textAlign = "center";
          header.style.display = "none"; // Show the 'No Members Found' row
          total.style.display = "none";
        } else {
          noRes.style.display = "none";
          header.style.display = "table-row"; // Show the header row
          total.style.display = "block";
          total.innerHTML = `<h5><b>Total Member(s) Found: ${data.length}</b></h5>`;
          data.forEach((element) => {
            resultTable.innerHTML += `
              <tr>
                <td style="text-align: center;">${element.student__student_id}</td>
                <td style="text-align: center;">${element.student__first_name}</td>
                <td style="text-align: center;">${element.student__last_name}</td>
                <td style="text-align: center;">${element.club__club_name}</td>
                <td style="text-align: center;"><a href="{% url 'edit' view_member.id %}"><i class="bi bi-yelp"></i></a></td>
              </tr>`;
          });
        }
      })
      .catch((err) => {
        console.log("Error: ", err);
      });
  } else {
    // When search text is cleared, reset the display
    serTable.style.display = "none";
    memTable.style.display = "table"; // Show the original member table
    header.style.display = "none"; // Hide the header when no search is active
    total.style.display = "none";
  }
});
