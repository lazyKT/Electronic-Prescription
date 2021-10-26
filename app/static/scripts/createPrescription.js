const patients = [
  { name: "lwin" },
  { name: "jack" },
  { name: "susan" },
  { name: "suzana" },
  { name: "jake" },
  { name: "amy" },
  { name: "holt" },
  { name: "kevin" },
  { name: "terry" },
  { name: "guzman" },
  { name: "searah" },
  { name: "joe" },
  { name: "john" },
  { name: "jason" },
  { name: "david" },
  { name: "mike" },
  { name: "paul" },
  { name: "kyaw" },
  { name: "liz" },
  { name: "eliot" },
  { name: "sam" },
  { name: "kate" }
];

const pharmacists = [
  { name: "lwin" },
  { name: "jack" },
  { name: "susan" },
  { name: "suzana" },
  { name: "jake" },
  { name: "amy" },
  { name: "holt" },
  { name: "kevin" },
  { name: "terry" },
  { name: "guzman" },
  { name: "searah" },
  { name: "joe" },
  { name: "john" },
  { name: "jason" },
  { name: "david" },
  { name: "mike" },
  { name: "paul" },
  { name: "kyaw" },
  { name: "liz" },
  { name: "eliot" },
  { name: "sam" },
  { name: "kate" }
];

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

  // add medicines in medicine list
  populateMedsList(medsList);

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
  searchBtn.addEventListener("click", (e) => {
    const searchKeyWord = document.getElementById("search-input").value;

    if (!searchKeyWord || searchKeyWord === "") return;

    clearResults();

    const results = searchData === 'patient'
                      ? patients.filter((p) => p.name.includes(searchKeyWord))
                      : pharmacists.filter((p) => p.name.includes(searchKeyWord))

    appendResults(results);
  });

  // add medicine
  addMedicineButton.addEventListener("click", (e) => openModal(medModal));

  // close modals
  closeModalBtn.addEventListener("click", (e) => closeModal(modalContainer));

  closeMedicationModal.addEventListener("click", (e) => closeModal(medModal));

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
    const div = document.createElement("div");
    div.setAttribute("class", "d-flex justify-content-between my-2 result");

    const name = document.createElement("h6");
    name.setAttribute("class", "text-muted");
    name.innerHTML = res.name;

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
      input.value = name.innerHTML;
    });
  });
}

function clearResults() {
  const resultContainer = document.getElementById("result-container");
  while (resultContainer.lastChild) {
    resultContainer.removeChild(resultContainer.lastChild);
  }
}

function populateMedsList(medsList) {
  medicines.forEach((f) => {
    const option = document.createElement("option");
    option.setAttribute("value", f);
    medsList.appendChild(option);
  });
}

function addMedToMedicationList(medication, parent) {
  const div = document.createElement("div");
  const row = document.createElement("div");
  row.setAttribute("class", "d-flex justify-content-between px-2 my-1");
  const { medName, medFreq, extraNote } = medication;

  const medNameDOM = document.createElement("h6");
  medNameDOM.setAttribute("class", "text-muted");
  medNameDOM.innerHTML = medName;

  const medFreqDOM = document.createElement("span");
  medFreqDOM.setAttribute("class", "text-secondary");
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
