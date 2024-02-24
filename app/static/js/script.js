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


// function showUpdateModal() {
//     document.getElementById('updateModal').style.display = 'block';
// }


function showUpdateModal() {
    const customerId = document.getElementById('customerIdToUpdate').value;


    fetch(`/customers/details?customer_id=${customerId}`)
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

    // Uncheck all checkboxes that might have been checked
    // var checkboxes = document.querySelectorAll('.delete-checkbox');
    // checkboxes.forEach(function(checkbox) {
    //     checkbox.checked = false;
    // });

    // Reset any other dynamic elements in the modal to their default state
    // For example, if you have a message element that shows the result of the deletion, hide it or reset its text
    // document.getElementById('resultMessage').style.display = 'none'; // Hide or reset other elements as needed

    // If there's a delete button that needs to be hidden
    // var deleteButton = document.getElementById('deleteButton');
    // if (deleteButton) {
    //     deleteButton.style.display = 'none';
    // }

    // If you're keeping track of the ID to delete somewhere, clear that too
    document.getElementById('customerIdToDelete').value = '';

}



document.querySelector('#updateModal .close-button').addEventListener('click', function() {
    document.querySelector('#updateModal').style.display = 'none';
});




function validateDeleteInput(input) {
    var confirmDeleteButton = document.getElementById('confirmDeleteButton');
    // Check if the input value is the word 'delete'
    var isDeleteTyped = input.value.toLowerCase() === 'delete';
    confirmDeleteButton.disabled = !isDeleteTyped; // Enable button only if 'delete' is typed
    // Show or hide the confirmation form based on the input
    document.getElementById('deleteConfirmForm').style.display = isDeleteTyped ? 'block' : 'none';
}





 function changeItemsPerPage(select) {
        window.location.href = "{{ url_for('customers.home_page', page=1) }}?per_page=" + select.value;
    }





// dynamically submits and reoute to homepage when there is any search in the search box



document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const form = document.getElementById('searchForm');
    const homeUrl = form.getAttribute('data-home-url'); // Get the home page URL from the data attribute

    // Load any saved search query from session storage and set it as the input value
    const savedQuery = sessionStorage.getItem('searchQuery');
    if (savedQuery) {
        searchInput.value = savedQuery;
    }

    searchInput.addEventListener('input', function() {
        const query = searchInput.value.trim();

        if (query.length >= 3) {
            // Save the current query to session storage right before submitting
            sessionStorage.setItem('searchQuery', query);
            form.submit();
        } else if (query.length === 0) {
            // Clear the saved query from session storage and redirect to home page
            sessionStorage.removeItem('searchQuery');
            window.location.href = homeUrl; // Use the homeUrl variable for redirection
        }
        // For cases where the user deletes the text down to below 3 characters but doesn't empty the input
        // Update the session storage with the current (non-empty) value
        else {
            sessionStorage.setItem('searchQuery', query);
        }
    });
});










