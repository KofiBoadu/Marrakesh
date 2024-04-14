// add customer functionality
document.addEventListener('DOMContentLoaded', function() {
    let customerBtn = document.getElementById("createCustomerBtn");
    let popUpForm = document.getElementById("popUp");
    let close = document.getElementById("close");
    let form = document.querySelector('.modal__form'); 
    customerBtn.addEventListener('click', function() {
        popUpForm.style.display = 'block';
    });

    close.addEventListener('click', function() {
        popUpForm.style.display = 'none';
        let contact_exist_div= document.getElementById("contactExists")
        let additionalFields = document.getElementById("additionalFields")
        contact_exist_div.style.display = "none"
        additionalFields.style.display = "none"

        form.reset(); 
    });
});










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
// Array to store the IDs of selected contacts
let selectedContactIds = [];
console.log(selectedContactIds)

function toggleDeleteButton(checkbox) {
    let deleteButton = document.getElementById('deleteButton');
    const contactId = checkbox.value;

    // Add or remove the contact ID from the array based on checkbox state
    if (checkbox.checked) {
        selectedContactIds.push(contactId);
    } else {
        selectedContactIds = selectedContactIds.filter(id => id !== contactId);
    }

    // Show or hide the delete button based on if any contacts are selected
    deleteButton.style.display = selectedContactIds.length > 0 ? 'flex' : 'none';
    
    console.log('Selected IDs:', selectedContactIds);
}


function showModal() {
    const deleteModal = document.getElementById('deleteModal');
    const deleteMessage1 = document.querySelector('.delete-message-1');
    const deleteTitle = document.querySelector('.delete-title');
    
    // Update modal title and message based on the number of selected contacts
    const deleteCount = selectedContactIds.length;
    deleteTitle.textContent = `Delete ${deleteCount} Record${deleteCount > 1 ? 's' : ''}?`;
    deleteMessage1.textContent = `You're about to delete ${deleteCount} record${deleteCount > 1 ? 's' : ''}. Deleted records can't be restored.`;
    
    // Populate the hidden input with the IDs of all selected contacts
    document.getElementById('customerIdToDelete').value = selectedContactIds.join(',');

    deleteModal.style.display = 'block';
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


function validateDeleteInput(input) {
    var confirmDeleteButton = document.getElementById('confirmDeleteButton');
    // Check if the input value is the word 'delete'
    var isDeleteTyped = input.value.toLowerCase() === 'delete';
    confirmDeleteButton.disabled = !isDeleteTyped; // Enable button only if 'delete' is typed
    // Show or hide the confirmation form based on the input
    document.getElementById('deleteConfirmForm').style.display = isDeleteTyped ? 'block' : 'none';
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













document.addEventListener('DOMContentLoaded', function() {
    var closeButton = document.querySelector('#updateModal .close-button');
    if (closeButton) {
        closeButton.addEventListener('click', function() {
            document.querySelector('#updateModal').style.display = 'none';
        });
    }
});









// table loading spinner 
document.addEventListener('DOMContentLoaded', function() {
    // Hide the spinner once the page is fully loaded
    document.getElementById('loadingSpinner').style.display = 'none';
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
            var existing_contact_link = document.getElementById("existing_contact_link");
            var contact_profile_avatar= document.getElementById("contact-profile-avatar");
            var existing_contact_email = document.getElementById("existing-contact-email");
            var create_contact_btn=document.getElementById("contact-submit-button");

            if (data.exists) {
                if (data.exists) {
                    contactExistsDiv.style.display = 'block';
                    create_contact_btn.style.display="none"
                    additionalFieldsDiv.style.display = 'none';
                    existing_contact_link.textContent = data.first_name + data.last_name;
                    contact_profile_avatar.textContent = data.first_name[0] + data.last_name[0];
                    existing_contact_email.textContent= data.email_address
                    // Update the href attribute with the correct blueprint prefix and contact_id
                    existing_contact_link.href = '/profiles/' + data.contact_id;
                    existing_contact_link.classList.add('active-link'); // Add your styling for an active link
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





//This optimizes the search function by just updating the table records and not the whole page
document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const homeUrl = searchForm.getAttribute('data-home-url') || '/';

    // Load any saved search query from storage and set it as the input value
    const savedQuery = localStorage.getItem('searchQuery');
    if (savedQuery) {
        searchInput.value = savedQuery;
    }

    searchInput.addEventListener('input', function() {
        const query = searchInput.value.trim();
        localStorage.setItem('searchQuery', query);

        if (query.length === 0) {
            performSearch(); // Redirect user to the home page
        } else if (query.length >= 3) {
            performSearch(); // Perform the AJAX search
        }
    });

    searchForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        performSearch();
    });
});

function performSearch() {
    console.log("performSearch called");
    const homeUrl = searchForm.getAttribute('data-home-url');
    const searchQuery = document.getElementById('searchInput').value.trim();

    if (searchQuery.length >= 3 || searchQuery.length ===0) {
        fetch(homeUrl, {
            method: 'POST',
            body: JSON.stringify({ search_query: searchQuery }),
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            updateTable(data);
        })
        .catch(error => console.error('Error:', error));
    }
}




function updateTable(data) {
    document.getElementById('table-body').innerHTML = data.html;
    if (data.total_records !== undefined) {
        const totalElement = document.getElementById('total');
        totalElement.textContent = `${parseInt(data.total_records).toLocaleString()} Records`;
    }
}







document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const homeUrl = searchForm.getAttribute('data-home-url') || '/'; // Assuming '/contacts/home' is the correct endpoint

    function fetchAndUpdateContent(page) {
        const itemsPerPageSelect = document.getElementById('items-per-page'); // Ensure fresh selection
        const itemsPerPage = itemsPerPageSelect.value;
        const searchQuery = searchInput ? searchInput.value.trim() : '';

        console.log(`Fetching content for page ${page}, items per page: ${itemsPerPage}, search query: "${searchQuery}"`);

        fetch(`${homeUrl}?page=${page}&items_per_page=${itemsPerPage}&search_query=${encodeURIComponent(searchQuery)}&_=${new Date().getTime()}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            console.log('Response status:', response.status); // Log the response status
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data); // Log the received data
            const tableBody = document.getElementById('table-body');
            const paginationControls = document.querySelector('.pagination-controls');
            if (tableBody && paginationControls) {
                tableBody.innerHTML = data.table_body_html;
                paginationControls.innerHTML = data.pagination_html;

                attachEventListenersToPaginationLinks();
                reinitializeItemsPerPageListener(); // Reinitialize event listener for the "items per page" dropdown
                
                updateItemsPerPageSelection(itemsPerPage); // Update the dropdown to reflect the current selection
            } else {
                console.error('Could not find table body or pagination controls elements.');
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    }

    function attachEventListenersToPaginationLinks() {
        document.querySelectorAll('.pagination-controls .pagination a').forEach(link => {
            link.removeEventListener('click', paginationLinkClicked); // Remove existing event listener to prevent duplicates
            link.addEventListener('click', paginationLinkClicked);
        });
    }

    function paginationLinkClicked(event) {
        event.preventDefault();
        const page = new URL(this.href).searchParams.get('page');
        console.log(`Pagination link clicked, navigating to page: ${page}`);
        fetchAndUpdateContent(page);
    }

    function reinitializeItemsPerPageListener() {
        const itemsPerPageSelect = document.getElementById('items-per-page');
        if (itemsPerPageSelect) {
            itemsPerPageSelect.removeEventListener('change', handleItemsPerPageChange); // Prevent duplicating listeners
            itemsPerPageSelect.addEventListener('change', handleItemsPerPageChange);
        }
    }

    function handleItemsPerPageChange() {
        console.log('Items per page changed to:', this.value);
        fetchAndUpdateContent(1); // Always revert back to the first page after a change in 'items per page'
    }

    function updateItemsPerPageSelection(selectedValue) {
        const itemsPerPageSelect = document.getElementById('items-per-page');
        if (itemsPerPageSelect) {
            itemsPerPageSelect.value = selectedValue;
        }
    }

    attachEventListenersToPaginationLinks(); // Initial call to attach event listeners to pagination links
    reinitializeItemsPerPageListener(); // Initial call to attach event listener to the "items per page" dropdown
});




