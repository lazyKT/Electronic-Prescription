// let editingUsername = false;
//
// // DOM Nodes
// const usernameSaveButton = document.getElementById("username-save-btn");
//
//
// // Hide Some Buttons
// usernameSaveButton.style.display = "none";
//
//
// const usernameEditButton = document.getElementById("username-edit-btn");
// usernameEditButton.addEventListener("click", e => {
//
//   e.preventDefault();
//   editingUsername = !editingUsername;
//
//   console.log("username edit click");
//
//   const usernameInput = document.getElementById("username-profile-input");
//   const usernameSpan = document.getElementById("username-profile-span");
//
//   if (editingUsername) {
//     toggleInput(usernameInput, usernameSpan, show=true);
//     e.target.innerHTML = "Cancel";
//     usernameSaveButton.style.display = "none";
//   }
//   else {
//     toggleInput(usernameInput, usernameSpan, show=false);
//     e.target.innerHTML = "Edit";
//     usernameSaveButton.style.display = "block";
//   }
// });
//
//
// usernameSaveButton.addEventListener("click", async e => {
//   try {
//     e.preventDefault();
//     e.target.innerHTML = "Loading ...";
//
//     const usernameInput = document.getElementById("username-profile-input").value;
//
//     if (!usernameInput || usernameInput === '') {
//       e.target.innerHMTL = "Save";
//       return;
//     }
//
//     const response = await fetch({username: usernameInput});
//
//     console.log(response);
//     if (response && response.ok) {
//       const json = await response.json();
//     }
//     else {
//       const { message } = await response.json();
//       console.log("Error", message);
//     }
//   }
//   catch (error) {
//
//   }
//   finally {
//     e.target.innerHTML = "Save";
//   }
// });
//
//
// function toggleInput (input, span, show) {
//
//   if (!input)
//     return;
//
//   input.style.display = show ? "block" : "none";
//   span.style.display = show ? "none" : "block";
// }
//
//
// // Network Requests
// async function editUser (data) {
//   try {
//     let url = "http://127.0.0.1:5000/"
//
//
//     const response = await fetch(url, {
//       method: "PUT",
//       headers: {
//         "Content-Type" : "application/json",
//         "Accept" : "application/json"
//       },
//       body: JSON.stringify(data)
//     });
//
//     return response;
//   }
//   catch (error) {
//     console.error(error);
//   }
// }
