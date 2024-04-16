
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







document.addEventListener('DOMContentLoaded', function() {
    // Initialize the campaign ID and set up the initial content fetch
    initialize();

    function initialize() {
        const campaignIdInput = document.getElementById('campaign_id');
        if (!campaignIdInput) {
            console.error('Campaign ID input not found');
            return;
        }
        const campaignId = campaignIdInput.value;
        console.log("Campaign ID IS = ", campaignId);

        // Fetch initial content
        fetchAndUpdateContent(1); // Load the first page initially

        // Delegate click events for pagination to handle dynamic content loading
        document.addEventListener('click', function(event) {
            if (event.target.matches('.marketing-pagination-controls a')) {
                event.preventDefault();
                const page = new URL(event.target.href).searchParams.get('page');
                fetchAndUpdateContent(page);
            }
        });
    }

    // Function to fetch and update the table and pagination content dynamically
    function fetchAndUpdateContent(page) {
        const campaignId = document.getElementById('campaign_id').value;
        const itemsPerPageSelect = document.getElementById('items-per-page');
        const itemsPerPage = itemsPerPageSelect ? itemsPerPageSelect.value : 50;
        const url = `/marketing/campaign/performance/${campaignId}?page=${page}&items_per_page=${itemsPerPage}`;

        fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateDOMElements(data);
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    }

    // Update DOM elements with new data
    function updateDOMElements(data) {
        const tableBody = document.getElementById('performance-table-body');
        const paginationControls = document.querySelector('.marketing-pagination-controls');
        if (tableBody && paginationControls) {
            tableBody.innerHTML = data.marketing_table_body_html;
            paginationControls.innerHTML = data.marketing_pagination_html;
        } else {
            console.error('Could not find the performance table body or pagination controls elements.');
        }
    }
});

