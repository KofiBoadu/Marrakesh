

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

