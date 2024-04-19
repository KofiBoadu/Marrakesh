



document.addEventListener('DOMContentLoaded', function () {
  // Retrieve and check the user's role ID
  const roleId = parseInt(document.getElementById('login-user-role-id').value, 10);
  if (roleId > 1) {
    // Select and disable all buttons with the 'user-action-button' class
    document.querySelectorAll('.user-action-button').forEach(button => {
      button.disabled = true;
    });
  }

  // // Setup for checkboxes and updating form values based on the selected user
  // const checkboxes = document.querySelectorAll('.user-checkbox');
  // checkboxes.forEach(function(checkbox) {
  //   checkbox.addEventListener('change', function() {
  //     if (this.checked) {
  //       // Retrieve the user ID from the data attribute
  //       const userId = this.getAttribute('data-user-id');
  //       // Update the hidden input's value for various forms
  //       document.getElementById('remove-user-id').value = userId;
  //       document.getElementById('deactivate-user-id').value = userId;
  //       document.getElementById('reactivate-user-id').value = userId;
  //       document.getElementById('make-new-user-admin-id').value = userId;
  //       document.getElementById('remove-new-user-admin-id').value = userId;
  //     }
  //   });
  // });
  // Setup for checkboxes and updating form values based on the selected user
  const checkboxes = document.querySelectorAll('.user-checkbox');
  const menu = document.getElementById('user-action-div'); // Assuming you have a menu div in your HTML
  const forms = menu.querySelectorAll('form');

  checkboxes.forEach(function (checkbox) {
    checkbox.addEventListener('change', function () {
      if (this.checked) {
        // Retrieve the user ID from the data attribute
        const userId = this.getAttribute('data-user-id');
        // Update the hidden input's value for various forms
        forms.forEach(function (form) {
          const input = form.querySelector('input[type="hidden"]');
          input.value = userId;
        });

        // Show the menu when a user is selected
        menu.style.display = 'block';
      } else {
        // Hide the menu when no user is selected
        menu.style.display = 'none';
      }
    });
  });

});


document.getElementById('tourForm').addEventListener('submit', function () {
  // Trim the values of text inputs
  this.querySelectorAll('input[type=text]').forEach(input => {
    input.value = input.value.trim();

  });
});

function show_userButton() {
  document.getElementById('user').style.display = 'block';

}

function closeUserModal() {
  document.getElementById('user').style.display = 'None';
}