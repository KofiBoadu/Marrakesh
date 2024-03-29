

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

//
//document.addEventListener('DOMContentLoaded', function() {
//            var quill = new Quill('#editor', {
//                theme: 'snow'
//            });
//
//            var form = document.querySelector('.marketing-form');
//            form.onsubmit = function(event) {
//                // Prevent the default form submission
//                event.preventDefault();
//
//                // Populate hidden input with the content from the rich text editor
//                var htmlContent = quill.root.innerHTML;
//                document.querySelector('input[name="emailBody"]').value = htmlContent;
//
//                // Now submit the form with the rich text content
//                form.submit();
//            };
//        });


//
//document.addEventListener("DOMContentLoaded", function() {
//    // Quill editor setup
//     var quill = new Quill('#editor', { theme: 'snow' });
//     var emailCampaignURL = "{{ url_for('marketing.send_marketing_emails') }}";
//     var form = document.getElementById('emailForm');
//
//      form.addEventListener('submit', function(event) {
//        event.preventDefault();
//
//    document.getElementById("sendMarketing-EmailButton").addEventListener('click', function() {
//        var fromAddress = document.getElementById('fromAddress').value;
//        var customerType = document.getElementById('customerType').value;
//        var emailSubject = document.getElementById('emailSubject').value;
//        var emailBody = quill.root.innerHTML; // Get HTML content from Quill editor
//
//        // Prepare data to be sent in the AJAX request
//        var data = {
//            fromAddress: fromAddress,
//            customerType: customerType,
//            emailSubject: emailSubject,
//            emailBody: emailBody
//        };
//
//        // AJAX request to your Flask route
//        fetch(emailCampaignURL, {
//            method: 'POST',
//            headers: {'Content-Type': 'application/json'},
//            body: JSON.stringify(data)
//        })
//        .then(response => {
//            if (response.ok) {
//                return response.json();  // Parse JSON response if request was successful
//            }
//            throw new Error('Network response was not ok.');  // Throw an error if not successful
//        })
//        .then(data => {
//            console.log('Success:', data);
//            // Redirect here after successful request
//            window.location.href = '/emails';
//        })
//        .catch((error) => {
//            console.error('Error:', error);
//            // Handle errors here, if needed
//        });
//    });
//});
//
