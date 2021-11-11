/**
View Description
**/
function viewPrescription (node) {
  const pres_id = node.dataset.presId;
  window.location = `/prescription/${pres_id}`
}


/**
# search patient to view patient profile and his prescriptions
**/
function searchPatientsAndPrescriptions () {
  const dataContainer = document.getElementById("prescription-data-container");
  clearPrescriptions(dataContainer);
}


/**
# Clear Prescriptions Container for new data
**/
function clearPrescriptions (container) {

  while (container.lastChild) {
      container.removeChild(container.lastChild);
  }
}
