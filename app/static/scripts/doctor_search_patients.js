/**
###### Doctor Search Patients Scripts #######
**/

// Search Patients on Enter Key Pressed
async function searchPatientsInputOnKey (e) {
  try {
    e.preventDefault();

    if (e.key === "Enter" && e.target.value !== '') {
      await searchPatients(e.target.value);
    }
  }
  catch (error) {
    showErrorMessage(error.toString());
  }
}


// Search Patients on Search Button Clicked
async function searchPatientsButtOnPressed (e) {
  try {
    e.preventDefault();

    const searchQuery = document.getElementById("doctor-search-patients-input");

    if (!searchQuery  || (searchQuery.value) === '') {
      // set focus on input
      searchQuery.focus();
      return;
    }

    await searchPatients(searchQuery.value);
  }
  catch (error) {
    showErrorMessage(error.toString());
  }
}


// search patients
async function searchPatients (q) {
  try {
    const response = await searchPatientsRequest(q);

    if (response && response.ok) {
      const patients = await response.json();

      preateToDisplaySearchPatientResults (patients, q);
    }
    else {
      const { message } = await response.json();

      const errorMessage = message ? message : `Network Connection Error`;
      console.log(errorMessage);
      showErrorMessage(errorMessage);
    }
  }
  catch (error) {
    console.error (error);
    showErrorMessage("Something Went Wrong. Try Again!");
  }
}


function resetSearchResultsOnClicked (event) {
  event.preventDefault();
  const resultContainer = document.getElementById("doctor-search-patients-results");
  clearResultContainer(resultContainer);
}


// show search results
function preateToDisplaySearchPatientResults (patients, q) {

  const resultContainer = document.getElementById("doctor-search-patients-results");

  // clear the existing data
  clearResultContainer(resultContainer);

  displayResults(resultContainer, patients, q);
}



// clear data container and make room for new data results
function clearResultContainer (container) {
  while (container.lastChild) {
    container.removeChild(container.lastChild);
  }
}


// display search results
function displayResults (container, patients, q) {
  if (patients.length === 0) {
    // if no results were found
    showEmptyResult(container, q);
  }
  else {
    patients.forEach (
      patient => {
        container.appendChild (createPatientCard(patient));
      }
    )
  }
}


function createPatientCard (patient) {
  const card = document.createElement("div");
  card.setAttribute("class", "card mb-2 p-2");
  // card.setAttribute("id", `doc-patient-${patient.id}`);

  fillPatientsInfoInCard(card, patient);

  card.addEventListener("mouseenter", () => hoverCard(card, "on"));

  card.addEventListener("mouseleave", () => hoverCard(card, "leave"));

  card.addEventListener("click", () => viewPatientPrescriptions(patient.id));

  return card;
}


function fillPatientsInfoInCard (card, patient) {

  const firstRow = createRowAndFillData(
    "Username",
    patient.username,
    "Full Name",
    `${patient.fName} ${patient.lName}`
  );

  const secondRow = createRowAndFillData(
    "Age",
    computePatientsAge(patient.dob),
    "Gender",
    patient.gender
  )

  card.appendChild(firstRow);
  card.appendChild(secondRow);
}


function createRowAndFillData (title1, data1, title2, data2) {
  const row = document.createElement("div");
  row.setAttribute("class", "row");

  const col1 = document.createElement("div");
  col1.setAttribute("class", "col");
  const col2 = document.createElement("div");
  col2.setAttribute("class", "col");

  const col1Title = createInfoHeader(title1);
  const col1Data = createInfoDataHolder(data1);
  col1.appendChild(col1Title);
  col1.appendChild(col1Data);

  const col2Title = createInfoHeader(title2);
  const col2Data = createInfoDataHolder(data2);
  col2.appendChild(col2Title);
  col2.appendChild(col2Data);

  row.appendChild(col1);
  row.appendChild(col2);

  return row;
}


function createInfoHeader (name) {
  const span = document.createElement("span");
  span.setAttribute("class", "text-muted");
  span.innerHTML = name;
  return span;
}


function createInfoDataHolder (data) {
  const h6 = document.createElement("h6");
  h6.setAttribute("class", "text-muted");
  h6.innerHTML = data;
  return h6;
}


function computePatientsAge (birthDate) {

  const today = new Date()
  const bd = new Date(birthDate);

  // return closet age
  return today.getYear() - bd.getYear();
}


function hoverCard (card, event) {
  if (event == "on") {
    card.style.background = "gainsboro";
  }
  else {
    card.style.background = "white";
  }
}


function viewPatientPrescriptions (id) {
  window.location = `http://127.0.0.1:5000/patients/prescriptions/${id}`;
}


function showEmptyResult(resultContainer, q) {
  const emptyMessageBox = document.createElement("div");
  emptyMessageBox.setAttribute("class", "alert alert-info");
  emptyMessageBox.setAttribute("id", "empty-msg-box");
  emptyMessageBox.setAttribute("role", "alert");
  emptyMessageBox.innerHTML = `No search Result(s) related to ${q}`;
  emptyMessageBox.style.display = "block";
  resultContainer.appendChild(emptyMessageBox);
}


function showErrorMessage(message) {
  removeErrorMessage();
  const errorContainer = document.getElementById("error-div-search-patients");
  const errorMessageBox = document.createElement("div");
  errorMessageBox.setAttribute("class", "alert alert-danger");
  errorMessageBox.setAttribute("id", "error-msg-box");
  errorMessageBox.setAttribute("role", "alert");
  errorMessageBox.innerHTML = message;
  errorContainer.appendChild(errorMessageBox);
}


function removeErrorMessage() {
  const errorMessage = document.getElementById("error-msg-box");
  if (errorMessage)
    errorMessage.remove();
}


// Search Patients with keyword
async function searchPatientsRequest (q) {
  try {
    const response = fetch(`http://127.0.0.1:5000/patient/filter/${q}`, {
      method: "GET",
      headers: {
        "Content-Type" : "Application/json",
        "Accept" : "Application/json"
      }
    });

    return response;
  }
  catch (error) {
    console.error (`Error Searching Patients: ${error}`);
  }
}
