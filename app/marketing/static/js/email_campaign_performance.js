
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









// document.addEventListener('DOMContentLoaded', function() {
//   // Get the campaign ID from a hidden input field
//   const campaignIdInput = document.getElementById('campaign_id');
//   if (!campaignIdInput) {
//       console.error('Campaign ID input not found');
//       return;
//   }
//   const campaignId = campaignIdInput.value;

//   // Fetch and update the table and pagination content dynamically
//   function fetchAndUpdateContent(page) {
//       const itemsPerPageSelect = document.getElementById('items-per-page');
//       const itemsPerPage = itemsPerPageSelect ? itemsPerPageSelect.value : 50;
//       const url = `/marketing/campaign/performance/${campaignId}?page=${page}&items_per_page=${itemsPerPage}`;

//       fetch(url, {
//           method: 'GET',
//           headers: {
//               'Accept': 'application/json',
//               'X-Requested-With': 'XMLHttpRequest'
//           }
//       })
//       .then(response => {
//           if (!response.ok) {
//               throw new Error('Network response was not ok');
//           }
//           return response.json();
//       })
//       .then(data => {
//           const tableBody = document.getElementById('performance-table-body');
//           const paginationControls = document.querySelector('.marketing-pagination-controls');
//           if (tableBody && paginationControls) {
//               tableBody.innerHTML = data.table_body_html;
//               paginationControls.innerHTML = data.pagination_html;

//               // Reattach event listeners to new pagination links
//               attachEventListenersToPaginationLinks();
//           } else {
//               console.error('Could not find the performance table body or pagination controls elements.');
//           }
//       })
//       .catch(error => {
//           console.error('Fetch error:', error);
//       });
//   }

//   // Attach event listeners to pagination links
//   function attachEventListenersToPaginationLinks() {
//       const links = document.querySelectorAll('.marketing-pagination-controls a');
//       links.forEach(link => {
//           link.removeEventListener('click', handlePaginationLinkClick); // Remove existing event listener to prevent duplicates
//           link.addEventListener('click', handlePaginationLinkClick);
//       });
//   }

//   // Handle pagination link clicks
//   function handlePaginationLinkClick(event) {
//       event.preventDefault();
//       const page = new URL(this.href).searchParams.get('page');
//       fetchAndUpdateContent(page);
//   }

//   // Initial call to attach event listeners to existing pagination links
//   attachEventListenersToPaginationLinks();
// });
