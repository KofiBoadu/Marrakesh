

document.addEventListener("DOMContentLoaded", function() {
    var form = document.querySelector(".marketing-form");

    form.addEventListener("submit", function(e) {
        e.preventDefault(); // Prevent the actual form submission

        var emailBodyTextArea = document.getElementById("emailBody");
        var processedBody = autoLink(emailBodyTextArea.value);

        // Set the processed text back to the textarea
        emailBodyTextArea.value = processedBody;

        // Now submit the form programmatically
        e.currentTarget.submit();
    });

    function autoLink(text) {
        var urlRegex = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
        return text.replace(urlRegex, function(url) {
            return '<a href="' + url + '">' + url + '</a>';
        });
    }
});








document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('input[name="selected_campaigns"]');
    const deleteButton = document.getElementById('campaign_deleteButton');
    const hiddenInput = document.getElementById('deleting-campaign_id');

    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
          
            const checkedCheckboxes = document.querySelectorAll('input[name="selected_campaigns"]:checked');
            
            if (checkedCheckboxes.length > 0) {
                
                deleteButton.style.display = 'block';
                let id= hiddenInput.value = checkedCheckboxes[0].value;
              
            } else {
                deleteButton.style.display = 'none';
                hiddenInput.value = '';
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    // Setup Quill editor
    var quill = new Quill('#editor', { theme: 'snow' });

    // Correctly define the URL for the AJAX request dynamically
    var emailCampaignURL = document.querySelector('.marketing-form').getAttribute('data-email-campaign-url');

    // Get the form and attach a submit event listener
    var form = document.querySelector('.marketing-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Prepare data to be sent in the AJAX request
        var data = {
            fromAddress: document.getElementById('fromAddress').value,
            customerType: document.getElementById('customerType').value,
            emailSubject: document.getElementById('emailSubject').value,
            emailBody: quill.root.innerHTML // Get HTML content from Quill editor
        };

        // Make the AJAX request to the Flask route
        fetch(emailCampaignURL, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok.');
            return response.json(); // Parse JSON response
        })
        .then(data => {
            console.log('Success:', data);
            if(data.redirectUrl) {
                window.location.href = data.redirectUrl; // Use the server-provided URL for redirection
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Optionally handle errors here, such as displaying an error message to the user
        });
    });
});
