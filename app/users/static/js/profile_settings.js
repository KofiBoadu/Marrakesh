



document.addEventListener('DOMContentLoaded', function() {
  const checkboxes = document.querySelectorAll('.user-checkbox');
  checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
      if (this.checked) {
        // Retrieve the user ID from the data attribute
        const userId = this.getAttribute('data-user-id');
        // Update the hidden input's value
        document.getElementById('hiddenUserId').value = userId;
      }
    });
  });
});

