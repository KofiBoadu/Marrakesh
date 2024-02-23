




function openEmailForm() {
  // Show the email form when the button is clicked
  document.getElementById('emailForm').style.display = 'block';
}




function closeEmailForm() {
  document.getElementById('emailForm').style.display = 'none';
}

//note
function openNoteForm() {
  // Show the email form when the button is clicked
  document.getElementById('noteForm').style.display = 'block';
}

function closeNoteForm() {
  document.getElementById('noteForm').style.display = 'none';
}
function expandNoteForm(){
  let noteForm = document.querySelector('.noteForm').style.display="none"
  var emailContainer = header.closest('.email-activity-container');
  if (emailBody.style.display === 'block') {
    emailBody.style.display = 'none';
  } else {
    emailBody.style.display = 'block';
  }
}

function toggleEmailBody(header) {
  // Find the closest email container
  var emailContainer = header.closest('.email-activity-container');

  // Find the email body inside the email container
  var emailBody = emailContainer.querySelector('.email-body');

  // Toggle the display of the email body
  if (emailBody.style.display === 'block') {
    emailBody.style.display = 'none';
  } else {
    emailBody.style.display = 'block';
  }
}



function toggleEmailForm(header) {
  // Find the closest email form container
  var emailFormContainer = header.closest(".email-form-container");

  // Find the email form inside the email form container
  var emailSendBody = emailFormContainer.querySelector('.sendEmail');

  // Toggle the display of the email form
  if (emailSendBody.style.display === 'block') {
    emailSendBody.style.display = 'none';
  } else {
    emailSendBody.style.display = 'block';
  }
}

// function toggleUpdateNameForm() {
//   var formContainer = document.getElementById('formContainer');
//   formContainer.classList.toggle('hidden');
// }


// document.getElementById('edit').addEventListener('click', function() {
//   toggleFormVisibility();
// });


function showUpdateNameForm() {
  var nameForm = document.getElementById('formContainer')
  var editButton = document.querySelector(".edit")
  nameForm.style.display = "block"
  editButton.style.display = "block"

}
function closeUpdateNameForm() {
  document.getElementById('formContainer').style.display = 'none';
  var nameForm = document.getElementById('formContainer').querySelector('.update_customer_name');
  if (nameForm) {
    nameForm.reset();
  }
  var editButton = document.querySelector(".edit")
  editButton.style.display = "none"
}
function editButtonDisplay() {
  document.querySelector('.edit').style.display = 'none'
}

function showEditButton() {
  let editButton = document.querySelector(".edit")
  editButton.style.display = "inline-block"
}
function hideEditButton(event) {
  let editButton = document.querySelector(".edit");
  var nameForm = document.getElementById('formContainer').querySelector('.update_customer_name');

  // Check if the mouseout occurred outside the nameForm and outside the editButton
  if (nameForm.contains(event.relatedTarget)) {
    // Hide the edit button
    editButton.style.display = "block";
  }
  if (event.relatedTarget !== editButton) {
    editButton.style.display = "none";
  }
}

//phone edit
function showUpdatePhoneForm() {
  var phoneForm = document.getElementById('phoneformContainer')
  var phoneEditButton = document.querySelector(".editPhone")
  phoneForm.style.display = "block"
  phoneEditButton.style.display = "block"

}
function closeUpdatePhoneForm() {
  document.getElementById('phoneformContainer').style.display = 'none';
  var phoneForm = document.getElementById('phoneformContainer').querySelector('.update_customer_phone');
  if (phoneForm) {
    phoneForm.reset();
  }
  var phoneEditButton = document.querySelector(".phoneEdit")
  phoneEditButton.style.display = "none"
}
function phoneEditButtonDisplay() {
  document.querySelector('.phoneEdit').style.display = 'none'
}

function showPhoneEditButton() {
  let phoneEditButton = document.querySelector(".phoneEdit")
  phoneEditButton.style.display = "inline-block"
}
function phoneHideEditButton(event) {
  let phoneEditButton = document.querySelector(".phoneEdit");
  var phoneForm = document.getElementById('phoneformContainer').querySelector('.update_customer_phone');

  // Check if the mouseout occurred outside the nameForm and outside the editButton
  if (phoneForm.contains(event.relatedTarget)) {
    // Hide the edit button
    phoneEditButton.style.display = "block";
  }
  if (event.relatedTarget !== phoneEditButton) {
    phoneEditButton.style.display = "none";
  }
}

//email edit
function showUpdateEmailForm() {
  var emailForm = document.getElementById('emailformContainer')
  var emailEditButton = document.querySelector(".emailEdit")
  emailForm.style.display = "block"
  emailEditButton.style.display = "block"

}
function closeUpdateEmailForm() {
  document.getElementById('emailformContainer').style.display = 'none';
  var emailForm = document.getElementById('emailformContainer').querySelector('.update_customer_email');
  if (emailForm) {
    emailForm.reset();
  }
  var emailEditButton = document.querySelector(".emailEdit")
  emailEditButton.style.display = "none"
}
function emailEditButtonDisplay() {
  document.querySelector('.emailEdit').style.display = 'none'
}

function showEmailEditButton() {
  let emailEditButton = document.querySelector(".emailEdit")
  emailEditButton.style.display = "inline-block"
}
function emailHideEditButton(event) {
  let emailEditButton = document.querySelector(".emailEdit")
  var emailForm = document.getElementById('emailformContainer').querySelector('.update_customer_email');

  // Check if the mouseout occurred outside the nameForm and outside the editButton
  if (emailForm.contains(event.relatedTarget)) {
    // Hide the edit button
    emailEditButton.style.display = "block";
  }
  if (event.relatedTarget !== emailEditButton) {
    emailEditButton.style.display = "none";
  }
}

