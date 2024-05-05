// add customer functionality
document.addEventListener('DOMContentLoaded', function () {
    let customerBtn = document.getElementById("createCustomerBtn");
    let popUpForm = document.getElementById("popUp");
    let close = document.getElementById("close");
    let form = document.querySelector('.modal__form');
    let additionalFields = document.getElementById("additionalFields")
    let phoneInput = document.getElementById("phone");
    let stateSelect = document.getElementById("state");
    let maleRadio = document.getElementById("male");
    let femaleRadio = document.getElementById("female");
    let statusSelect = document.getElementsByName("lead_status")[0]; // Assuming there's only one element with the name "lead_status"
    customerBtn.addEventListener('click', function () {
        additionalFields.style.display = "block"

        popUpForm.style.display = 'block';
        additionalFields.style.filter = "blur(5px)";
        phoneInput.disabled = true;
        stateSelect.disabled = true;
        maleRadio.disabled = true;
        femaleRadio.disabled = true;
        statusSelect.disabled = true;
        ;

    });

    close.addEventListener('click', function () {
        popUpForm.style.display = 'none';
        let contact_exist_div = document.getElementById("contactExists")

        contact_exist_div.style.display = "none"
        additionalFields.style.display = "none"

        form.reset();
    });
});










// //add tour modal form
// document.addEventListener('DOMContentLoaded', function() {
//     let tourBtn= document.getElementById("tourBtn");
//     let tourForm=document.getElementById("tourForm");
//     let exit=document.getElementById("exit");

//     tourBtn.addEventListener('click',function(){
//         tourForm.style.display='block'
//     })

//     exit.addEventListener('click',function(){
//         tourForm.style.display='none'
//     })
// })












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
        id = document.getElementById('customerIdToUpdate').value = checkbox.value;
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
            let name = document.getElementById('updatefirstName').value = data.first_name || '';
            document.getElementById('updatelastName').value = data.last_name || '';
            document.getElementById('updateemail').value = data.email_address || '';
            document.getElementById('updatephone').value = data.phone_number || '';
            document.getElementById('updatestate').value = data.state_address || '';

            // Display the modal
            document.getElementById('updateModal').style.display = 'block';
            console.log(customerId, "customer ID after click the logo ")
            console.log(name, "customer name")
        })
        .catch(error => console.error('Error:', error));
}













document.addEventListener('DOMContentLoaded', function () {
    var closeButton = document.querySelector('#updateModal .close-button');
    if (closeButton) {
        closeButton.addEventListener('click', function () {
            document.querySelector('#updateModal').style.display = 'none';
        });
    }
});









// table loading spinner 
document.addEventListener('DOMContentLoaded', function () {
    // Hide the spinner once the page is fully loaded
    document.getElementById('loadingSpinner').style.display = 'none';
});












document.addEventListener("DOMContentLoaded", function () {
    var emailField = document.getElementById("email");

    emailField.addEventListener("input", function (event) {
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
                var contact_profile_avatar = document.getElementById("contact-profile-avatar");
                var existing_contact_email = document.getElementById("existing-contact-email");
                var create_contact_btn = document.getElementById("contact-submit-button");
                let phoneInput = document.getElementById("phone");
                let stateSelect = document.getElementById("state");
                let maleRadio = document.getElementById("male");
                let femaleRadio = document.getElementById("female");
                let statusSelect = document.getElementsByName("lead_status")[0]; // Assuming there's only one element with the name "lead_status"

                // Enable the input elements

                if (data.exists) {
                    if (data.exists) {
                        contactExistsDiv.style.display = 'block';
                        create_contact_btn.style.display = "none"
                        additionalFieldsDiv.style.display = 'none';
                        existing_contact_link.textContent = data.first_name + data.last_name;
                        contact_profile_avatar.textContent = data.first_name[0] + data.last_name[0];
                        existing_contact_email.textContent = data.email_address
                        // Update the href attribute with the correct blueprint prefix and contact_id
                        existing_contact_link.href = '/profiles/' + data.contact_id;
                        existing_contact_link.classList.add('active-link'); // Add your styling for an active link
                    } // Make sure to style this class as needed
                } else {
                    contactExistsDiv.style.display = 'none';
                    additionalFieldsDiv.style.display = 'block';
                    create_contact_btn.style.display = 'block';
                    additionalFieldsDiv.style.filter = "none";
                    phoneInput.disabled = false;
                    stateSelect.disabled = false;
                    maleRadio.disabled = false;
                    femaleRadio.disabled = false;
                    statusSelect.disabled = false;
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
            event.preventDefault();
    });


    document.getElementById("popUp").style.display = 'none';
    
});




document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const itemsPerPageSelect = document.getElementById('items-per-page');
    const tableBody = document.getElementById('table-body');
    const paginationControls = document.querySelector('.pagination-controls');
    const homeUrl = searchForm.getAttribute('data-home-url') || '/contacts/home';

    // Load any saved search query from local storage
    const savedQuery = localStorage.getItem('searchQuery');
    if (savedQuery) {
        searchInput.value = savedQuery;
    }

    // Function to perform search and update page content
    function performSearch(page = 1) {
        const searchQuery = searchInput.value.trim();
        const itemsPerPage = itemsPerPageSelect.value;

        fetch(homeUrl, {
            method: 'POST',
            body: JSON.stringify({
                search_query: searchQuery,
                page: page,
                items_per_page: itemsPerPage
            }),
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            updatePageContent(data);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load data: ' + error.message);
        });
    }

    // Function to update the table and pagination controls
    function updatePageContent(data) {
        tableBody.innerHTML = data.html; // Make sure the key matches with what's sent from server
        paginationControls.innerHTML = data.pagination_html;// Match the key
        document.getElementById('total').textContent = `${data.total_records.toLocaleString()} Records`;
        attachEventListenersToPaginationLinks();
    }

    // Function to attach event listeners to pagination links
    function attachEventListenersToPaginationLinks() {
        document.querySelectorAll('.pagination-controls .pagination a').forEach(link => {
            link.removeEventListener('click', paginationLinkClicked);
            link.addEventListener('click', paginationLinkClicked);
        });
    }

    // Function to handle pagination link clicks
    function paginationLinkClicked(event) {
        event.preventDefault();
        const page = new URL(this.href).searchParams.get('page');
        performSearch(page);
    }

    // Event listeners
    searchInput.addEventListener('input', function () {
        const query = searchInput.value.trim();
        localStorage.setItem('searchQuery', query);
        if (query.length === 0 || query.length >= 3) {
            performSearch();
        }
    });

    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        performSearch();
    });

    itemsPerPageSelect.addEventListener('change', function () {
        performSearch(1); // Reset to first page when changing items per page
    });

    // Initial call to attach event listeners to existing pagination links
    attachEventListenersToPaginationLinks();
});

























document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filtering-form');
    const activeFiltersContainer = document.getElementById('active-filters');

    filterForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(filterForm);
        updateActiveFilters(formData);
        performFilterRequest(formData);
    });

    function updateActiveFilters(formData) {
        activeFiltersContainer.innerHTML = ''; // Clear current filters display
        formData.forEach((value, key) => {
            if (value) {
                const filterTag = document.createElement('div');
                filterTag.textContent = `${key.charAt(0).toUpperCase() + key.slice(1)}: ${value}`;
                const closeButton = document.createElement('button');
                closeButton.textContent = '×';
                closeButton.onclick = function() {
                    removeFilter(key);
                };
                filterTag.appendChild(closeButton);
                activeFiltersContainer.appendChild(filterTag);
            }
        });
    }

    function removeFilter(key) {
        const input = document.querySelector(`[name="${key}"]`);
        if (input) {
            input.value = ''; // Reset the filter
            filterForm.submit(); // Re-submit the form to update filters
        }
    }

    function performFilterRequest(formData) {
        const filterData = {};
        formData.forEach((value, key) => {
            if (value) filterData[key] = value;
        });

        fetch(filterForm.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(filterData)
        })
        .then(response => response.json())
        .then(data => {
            // Update the table body with filtered data
            document.getElementById('table-body').innerHTML = data.html;
            document.getElementById('total').textContent = `${data.total_records} Records`;
            // Update pagination controls if needed
            if (data.pagination_html) {
                document.querySelector('.pagination-controls').innerHTML = data.pagination_html;
            }
        })
        .catch(error => {
            console.error('Fetch Error:', error);
        });
    }
});
















//UPDATE CONTACT OWNER FUNCTIONS in the rows
function showUserList(contactId) {
    document.getElementById('selected-contact-id').value = contactId;
    document.getElementById('user-list-popup').style.display = 'block';
}

function selectUser(userId) {
    document.getElementById('selected-user-id').value = userId;
    document.getElementById('update-owner').style.display = 'block';
    document.getElementById('user-list-popup').style.display = 'none';
}

function closeForm() {
    document.getElementById('update-owner').style.display = 'none';
}


//Function to handle form submission using Fetch API
function submitForm(event) {
    event.preventDefault(); // Prevent default form submission

    const form = document.getElementById('update-owner-form');
    const url = form.getAttribute('data-url'); // Get the URL from data attribute
    const userId = document.getElementById('selected-user-id').value;
    const contactId = document.getElementById('selected-contact-id').value;

    const data = new FormData();
    data.append('user_id', userId);
    data.append('contact_id', contactId);

    fetch(url, {
        method: 'POST',
        body: data
    })
    .then(response => response.json())
    .then(data => {
        if (data.owner) {
            // Update the owner cell directly
            document.getElementById('contact-owner-' + contactId).textContent = data.owner;
            closeForm(); // Close the form
        } else {
            alert('Failed to update contact owner: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update contact owner.');
    });
}

// Add event listener to the form
document.getElementById('update-owner-form').addEventListener('submit', submitForm);
