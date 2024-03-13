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



// document.querySelector('#updateModal .close-button').addEventListener('click', function() {
//     document.querySelector('#updateModal').style.display = 'none';
// });

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


 function changeItemsPerPage(select) {
        window.location.href = "{{ url_for('customers.home_page', page=1) }}?per_page=" + select.value;
    }











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
            event.preventDefault(); // Prevent form submission if the search query is empty
            // Optionally redirect to home here too, if immediate redirection is desired
            // redirectToHomePage();
            return false;
        }
        // Note: No need to clear the search here as we want to keep the input after submission
    });
});




// table loading spinner 


document.addEventListener('DOMContentLoaded', function() {
    // Hide the spinner once the page is fully loaded
    document.getElementById('loadingSpinner').style.display = 'none';
});




