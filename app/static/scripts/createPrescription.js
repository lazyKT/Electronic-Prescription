const medicines = [
  "Panadol",
  "Dicogin",
  "Dolphinal",
  "Fluza",
  "Biogesic",
  "Konidin",
  "Strapcils",
  "Panadol",
  "Dicogin",
  "Dolphinal",
  "Fluza",
  "Biogesic",
  "Konidin",
  "Strapcils",
  "Panadol",
  "Dicogin",
  "Dolphinal",
  "Fluza",
  "Biogesic",
  "Konidin",
  "Strapcils",
  "Panadol",
  "Dicogin",
  "Dolphinal",
  "Fluza",
  "Biogesic",
  "Konidin",
  "Strapcils",
  "Panadol",
  "Dicogin",
  "Dolphinal",
  "Fluza",
  "Biogesic",
  "Konidin",
  "Strapcils"
];

let searchData

window.onload = () => {
  // DOM Nodes
  const errorMessageBoxPresc = document.getElementById('error-message-presc');
  const modalContainer = document.getElementById("modal-container");
  const patientInput = document.getElementById("patient");
  const pharmacistInput = document.getElementById("pharmacist");
  const searchBtn = document.getElementById("search-btn");
  const medsList = document.getElementById("meds-list");
  const closeModalBtn = document.getElementById("dismiss-modal");
  const medModal = document.getElementById("med-modal-container");
  const closeMedicationModal = document.getElementById("dismiss-med-modal");
  const addMedtoList = document.getElementById("add-med");
  const addMedicineButton = document.getElementById("add-med-button");
  const medicationList = document.getElementById("medication");
  const createPrescriptionButton = document.getElementById("create-prescription"); // submit

  // add medicines in medicine list
  populateMedsList(medsList);
  errorMessageBoxPresc.style.display = 'none';

  // choose patient
  patientInput.addEventListener("focus", () => {
    openModal(modalContainer);
    document.getElementById("search-input").focus();
    document.getElementById("search-input").setAttribute('placeholder', 'Search Patients');
    document.getElementById("modal-title").innerHTML = "Search Patients";
    searchData = 'patient';
  });

  pharmacistInput.addEventListener("focus", () => {
    openModal(modalContainer);
    document.getElementById("search-input").focus();
    document.getElementById("search-input").setAttribute('placeholder', 'Search Pharmacists');
    document.getElementById("modal-title").innerHTML = "Search Pharmacist";
    searchData = 'pharmacist';
  });

  // search patient
  searchBtn.addEventListener("click", async (e) => {
    try {
      const searchKeyWord = document.getElementById("search-input").value;

      if (!searchKeyWord || searchKeyWord === "") return;

      clearResults();

      const results = await filterRequest(searchKeyWord);

      appendResults(results);
    }
    catch (error) {
      console.log(`Error fetching ${searchData} filtered request`, error);
    }
  });

  // add medicine
  addMedicineButton.addEventListener("click", (e) => openModal(medModal));

  // close patient/pharmacy modals
  closeModalBtn.addEventListener("click", (e) => closeModal(modalContainer));

  // close medication modal
  closeMedicationModal.addEventListener("click", (e) => closeModal(medModal));

  /* add medication to the medication list */
  addMedtoList.addEventListener("click", (e) => {
    const medName = document.getElementById("med-input")?.value;
    const medFreq = document.getElementById("med-freq")?.value;
    const extraNote = document.getElementById("extra-note-meds")?.value;

    if (!medName || medName === "" || !medFreq || medFreq === "") return;

    console.log(medName);
    console.log(medFreq);
    console.log(extraNote);

    addMedToMedicationList({ medName, medFreq, extraNote }, medicationList);

    closeModal(medModal);
  });

  /* create prescription | submit button click event */
  createPrescriptionButton.addEventListener('click', async e => {
    try {
      const patient = patientInput.dataset.patientId;
      const pharmacist = pharmacistInput.dataset.pharmacistId;
      const fromDate = document.getElementById('from_date').value;
      const toDate = document.getElementById('to_date').value;

      console.log(fromDate, toDate);

      if (!pharmacist || pharmacist === '' || !patient || patient === '' || !fromDate || fromDate === '' || !toDate || toDate === '')
        return;

      if (medicationList.childNodes.length <= 1)
        return;

      /* formated medication string: seperate each by comma */
      let medStr = "";
      medicationList.childNodes.forEach( (node, idx) => {
        if (idx !== 0) {
          const medName = `med-name-${idx}`;
          const medFreq = `med-freq-${idx}`;
          const delimeter = idx === 1 ? '' : ', ';
          medStr += `${document.getElementById(medName).innerHTML} ${document.getElementById(medFreq).innerHTML} ${delimeter}`;
        }
      });

      const response = await createPrescriptionRequest({ patient, pharmacist, medStr, fromDate, toDate});

      if (response.ok) {
        window.location = '/doctor/dashboard';
      }
      else {
        const json = await response.json();
        console.log(json); //DEBUG
      }

    }
    catch (error) {
      console.log('Error fetching create prescriptions request', error);
      errorMessageBoxPresc.style.display = 'block';
      if (error)
        errorMessageBoxPresc.innerHTML = error;
      else
        errorMessageBoxPresc.innerHTML = "Internal Server Error!";
    }
  });

};

function openModal(modal) {
  modal.style.display = "flex";
}

function closeModal(modal) {
  modal.style.display = "none";
}

function appendResults(results) {

  const resultContainer = document.getElementById("result-container");

  results.forEach((res) => {
    const { fName, lName, username, id } = res;

    const div = document.createElement("div");
    div.setAttribute("class", "d-flex justify-content-between my-2 result");

    const name = document.createElement("h6");
    name.setAttribute("class", "text-muted");
    name.innerHTML = `${fName} ${lName} @${username}`;

    const btn = document.createElement("button");
    btn.setAttribute("class", "btn btn-success");
    btn.innerHTML = "Select";

    div.appendChild(name);
    div.appendChild(btn);

    resultContainer.appendChild(div);
    resultContainer.appendChild(document.createElement("hr"));

    // chose patient/pharmacist
    btn.addEventListener("click", () => {
      const modalContainer = document.getElementById("modal-container");

      modalContainer.style.display = "none"; // hide modal
      clearResults(); // clear results
      (document.getElementById('search-input')).value = ''; // clear the search input

      const input = searchData === 'patient'
          ? document.getElementById("patient")
          : document.getElementById('pharmacist');
      input.value = `${fName} ${lName}`; // show Full Name
      input.setAttribute(`data-${searchData}-id`, id); // set id of patient/pharmacist in dataset attribute
      closeModal(modalContainer); // close the modal
    });
  });
}


/* clear search results */
function clearResults() {
  const resultContainer = document.getElementById("result-container");
  while (resultContainer.lastChild) {
    resultContainer.removeChild(resultContainer.lastChild);
  }
}


/* add medicine list in search category */
function populateMedsList(medsList) {
  medicines.forEach((f) => {
    const option = document.createElement("option");
    option.setAttribute("value", f);
    medsList.appendChild(option);
  });
}

/* add medicines to medications list */
function addMedToMedicationList(medication, parent) {
  const div = document.createElement("div");
  const row = document.createElement("div");
  row.setAttribute("class", "d-flex justify-content-between px-2 my-1");
  const { medName, medFreq, extraNote } = medication;

  const medNameDOM = document.createElement("h6");
  medNameDOM.setAttribute("class", "text-muted");
  medNameDOM.setAttribute("id", `med-name-${parent.childNodes.length}`);
  medNameDOM.innerHTML = medName;

  const medFreqDOM = document.createElement("span");
  medFreqDOM.setAttribute("class", "text-secondary");
  medFreqDOM.setAttribute("id", `med-freq-${parent.childNodes.length}`);
  medFreqDOM.innerHTML = `@${medFreq}x time(s) a day`;

  row.appendChild(medNameDOM);
  row.appendChild(medFreqDOM);

  const note = document.createElement("span");
  note.setAttribute("class", "text-danger mx-2");
  note.innerHTML = `* ${extraNote}`;

  div.appendChild(row);
  div.appendChild(note);
  div.appendChild(document.createElement("hr"));
  parent.appendChild(div);
}


/*
 Search patients/pharmacist request
 */
async function filterRequest(q) {
  try {
    const response = await fetch(`/${searchData}/filter/${q}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    });

    const results = await response.json()

    return results;
  }
  catch (error) {
    console.log(`Error filtering ${searchData}`, error);
  }
}


/*
 Create New Prescription Request
 */
async function createPrescriptionRequest(pres) {
  try {

    const { patient, pharmacist, medStr, fromDate, toDate } = pres;

    const data = {
      identifier : new Date().getTime(),
      medication : medStr,
      from_date: fromDate,
      to_date: toDate,
      patient, pharmacist
    }

    const response = await fetch('/create-prescriptions', {
      method: 'POST',
      headers: {
        'Content-Type' : 'application/json',
        'Accept' : 'application/json',
      },
      body: JSON.stringify(data)
    });

    return response;
  }
  catch (error) {
    console.log("Error Creating Prescriptions", error);
  }
}
