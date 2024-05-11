

//UPDATE THE USER PROFILE DETAILS INCLUDING FIRST NAME AND LAST NAME
// Initial values to restore on cancel
document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded and parsed");

    let initialFirstName = document.getElementById("firstName").value;
    console.log("Initial First Name:", initialFirstName);
    let initialLastName = document.getElementById("lastName").value;
    console.log("Initial Last Name:", initialLastName);

    // Select input fields and button container
    const firstNameInput = document.getElementById("firstName");
    const lastNameInput = document.getElementById("lastName");
    const buttonContainer = document.getElementById("buttonContainer");

    // Buttons
    const saveButton = document.getElementById("saveButton");
    const cancelButton = document.getElementById("cancelButton");

    if (firstNameInput && lastNameInput && buttonContainer && saveButton && cancelButton) {
        // Show buttons when any input field is changed
        [firstNameInput, lastNameInput].forEach(input => {
            input.addEventListener("input", () => {
                console.log("Input changed");
                buttonContainer.style.display = "block";
            });
        });

        // Save button click
        saveButton.addEventListener("click", () => {
            const formData = new FormData(document.getElementById("user-profile-details"));
            const form = document.getElementById("user-profile-details");
            const postUrl = form.getAttribute("data-url");
            fetch(postUrl, {
                method: "POST",
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    console.log("Save successful");
                    buttonContainer.style.display = "none";
                    initialFirstName = firstNameInput.value;
                    initialLastName = lastNameInput.value;
                } else {
                    console.error("Error:", data.message);
                    alert(`Error: ${data.message}`);
                }
            })
            .catch(error => {
                console.error("Server error:", error);
                alert(`Server error: ${error}`);
            });
        });

        // Cancel button click
        cancelButton.addEventListener("click", () => {
            console.log("Cancel clicked");
            firstNameInput.value = initialFirstName;
            lastNameInput.value = initialLastName;
            buttonContainer.style.display = "none";
        });
    } else {
        console.error("One or more elements not found");
    }
});
















//update tours content IN THE TABLE INSTEAD OF REFRESHING THE WHOLE PAGE
document.addEventListener('DOMContentLoaded', function() {
    const tour_paginationContainer = document.querySelector('.tours-pagination-controls');

    // Check if the pagination container exists
    if (tour_paginationContainer) {
        tour_paginationContainer.addEventListener('click', function(e) {
            // Prevent the default link behavior
            e.preventDefault();

            // Target only anchor tags
            const target = e.target.closest('a');
            if (!target || target.parentElement.classList.contains('disabled')) {
                return;
            }

            const url = target.getAttribute('href');
            if (url) {
                fetch(url, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' } // Important to differentiate between AJAX and regular requests on the server
                })
                .then(response => response.json())
                .then(data => {
                    // Assuming the server sends back JSON with the HTML fragments
                    document.getElementById('toursTableData').innerHTML = data.tours_table_body_html; // Update the table body
                    document.querySelector('.tours-pagination-controls').innerHTML = data.tours_pagination_html; // Update the pagination controls
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        });
    }
});





//disables the user functionalities and buttons if its A STANDARD USER
document.addEventListener('DOMContentLoaded', function () {
  // Retrieve and check the user's role ID
  const roleId = parseInt(document.getElementById('login-user-role-id').value, 10);
  if (roleId > 1) {
    // Select and disable all buttons with the 'user-action-button' class
     const create_AdminsButton = document.getElementById('add_admin_button');
     if (create_AdminsButton) {
		create_AdminsButton.disabled = true;
		create_AdminsButton.classList.add('disabled'); // Use 'disabled' class for styling
		create_AdminsButton.style.backgroundColor ="#d3d3d357"
		create_AdminsButton.style.border="none"
//		createAdminsButton.style.color = "#FF914C";
		create_AdminsButton.innerHTML = '<img src="https://img.icons8.com/material-rounded/10/FF914C/lock-2.png" alt="Export icon"> Create new user';
	  }
    document.querySelectorAll('.user-action-button').forEach(button => {
      button.disabled = true;
    });
  }





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






function show_TourButton() {
  document.getElementById('tourForm').style.display = 'block';

}

function closeTourModal() {
  document.getElementById('tourForm').style.display = 'None';
}




//
////UPDATE THE USER PROFILE DETAILS INCLUDING FIRST NAME AND LAST NAME
//// Initial values to restore on cancel
//document.addEventListener("DOMContentLoaded", function() {
//    console.log("DOM fully loaded and parsed");
//
//    let initialFirstName = document.getElementById("firstName").value;
//    console.log("Initial First Name:", initialFirstName);
//    let initialLastName = document.getElementById("lastName").value;
//    console.log("Initial Last Name:", initialLastName);
//
//    // Select input fields and button container
//    const firstNameInput = document.getElementById("firstName");
//    const lastNameInput = document.getElementById("lastName");
//    const buttonContainer = document.getElementById("buttonContainer");
//
//    // Buttons
//    const saveButton = document.getElementById("saveButton");
//    const cancelButton = document.getElementById("cancelButton");
//
//    if (firstNameInput && lastNameInput && buttonContainer && saveButton && cancelButton) {
//        // Show buttons when any input field is changed
//        [firstNameInput, lastNameInput].forEach(input => {
//            input.addEventListener("input", () => {
//                console.log("Input changed");
//                buttonContainer.style.display = "block";
//            });
//        });
//
//        // Save button click
//        saveButton.addEventListener("click", () => {
//            const formData = new FormData(document.getElementById("user-profile-details"));
//            fetch("{{ url_for('users.update_user_details') }}", {
//                method: "POST",
//                body: formData
//            })
//            .then(response => response.json())
//            .then(data => {
//                if (data.status === "success") {
//                    console.log("Save successful");
//                    buttonContainer.style.display = "none";
//                    initialFirstName = firstNameInput.value;
//                    initialLastName = lastNameInput.value;
//                } else {
//                    console.error("Error:", data.message);
//                    alert(`Error: ${data.message}`);
//                }
//            })
//            .catch(error => {
//                console.error("Server error:", error);
//                alert(`Server error: ${error}`);
//            });
//        });
//
//        // Cancel button click
//        cancelButton.addEventListener("click", () => {
//            console.log("Cancel clicked");
//            firstNameInput.value = initialFirstName;
//            lastNameInput.value = initialLastName;
//            buttonContainer.style.display = "none";
//        });
//    } else {
//        console.error("One or more elements not found");
//    }
//});
//
//
//

