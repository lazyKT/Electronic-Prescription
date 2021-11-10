const medicines = [
  "Panadol",
  "Dicogin",
  "Dolphinal",
  "Fluza",
  "Biogesic",
  "Konidin",
  "Strapcils",
];

let searchData

window.onload = () => {
  // DOM Nodes
  const errorMessageBoxPresc = document.getElementById('error-message-presc');
  const modalContainer = document.getElementById("modal-container");
  const patientInput = document.getElementById("patient");
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

  // search patient
  searchBtn.addEventListener("click", async (e) => {
    try {
      const searchKeyWord = document.getElementById("search-input").value;

      if (!searchKeyWord || searchKeyWord === "") return;

      clearResults();

      const response = await filterRequest(searchKeyWord);

      if (response && response.ok) {
        const results = await response.json();

        if (results.length === 0)
          showEmptyMessage(searchKeyWord);
        else
          appendResults(results);
      }
      else {
        const { message } = await response.json();
        const errMessage = message ? message : 'Network Connection Error!';
        showErrorMessage(errMessage);
      }
    }
    catch (error) {
      console.log(`Error fetching ${searchData} filtered request`, error);
    }
  });

  // add medicine
  addMedicineButton.addEventListener("click", (e) => openModal(medModal));

  // close patient/pharmacy modals
  closeModalBtn.addEventListener("click", (e) => {
    closeModal(modalContainer);
  });

  // close medication modal
  closeMedicationModal.addEventListener("click", (e) => {
    clearMedicationForm();
    closeModal(medModal);
  });

  /* add medication to the medication list */
  addMedtoList.addEventListener("click", (e) => {
    const medName = document.getElementById("med-input")?.value;
    const medFreq = document.getElementById("med-freq")?.value;
    const medQty = document.getElementById("med-qty")?.value;
    const extraNote = document.getElementById("extra-note-meds")?.value;

    if (!medName || medName === "" || !medFreq || medFreq === "" || !medQty || medQty === 0) return;

    addMedToMedicationList({ medName, medFreq, medQty, extraNote }, medicationList);

    clearMedicationForm();

    closeModal(medModal);
  });

  /* create prescription | submit button click event */
  createPrescriptionButton.addEventListener('click', async e => {
    try {
      const patient = patientInput.dataset.patientId;
      const fromDate = document.getElementById('from_date').value;
      const toDate = document.getElementById('to_date').value;
      e.preventDefault();
      e.target.innerHTML = 'Loading..'
      e.target.setAttribute('disabled', true); // Disable the button, so that the user don't press again while loading

      if (!patient || patient === '' || !fromDate || fromDate === '' || !toDate || toDate === '')
      {
        e.target.innerHTML = 'Create Prescription';
        e.target.removeAttribute('disabled');
        throw new Error('Missing Required Data')
        return;
      }

      if (medicationList.childNodes.length <= 1)
        return;

      const medStr = medicationString(medicationList);

      const response = await createPrescriptionRequest({ patient, medStr, fromDate, toDate});

      if (response && response.ok) {
        window.location = '/doctor/dashboard';
      }
      else {
        const { message } = await response.json();
        if (message)
          errorMessageBoxPresc.innerHTML = message;
        else
          errorMessageBoxPresc.innerHTML = 'Network Connection Error!';
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
function clearResults () {
  const resultContainer = document.getElementById("result-container");
  while (resultContainer.lastChild) {
    resultContainer.removeChild(resultContainer.lastChild);
  }
}


/* clear medication form */
function clearMedicationForm () {
  const medInput = document.getElementById("med-input");
  const medQty = document.getElementById("med-qty");
  const medFreq = document.getElementById("med-freq");
  medInput.value = "";
  medQty.value = "";
  medFreq.value = "";
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
  row.setAttribute("class", "row px-2 mb-2");
  const { medName, medFreq, extraNote, medQty } = medication;

  const medNameDOM = document.createElement("h6");
  medNameDOM.setAttribute("class", "col text-muted");
  medNameDOM.setAttribute("id", `med-name-${parent.childNodes.length}`);
  medNameDOM.innerHTML = medName;

  const medQtyDOM = document.createElement("label");
  medQtyDOM.setAttribute("class", "col text-muted");
  medQtyDOM.setAttribute("id", `med-qty-${parent.childNodes.length}`);
  medQtyDOM.innerHTML = `x ${medQty}`;

  const medFreqDOM = document.createElement("span");
  medFreqDOM.setAttribute("class", "col text-secondary mx-1 text-end");
  medFreqDOM.setAttribute("id", `med-freq-${parent.childNodes.length}`);
  medFreqDOM.innerHTML = `@${medFreq}x time(s) a day`;

  row.appendChild(medNameDOM);
  row.appendChild(medQtyDOM);
  row.appendChild(medFreqDOM);

  const note = document.createElement("div");
  note.setAttribute("class", "alert alert-info mx-1 mt-1");
  note.setAttribute("role", "alert");
  note.innerHTML = "Take 2 tablets after every meal";

  div.appendChild(row);
  div.appendChild(note);
  div.appendChild(document.createElement("hr"));
  parent.appendChild(div);
}


/**
# Show Empty Message if the search results return nothing
**/
function showEmptyMessage (q) {
  const resultContainer = document.getElementById("result-container");
  const emptyMessageBox = document.createElement("div");
  emptyMessageBox.setAttribute("class", "alert alert-info");
  emptyMessageBox.setAttribute("id", "empty-msg-box");
  emptyMessageBox.setAttribute("role", "alert");
  emptyMessageBox.innerHTML = `No search Result(s) related to ${q}`;
  emptyMessageBox.style.display = "block";
  resultContainer.appendChild(emptyMessageBox);
}

/**
# Show Error Message if any error encounter during search
**/
function showErrorMessage (message) {
  const resultContainer = document.getElementById("result-container");
  const errorMessageBox = document.createElement("div");
  errorMessageBox.setAttribute("class", "alert alert-danger");
  errorMessageBox.setAttribute("id", "error-msg-box");
  errorMessageBox.setAttribute("role", "alert");
  errorMessageBox.innerHTML = message;
  errorMessageBox.style.display = "block";
  resultContainer.appendChild(errorMessageBox);
}


function openModal (modal) {
  modal.style.display = "flex";
}

function closeModal (modal) {
  modal.style.display = "none";
}


function medicationString (medicationList) {
  /* formated medication string: seperate each by comma */
  let medStr = "";
  for (let i = 0; i < medicationList.childElementCount; i++) {
    const medName = `med-name-${i+1}`;
    const medQty = `med-qty-${i+1}`;
    const medFreq = `med-freq-${i+1}`;
    const delimeter = i === 0 ? '' : ', ';

    medStr += `${delimeter} ${document.getElementById(medName).innerHTML} ${document.getElementById(medQty).innerHTML} ${document.getElementById(medFreq).innerHTML}`;
  }

  return medStr;
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

    return response;
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
      patient,
      pharmacist: 'NA'
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
