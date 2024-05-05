

//THIS UPDATE THE TITLE OF TASK AND MANIPULATE IT FRONTEND
document.addEventListener('DOMContentLoaded', function() {
    var inputField = document.getElementById('task-title-text-input');
    inputField.addEventListener('focus', function() {
        var buttons = this.closest('.task-title-form').querySelector('.task-title-buttons');
        buttons.style.display = 'block';
    });

    var forms = document.querySelectorAll('.task-title-form');
    forms.forEach(function(form) {
        var buttons = form.querySelector('.task-title-buttons');
        var saveButton = buttons.querySelector('button[name="task-title-saveButton"]');
        var cancelButton = buttons.querySelector('button[name="task-title-cancelButton"]');

        form.addEventListener('submit', function(event) {
            event.preventDefault();
            var actionUrl = form.getAttribute('data-action-url'); // Get the action URL from data attribute

            if (document.activeElement === saveButton) {
                var taskId = form.querySelector('[name="task_id"]').value;
                var newTaskTitle = form.querySelector('[name="taskTitle"]').value;

                // Update the input value immediately before the POST request
                form.querySelector('[name="taskTitle"]').value = newTaskTitle;

                // Hide the buttons as soon as Save is clicked
                buttons.style.display = 'none';

                // Proceed with the POST request to update the server data
                fetch(actionUrl, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    body: 'task_id=' + taskId + '&taskTitle=' + encodeURIComponent(newTaskTitle)
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    // Optionally inform the user of the success
                })
                .catch((error) => {
                    console.error('Error:', error);
                    // Optionally inform the user of the failure
                });
            } else if (document.activeElement === cancelButton) {
                // Just hide the buttons if Cancel is clicked, leave the input as the new title
                buttons.style.display = 'none';
            }
        });

        cancelButton.addEventListener('click', function(event) {
            event.preventDefault();
            // Just hide the buttons, leave the input as the new title
            buttons.style.display = 'none';
        });
    });
});




//update due date the task form
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.task-due-date-form');
    const select = document.getElementById('update-due-date');
    const customDateInput = document.getElementById('update-customDueDate');

    window.toggleUpdateCustomDate = function toggleUpdateCustomDate(select) {
        if (select.value === 'update-custom-date') {
            customDateInput.style.display = 'block';
            customDateInput.focus();  // Optionally focus the input to prompt the user
        } else {
            customDateInput.style.display = 'none';
            if (select.value) {
                submitForm();  // Programmatically submit form when a predefined date is selected
            }
        }
    }

    customDateInput.addEventListener('change', function() {
        if (this.value) {
            submitForm();  // Programmatically submit form when a custom date is entered
        }
    });

    function submitForm() {
        const formData = new FormData(form);
        fetch(form.action, {
            method: 'POST',
            body: formData
        }).then(response => response.json())
          .then(data => {
              console.log('Success:', data);
              // Handle success here, e.g., showing a success message
          })
          .catch((error) => {
              console.error('Error:', error);
              // Handle errors here, e.g., showing an error message
          });
    }

    // Initial check to handle pre-selected values when the page loads
    toggleUpdateCustomDate(select);
});





//update the task due time
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.task-due-time-form');
    const select = document.getElementById('update-task-due-time');

    select.addEventListener('change', function() {
        submitForm();
    });

    function submitForm() {
        const formData = new FormData(form); // Prepare form data for sending
        fetch(form.action, {
            method: 'POST', // Set the method to POST
            body: formData, // Attach the form data
        })
        .then(response => response.json()) // Assuming the server responds with JSON
        .then(data => {
            console.log('Success:', data);
            // Optionally, handle success here, such as showing a success message
        })
        .catch((error) => {
            console.error('Error:', error);
            // Optionally, handle errors here, such as showing an error message
        });
    }
});





//update the task due description
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.task-description-form');
    const descriptionContainer = document.querySelector('.description-container');
    const buttonsContainer = document.querySelector('.task-description-buttons');
    const taskDescriptionText = document.getElementById("task-description");
    const hoverLabel = document.getElementById("hover-label");

    hoverLabel.addEventListener('click', function() {
        // Toggle visibility of the description container
        const isDisplayed = descriptionContainer.style.display !== 'none';
        descriptionContainer.style.display = isDisplayed ? 'none' : 'block';
        buttonsContainer.style.display = 'none';  // Keep buttons hidden initially
    });

    taskDescriptionText.addEventListener('focus', function() {
        buttonsContainer.style.display = 'block';  // Show buttons when text area is focused
    });

    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Stop the form from submitting normally

        const formData = new FormData(form);  // Create a FormData object from the form
        const actionUrl = form.action;  // Get the form action to send the POST request

        fetch(actionUrl, {
            method: 'POST',
            body: formData  // Send the form data
        })
        .then(response => response.json())  // Assuming the server responds with JSON
        .then(data => {
            console.log('Success:', data);
            // Update the hover label with the new description after successful submission
            hoverLabel.textContent = taskDescriptionText.value;
            descriptionContainer.style.display = 'none';
            buttonsContainer.style.display = 'none';
        })
        .catch(error => {
            console.error('Error:', error);
            // Optionally handle error situations
        });
    });

    window.cancelEdit = function() {
        descriptionContainer.style.display = 'none'; // Hide the entire container on cancel
        buttonsContainer.style.display = 'none'; // Also hide the buttons
    };
});



function handleChange(select) {
    const submitButton = document.getElementById('submit-button');
    if (select.value === 'delete') {
        submitButton.style.display = 'inline';  // Show the button if 'Delete Task' is selected
    } else {
        submitButton.style.display = 'none';  // Hide the button otherwise
    }
}