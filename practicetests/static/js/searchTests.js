const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
tableOutput.style.display = "none";
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
                    <a
            href="{% url 'edit-test' user_tests.id  %}"
            class="btn btn-secondary btn-sm"
            >Edit</a
          >

        </td>
          <td>
                    <a
            href="{% url 'delete-test' user_tests.id  %}"
            class="btn btn-danger btn-sm"
            >Delete</a
          >
        </td>
      </tr>
          `;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
});
