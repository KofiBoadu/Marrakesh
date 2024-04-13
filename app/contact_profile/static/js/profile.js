




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
  //
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
  
  //state edit
  
  function showUpdateStateForm() {
    var stateForm = document.getElementById('stateformContainer')
    var stateEditButton = document.querySelector(".stateEdit")
    stateForm.style.display = "block"
    stateEditButton.style.display = "block"
  
  }
  function closeUpdateStateForm() {
    document.getElementById('stateformContainer').style.display = 'none';
    var stateForm = document.getElementById('stateformContainer').querySelector('.update_customer_state');
    if (stateForm) {
      stateForm.reset();
    }
    var stateEditButton = document.querySelector(".stateEdit")
    stateEditButton.style.display = "none"
  }
  function stateEditButtonDisplay() {
    document.querySelector('.stateEdit').style.display = 'none'
  }
  
  function showStateEditButton() {
    let stateEditButton = document.querySelector(".stateEdit")
    stateEditButton.style.display = "inline-block"
  }
  function stateHideEditButton(event) {
    let stateEditButton = document.querySelector(".stateEdit")
    var stateForm = document.getElementById('stateformContainer').querySelector('.update_customer_state');
  
    // Check if the mouseout occurred outside the nameForm and outside the editButton
    if (stateForm.contains(event.relatedTarget)) {
      // Hide the edit button
      stateEditButton.style.display = "block";
    }
    if (event.relatedTarget !== stateEditButton) {
      stateEditButton.style.display = "none";
    }
  }
  //status edit
  
  function showUpdateStatusForm() {
    var statusForm = document.getElementById('statusformContainer')
    var statusEditButton = document.querySelector(".statusEdit")
    statusForm.style.display = "block"
    statusEditButton.style.display = "block"
  
  }
  function closeUpdateStatusForm() {
    document.getElementById('statusformContainer').style.display = 'none';
    var statusForm = document.getElementById('stateformContainer').querySelector('.update_customer_state');
    if (statusForm) {
      statusForm.reset();
    }
    var statusEditButton = document.querySelector(".statusEdit")
    statusEditButton.style.display = "none"
  }
  function statusEditButtonDisplay() {
    document.querySelector('.statusEdit').style.display = 'none'
  }
  
  function showStatusEditButton() {
    let statusEditButton = document.querySelector(".statusEdit")
    statusEditButton.style.display = "inline-block"
  }
  function statusHideEditButton(event) {
    let statusEditButton = document.querySelector(".statusEdit")
    var statusForm = document.getElementById('statusformContainer').querySelector('.update-status');
  
    // Check if the mouseout occurred outside the nameForm and outside the editButton
    if (statusForm.contains(event.relatedTarget)) {
      // Hide the edit button
      statusEditButton.style.display = "block";
    }
    if (event.relatedTarget !== statusEditButton) {
      statusEditButton.style.display = "none";
    }
  }
  
  
  
  
  // update bookings
  document.addEventListener('DOMContentLoaded', function() {
      var updateButtons = document.querySelectorAll('.update-btn');
      console.log("JavaScript is running");
  
  
      updateButtons.forEach(function(button) {
          button.addEventListener('click', function(event) {
              // Prevent the default action
              event.preventDefault();
  
              var bookingId = this.getAttribute('data-booking-id');
              var contactId = this.getAttribute('data-contact-id');
              var tourId = this.getAttribute('data-tour-id');
              var tourName = this.getAttribute('data-tour-name');
  
              // Update the inputs in the submit-update-bookings form
              let id=document.querySelector('input[name="updatingbooking_contact_id"]').value = contactId;
              let bookid= document.querySelector('input[name="updatingbooking_booking_id"]').value = bookingId;
              let tourid= document.querySelector('input[name="updatingbooking_tour_id"]').value = tourId;
              document.getElementById('submit_booking').querySelector('p').textContent = `  ${tourName}`;
              console.log(id,bookid,tourid)
  
              // Show the submit-update-bookings form
              document.querySelector('.submit-update-bookings').style.display = 'block';
  
              // Correct the placeholders in the text content
              var formTexts = document.querySelectorAll('#submit_booking p');
              formTexts[0].textContent =  tourName;
              formTexts[1].textContent = "Modify to: " + tourName; // Update this based on user interaction or another method
          });
      });
  });
  
  function closeUpdateBookingForm() {
    document.getElementById('update-bookings').style.display = 'none';
    
  }
  
  
  
  // gets me the old tour name 
  document.addEventListener('DOMContentLoaded', function() {
      // Assuming your "update-bookings" form is wrapped in a div with a specific class or ID
      const formContainer = document.getElementById('update-bookings');
      const modifyFromParagraph = formContainer.querySelector('.modify p'); // Select the <p> within .modify
      
      // Attach the click event listener to the container of the buttons
      document.querySelector('.profile-bookings ul').addEventListener('click', function(event) {
          // Check if the clicked element or its parent is an "edit" button
          const editButton = event.target.closest('.update-btn');
          if (editButton) {
              // Retrieve the tour name from the data attribute of the button
              const tourName = editButton.getAttribute('data-tour-name');
              
              // Set the content of the <p> tag to the tour name
              modifyFromParagraph.textContent = tourName;
              
              // Set the hidden input value for submitting
              document.getElementById('modifyFromValue').value = tourName;
              
              // Show the form if it's not already visible
              formContainer.style.display = 'block';
          }
      });
  });
  
  
  
  // add a spin 
  
  document.addEventListener('DOMContentLoaded', function() {
      const form = document.getElementById('update-bookings'); // Use the form's ID
      const loadingOverlay = document.getElementById('loadingOverlay');
      
  
  
      form.addEventListener('submit', function(event) {
          // Optional: Prevent the form from submitting immediately if you need to validate
          // event.preventDefault();
  
          // Display the loading overlay
          loadingOverlay.style.display = 'flex';
      });
  });
  
  
  
  //book a tour
  
  function showBookingTourForm(){
    document.getElementById("bookingTour").style.display="block";
  }
  function closeBookingTourForm() {
    document.getElementById("bookingTour").style.display = 'none';
    
  }
  
  //delete note
  
  function deleteNote(notesId, customerId) {
    console.log("deleteNote called with notesId:", notesId, "and customerId:", customerId);
    // Confirm deletion
    if (!confirm("Are you sure you want to delete this note?")) {
      return;
    }
  
    // Set up the request data using URLSearchParams for x-www-form-urlencoded format
    var formData = new URLSearchParams();
    formData.append('notes_id', notesId);
    formData.append('customer_id', customerId);
  
    // Send the POST request
    fetch('/delete_notes', {
      method: 'POST',
      body: formData,
      credentials: 'same-origin', // Include cookies
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).then(response => {
      if (response.ok) {
        alert('Note deleted successfully.');
        window.location.reload(); // Reload the page to update the UI
      } else {
        alert('Failed to delete the note.');
      }
    }).catch(error => console.error('Error:', error));
  }
  
  
  


