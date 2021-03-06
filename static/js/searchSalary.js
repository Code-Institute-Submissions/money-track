const searchArea = document.querySelector("#searchArea");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tableBody = document.querySelector(".table-body");
const noResults = document.querySelector(".no-results");
tableOutput.style.display = "none";

searchArea.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = "none";
        tableBody.innerHTML = "";
        fetch("/salary/search-salary", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                appTable.style.display = "none";
                tableOutput.style.display = "block";

                console.log("data.length", data.length);

                if (data.length === 0) {
                    noResults.style.display = "block";
                    tableOutput.style.display = "none";
                } else {
                    noResults.style.display = "none";
                    data.forEach((item) => {
                        tableBody.innerHTML += `
                        <tr>

                        <td>${item.amount}</td>
                        <td>${item.source}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>

                        </tr>`;
                    });
                }
            });
    } else {
        noResults.style.display = "none";
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
    }
});