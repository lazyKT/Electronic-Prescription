const searchMedButton = document.getElementById("search-med-button");
const resetFilterButton = document.getElementById("reset-med-filter-button");

showErrorMessage(show=false);
toggleResetFilterButton(show=false);

searchMedButton.addEventListener("click", async (event) => {
    try {
      searchMedButton.innerHTML = "Loading ...";

      const searchMedInput = document.getElementById("search-med-input");
      if (!searchMedInput || searchMedInput.value === '') {
        searchMedButton.innerHTML = "Search";
        return;
      }

      toggleAllMedicinesTable(show=false);
      toggleResetFilterButton(show-true);

      const response = await searchMedicines(searchMedInput.value);

      if (response && response.ok) {
        const meds = await response.json();
        console.log(meds);
        displayMedSearchResults(meds);
      }
      else {
        const { message } = await response.json();
        const errorMessage = message ? message : "Network Connection Error";
        showErrorMessage(show=true, errorMessage);
      }
    }
    catch (error) {
      showErrorMessage(show=true, error);
    }
    finally {
      searchMedButton.innerHTML = "Search";
    }
});



function toggleAllMedicinesTable (show) {
  const allMedsTable = document.getElementById("all-meds-tbody");
  if (show)
    allMedsTable.style.display = "block";
  else
    allMedsTable.style.display = "none";
}


function toggleResetFilterButton (show) {
  if (show)
    resetFilterButton.style.display = "block";
  else
    resetFilterButton.style.display = "none";
}


function showErrorMessage (show, message) {
  const errorAlertMed = document.getElementById("error-alert-med");

  if (show) {
    errorAlertMed.style.display = "block";
    errorAlertMed.innerHTML = message;
  }
  else {
    errorAlertMed.style.display = "none";
  }
}


function displayMedSearchResults (meds) {

  showErrorMessage(show=false);
  const medSearchResultTbody = document.getElementById("search-meds");

  meds.forEach(
    med => {
      const tr = document.createElement("tr");
      createTableCell(tr, med.med_id);
      createTableCell(tr, med.medName);
      createTableCell(tr, (new Date(med.expDate)).toLocaleDateString());
      createTableCell(tr, med.price);
      createTableCell(tr, med.quantity);

      medSearchResultTbody.appendChild (tr);
    }
  );
}


function createTableCell (tr, value) {
  const td = document.createElement("td");
  const span = document.createElement("span");

  span.innerHTML = value;
  td.appendChild(span);
  tr.appendChild(td);
}


function createActionTableCell (tr, id) {
  const td = document.createElement("td");
  const div = document.createElement("div");
  div.setAttribute("class", "d-flex justify-content-start");

  const editButton = document.createElement("button");
  editButton.setAttribute("class", "btn btn-primary mx-1");
  editButton.innerHTML = '<i class="fas fa-pen"></i>';

  editButton.addEventListener("click", event => {
    window.location = `/medicines${id}`;
  });
}



async function searchMedicines (q) {
  try {
    const response = await fetch(`/medicines/search?q=${q}`, {
      method: "GET",
      headers: {
        "Content-Type" : "application/json",
        "Accept" : "application/json"
      }
    });

    return response;
  }
  catch (error) {

  }
}
