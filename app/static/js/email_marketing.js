

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


document.addEventListener('DOMContentLoaded', function() {
            var quill = new Quill('#editor', {
                theme: 'snow'
            });

            var form = document.querySelector('.marketing-form');
            form.onsubmit = function(event) {
                // Prevent the default form submission
                event.preventDefault();

                // Populate hidden input with the content from the rich text editor
                var htmlContent = quill.root.innerHTML;
                document.querySelector('input[name="emailBody"]').value = htmlContent;

                // Now submit the form with the rich text content
                form.submit();
            };
        });




