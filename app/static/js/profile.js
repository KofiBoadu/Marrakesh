




function openEmailForm() {
    // Show the email form when the button is clicked
    document.getElementById('emailForm').style.display = 'block';
  }




  function closeEmailForm() {
    document.getElementById('emailForm').style.display = 'none';
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