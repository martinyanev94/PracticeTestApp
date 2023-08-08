        const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
tableOutput.style.display = "none";
const paginationContainer = document.querySelector(".pagination-container");
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");


searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tbody.innerHTML = "";

    fetch("/my-tests/search-test", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        appTable.style.display = "none";
        tableOutput.style.display = "block";
        console.log(data);
        if (data.length === 0) {
          noResults.style.display = "block";
          tableOutput.style.display = "none";
        } else {
          noResults.style.display = "none";
          data.forEach((item) => {
            tbody.innerHTML += `
              <tr>
                <td>${item.header}</td>
                <td>${item.notes}</td>
                <td>${item.num_questions}</td>
                <td>${item.created_at}</td>
                <td>
                  <a href="#" class="btn btn-secondary btn-sm edit-button" data-id="${item.id}">Edit</a>
                </td>
                <td>
                  <a href="#" class="btn btn-danger btn-sm delete-button" data-id="${item.id}">Delete</a>
                </td>
              </tr>
            `;
          });

          // Attach event listeners to dynamically created buttons
          attachButtonEventListeners();
        }
      });
  } else {
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});

function attachButtonEventListeners() {
  const editButtons = document.querySelectorAll(".edit-button");
  const deleteButtons = document.querySelectorAll(".delete-button");
   const downloadStudentViewButtons = document.querySelectorAll(".download-student-view");

  editButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      const id = e.target.getAttribute("data-id");
      const editUrl = `/my-tests/edit-test/${id}`;
      window.location.href = editUrl;
    });
  });

  deleteButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      const id = e.target.getAttribute("data-id");
      if (confirmDelete()) {
        const deleteUrl = `/my-tests/delete-test/${id}`;
        window.location.href = deleteUrl;
      }
    });
  });
    deleteButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      const id = e.target.getAttribute("data-id");
      if (confirmDelete()) {
        const deleteUrl = `/my-tests/delete-test/${id}`;
        window.location.href = deleteUrl;
      }
    });
  });
      downloadStudentViewButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      const id = e.target.getAttribute("data-id");
      if (confirmDelete()) {
        const downloadStudentViewUrl = `/my-tests/download-student-view/${id}`;
        window.location.href = deleteUrl;
      }
    });
  });

}
