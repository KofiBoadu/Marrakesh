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
    if (checkbox.checked) {
        document.getElementById('customerIdToDelete').value = checkbox.value;
        
    
    }
}

function showModal() {
    document.getElementById('deleteModal').style.display = 'block';
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
    var checkboxes = document.querySelectorAll('.delete-checkbox');
    checkboxes.forEach(function(checkbox) {
        checkbox.checked = false;
    });

    // Reset any other dynamic elements in the modal to their default state
    // For example, if you have a message element that shows the result of the deletion, hide it or reset its text
    // document.getElementById('resultMessage').style.display = 'none'; // Hide or reset other elements as needed

    // If there's a delete button that needs to be hidden
    var deleteButton = document.getElementById('deleteButton');
    if (deleteButton) {
        deleteButton.style.display = 'none';
    }

    // If you're keeping track of the ID to delete somewhere, clear that too
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

