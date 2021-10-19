// console.log("User Admin scripts running ...");

function openCreateNewUserModal() {
  const modalContainer = document.getElementById("my-modal-container");
  modalContainer.style.display = "flex";
}

// open modal for Edit User or View User
function openEditViewModal(dom) {
  // to get the parent node of 'tr' type, we will transverse upwards until we get it
  // In this function, the parameter dom represents <button>
  // In our html hiearchy, tr -> td -> div -> button
  const tr = dom.parentNode.parentNode.parentNode; // button.div.td.tr
  const modalContainer = document.getElementById("my-modal-container");
  modalContainer.style.display = "flex";
  const modal = document.getElementById("my-modal");
  const modalMode = dom.dataset.mode;
  // create Modal Child Nodes based on the modalMode: edit will be inputs and view will be just texts
  createModalContents(modal, tr.cells, modalMode);
  // console.log(tr, tr.cells[0]);
}

function createModalContents(parent, data, mode) {
  // create container for the modal contents
  const modalTitle = document.createElement("h5");
  modalTitle.innerHTML = mode === "edit" ? "Edit Modal" : "View Details";
  parent.appendChild(modalTitle);
  const container = document.createElement("div");
  container.setAttribute("class", "modal-contents p-2");

  // iterate through the data object contents
  for (const [_, v] of Object.entries(data)) {

    // get value of data object
    const value = v.childNodes[0];
    let key
    try {
        // if the data have key dataset attribute,
        key = value ? value.dataset.key : null; // get key from DOM dataset
    }
    catch (error) {
      // otherwise, set to null
      key = null;
    }

    if (key && key !== null) {
      // create DOMs
      const title = document.createElement("h5");
      title.innerHTML = key;
      container.appendChild(title);
      if (mode === "edit") {
        const fieldType = value.dataset.fieldType; // input, select or immutable
        // create dom element based on data field type
        const field = document.createElement(
          fieldType === "pk" ? "input" : fieldType
        );
        field.setAttribute("id", `update-${key}`);
        field.setAttribute("class", "modal-input-field");
        // if field type is immutable, set readonly attribute to true
        fieldType === "pk" && field.setAttribute("readonly", true);
        // if field type is select, put options
        fieldType === "select" && getEditableSelector(field, key);
        field.value = value.innerHTML;
        container.appendChild(field);
      } else if (mode === "view") {
        const text = document.createElement("p");
        text.innerHTML = value.innerHTML;
        container.appendChild(text);
      }
    }
  }
  if (mode === "edit")
    container.appendChild(modalButton("save"));
  container.appendChild(modalButton("cancel"));
  parent.appendChild(container);
}


// create select input type with given options
function getEditableSelector(selector, data) {
  console.log("data", data);
  const values = data === "status" ? ["active", "inactive"]  : ["admin", "patient", "doctor", "pharmacist"];
  values.forEach((v) => {
    const option = document.createElement("option");
    option.value = v;
    option.text = v;
    selector.appendChild(option);
  });
}

// create dynamic button inside the modal
function modalButton(btnType) {
  const btn = document.createElement("button");
  btn.innerHTML = btnType.charAt(0).toUpperCase() + btnType.slice(1);
  if (btnType === "cancel") {
    btn.setAttribute("class", "btn btn-light modal-cancel-btn");
    btn.setAttribute("onclick", "dismissModal()");
  } else if (btnType === "save") {
    btn.setAttribute("class", "btn btn-primary modal-save-btn");
    btn.setAttribute("onclick", "updateData(this)");
    // btn.addEventListener("click", updateData(data));
    // btn.onclick = updateData(data);
  }
  return btn;
}

// dismiss modal
function dismissModal() {
  const modalContainer = document.getElementById("my-modal-container");
  if (modalContainer) modalContainer.style.display = "none";
  const modal = document.getElementById("my-modal");
  if (modal) modal.innerHTML = null; // remove all the modal contents on Cancel Button Press
}

// edit/update User
function updateData(dom) {
  console.log(dom, dom.innerHTML);
  dom.innerHTML = 'Loading ...';
  const id = document.getElementById("update-id").value;
  const username = document.getElementById("update-username").value;
  const role = document.getElementById("update-role").value;
  const email = document.getElementById("update-email").value;
  const status = document.getElementById("update-status").value;
  console.log (username, role, email, status);
  // make update user request
  updateUserRequest({id, username, role, email, status})
    .then(res => {
      // update successful
      dom.innerHTML = 'Save';
      updateDOM(res);
      dismissModal();
    })
    .catch(err => console.log("Update Erorr", err));
}

// update table row after the successful user update network request
function updateDOM(updatedData) {
  const { id, username, email, role, status } = updatedData;

  const updatedTd = document.querySelectorAll(`[data-user-key~="${id}"]`);
  // update value of each table cell
  updatedTd[1].childNodes[0].innerHTML = username;
  updatedTd[2].childNodes[0].innerHTML = email;
  updatedTd[3].childNodes[0].innerHTML = role;
  updatedTd[4].childNodes[0].innerHTML = status ? 'active' : 'inactive';
}


// making network requset to server for user update/edit
async function updateUserRequest(user) {
  const {id} = user;
  try {
    const response = await fetch(`/admin/user/${id}`, {
      method: 'PUT',
      headers : {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
      },
      body: JSON.stringify(user)
    });

    const json = await response.json();

    return json;
  }
  catch(error ) {
    console.log(error);
  }
}


// add new user request
async function addNewUserRequest(user) {
  try {
    const response = await fetch(`/admin/user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(user)
    });

    const json = await response.json();

    return json;
  }
  catch(error) {
    console.log("Create New User Error", error);
  }
}

//

//

//
///




/// Extra spcaes
