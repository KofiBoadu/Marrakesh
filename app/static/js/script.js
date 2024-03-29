//add customer functionality
document.addEventListener('DOMContentLoaded', function() {
    let customerBtn= document.getElementById("createCustomerBtn");
    let popUpForm=document.getElementById("popUp");
    let close=document.getElementById("close");

    customerBtn.addEventListener('click',function(){
        popUpForm.style.display='block'
    })

    close.addEventListener('click',function(){
        popUpForm.style.display='none'
    })
})

//add tour modal form
document.addEventListener('DOMContentLoaded', function() {
    let tourBtn= document.getElementById("tourBtn");
    let tourForm=document.getElementById("tourForm");
    let exit=document.getElementById("exit");

    tourBtn.addEventListener('click',function(){
        tourForm.style.display='block'
    })

    exit.addEventListener('click',function(){
        tourForm.style.display='none'
    })
})


//delete functionality
function toggleDeleteButton(checkbox) {
    let deleteButton = document.getElementById('deleteButton');
    deleteButton.style.display = checkbox.checked ? 'flex' : 'none';
    let id;
    if (checkbox.checked) {
        id=document.getElementById('customerIdToDelete').value = checkbox.value;
        console.log('Checkbox is checked, ID:', id);
        
    
    }
}


//update details functionality 
function updateCustomerDetails(checkbox) {
    let updateButton = document.getElementById('updateButton');
    updateButton.style.display = checkbox.checked ? 'flex' : 'none';
    let id;
    if (checkbox.checked) {
        id=document.getElementById('customerIdToUpdate').value = checkbox.value;
        console.log('Checkbox is checked, ID:', id);
    }

}




function showModal() {
    document.getElementById('deleteModal').style.display = 'block';
}



function showUpdateModal() {
    const customerId = document.getElementById('customerIdToUpdate').value;


    fetch(`/contacts/details?customer_id=${customerId}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Populate the form fields in the modal with the customer details
        let name= document.getElementById('updatefirstName').value = data.first_name || '';
        document.getElementById('updatelastName').value = data.last_name || '';
        document.getElementById('updateemail').value = data.email_address || '';
        document.getElementById('updatephone').value = data.phone_number || '';
        document.getElementById('updatestate').value = data.state_address || '';

        // Display the modal
        document.getElementById('updateModal').style.display = 'block';
        console.log(customerId,"customer ID after click the logo ")
        console.log(name,"customer name")
    })
    .catch(error => console.error('Error:', error));
}








function closeModal() {
    // Hide the modal
    document.getElementById('deleteModal').style.display = 'none';

    // Clear the input field where the user types 'delete'
    var deleteConfirmInput = document.getElementById('deleteConfirmInput');
    deleteConfirmInput.value = '';

    // Disable the 'Delete' button since the input is now empty
    var confirmDeleteButton = document.getElementById('confirmDeleteButton');
    confirmDeleteButton.disabled = true;

    // Hide the delete confirmation form
    var deleteConfirmForm = document.getElementById('deleteConfirmForm');
    deleteConfirmForm.style.display = 'none';


    document.getElementById('customerIdToDelete').value = '';

}





document.addEventListener('DOMContentLoaded', function() {
    var closeButton = document.querySelector('#updateModal .close-button');
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            document.querySelector('#updateModal').style.display = 'none';
        });
    }
});



function validateDeleteInput(input) {
    var confirmDeleteButton = document.getElementById('confirmDeleteButton');
    // Check if the input value is the word 'delete'
    var isDeleteTyped = input.value.toLowerCase() === 'delete';
    confirmDeleteButton.disabled = !isDeleteTyped; // Enable button only if 'delete' is typed
    // Show or hide the confirmation form based on the input
    document.getElementById('deleteConfirmForm').style.display = isDeleteTyped ? 'block' : 'none';
}



document.addEventListener('DOMContentLoaded', function() {
    // Function to handle changes in items per page
    function changeItemsPerPage(selectObject) {
        var selectedValue = selectObject.value; // Get the selected value from the dropdown
        var currentItemsPerPage = getCurrentItemsPerPage(); // Get the current items per page from the URL

        // Only redirect if the selected value is different from the current value
        if (selectedValue.toString() !== currentItemsPerPage) {
            var searchParams = new URLSearchParams(window.location.search);
            searchParams.set('items_per_page', selectedValue);
            searchParams.set('page', 1); // Optionally reset to the first page

            // Redirect to the same route with updated query parameters
            window.location.search = searchParams.toString();
        }
    }

    // Function to get the current 'items_per_page' value from the URL
    function getCurrentItemsPerPage() {
        var params = new URLSearchParams(window.location.search);
        return params.get('items_per_page') || '50'; // Default to 50 if not present
    }

    // Attach the change event listener to the dropdown
    var selectElement = document.getElementById('items-per-page');
    if (selectElement) {
        selectElement.addEventListener('change', function() {
            changeItemsPerPage(this);
        });
    }
});











// dynamically submits and reoute to homepage when there is any search in the search box
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const form = document.getElementById('searchForm');
    // Assuming you have a way to define or get the home URL
    const homeUrl = form.getAttribute('data-home-url') || '/'; // Fallback to root if not specified

    // Function to clear search input and storage
    function clearSearch() {
        searchInput.value = '';
        localStorage.removeItem('searchQuery'); // Using localStorage for persistence
    }

    // Redirect to home page if input is empty
    function redirectToHomePage() {
        window.location.href = homeUrl; // Redirect user to the home page
    }

    // Load any saved search query from storage and set it as the input value
    const savedQuery = localStorage.getItem('searchQuery');
    if (savedQuery) {
        searchInput.value = savedQuery;
    }

    searchInput.addEventListener('input', function() {
        const query = searchInput.value.trim();
        localStorage.setItem('searchQuery', query);

        // Auto-submit logic: submit form if query length is at least 3 characters
        if (query.length >= 3) {
            form.submit(); // Trigger form submission
        } else if (query.length === 0) {
            // Redirect to home page if the input becomes empty
            redirectToHomePage();
        }
    });

    form.addEventListener('submit', function(event) {
        const query = searchInput.value.trim();
        if (query.length === 0) {
            event.preventDefault();

            return false;
        }

    });
});




// table loading spinner 
document.addEventListener('DOMContentLoaded', function() {
    // Hide the spinner once the page is fully loaded
    document.getElementById('loadingSpinner').style.display = 'none';
});




document.addEventListener('DOMContentLoaded', function() {
  const roleId = parseInt(document.getElementById('login-user-role-id').value, 10);
  if (roleId > 1) {
    const exportButton = document.querySelector('.export');
    if (exportButton) {
      exportButton.disabled = true;
      exportButton.classList.add('disabled'); // Use 'disabled' class for styling
    }
  }
});









document.addEventListener("DOMContentLoaded", function() {
    var emailField = document.getElementById("email");

    emailField.addEventListener("input", function() {
        var email = this.value.trim();
        if (email.length === 0) {
            // If the email is empty, don't make the fetch call.
            return;
        }

        fetch('/contacts/check-email/contact-existence', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email }),
        })
        .then(response => response.json())
        .then(data => {
            var contactExistsDiv = document.getElementById("contactExists");
            var additionalFieldsDiv = document.getElementById("additionalFields");
            var existingEmailLink = document.getElementById("existingEmailLink");
            var create_contact_btn=document.getElementById("contact-submit-button");

            if (data.exists) {
                if (data.exists) {
                    contactExistsDiv.style.display = 'block';
                    create_contact_btn.style.display="none"
                    additionalFieldsDiv.style.display = 'none';
                    existingEmailLink.textContent = email;
                    // Update the href attribute with the correct blueprint prefix and contact_id
                    existingEmailLink.href = '/profiles/' + data.contact_id;
                    existingEmailLink.classList.add('active-link'); // Add your styling for an active link
                } // Make sure to style this class as needed
            } else {
                contactExistsDiv.style.display = 'none';
                additionalFieldsDiv.style.display = 'block';
                create_contact_btn.style.display='block';
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

  
    document.getElementById("popUp").style.display = 'none';
});





