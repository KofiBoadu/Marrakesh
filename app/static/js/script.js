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
    document.getElementById('deleteModal').style.display = 'none';
}


function validateDeleteInput(input) {
    var confirmDeleteButton = document.getElementById('confirmDeleteButton');
    // Check if the input value is the word 'delete'
    var isDeleteTyped = input.value.toLowerCase() === 'delete';
    confirmDeleteButton.disabled = !isDeleteTyped; // Enable button only if 'delete' is typed
    // Show or hide the confirmation form based on the input
    document.getElementById('deleteConfirmForm').style.display = isDeleteTyped ? 'block' : 'none';
}

