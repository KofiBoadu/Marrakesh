
document.addEventListener('DOMContentLoaded', (event) => {
  const url_parameters = new URLSearchParams(window.location.search);
  const message = url_parameters.get('message');
  const campaignId = url_parameters.get('campaign_id');

  // Create a unique key for sessionStorage based on campaignId
  const messageShownKey = `messageShown_${campaignId}`;

  if (message === 'email_processing' && sessionStorage.getItem(messageShownKey) !== 'true') {
    const messageElement = document.getElementById('email-processing-message');
    messageElement.style.display = 'block';
    // Mark that the message has been shown for this specific campaign
    sessionStorage.setItem(messageShownKey, 'true');

    // Set the display back to 'none' after 10 seconds
    setTimeout(() => {
      messageElement.style.display = 'none';
    }, 10000); // 10000 milliseconds = 10 seconds
  }
});
