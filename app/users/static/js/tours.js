




function submitDelete(event) {
    event.preventDefault(); // Prevent the default link behavior

    const form = document.getElementById('delete-form');
    const deleteLink = document.getElementById('delete-package');
    const tourIdInput = document.getElementById('tour_id_to_delete');

    // Set the tour ID to the hidden input's value
    const tourId = deleteLink.dataset.tourId;
    tourIdInput.value = tourId;

    // Use FormData to handle form submission
    const formData = new FormData(form);

    // Perform the fetch request
    fetch(form.action, {
        method: 'POST',
        body: formData
    }).then(response => {
        if (response.ok) {
            return response.json(); // assuming JSON response
        }
        throw new Error('Network response was not ok: ' + response.statusText);
    }).then(data => {

        // Optionally remove the row or refresh
        form.style.display = "none";  // Corrected from `form.display.style`
        document.getElementById(`tour-row-${tourId}`).remove();
    }).catch(error => {
        console.error('Error:', error);
        alert('Error deleting tour.');
    });
}






function handleDeleteCheckboxChange(checkbox) {
    const deleteForm = document.getElementById('delete-form');
    const deleteLink = document.getElementById('delete-package');

    if (checkbox.checked) {
        deleteForm.style.display = 'block';
        deleteLink.dataset.tourId = checkbox.dataset.tourId;
    } else {
        deleteForm.style.display = 'none';
    }
}

