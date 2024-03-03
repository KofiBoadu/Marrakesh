function renderCustomerLocationChart() {
    const ctx = document.getElementById('customerLocationChart').getContext('2d');

    fetch('/analytics/location_chart')
        .then(response => response.json())
        .then(data => {
            const stateGroups = data.map(item => item.state_group);
            const customerCounts = data.map(item => item.customer_count).map(Number);

            const total = customerCounts.reduce((acc, value) => acc + value, 0);

            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: stateGroups,
                    datasets: [{
                        data: customerCounts,
                        backgroundColor: [
                            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#F7464A',
                            '#46BFBD', '#FDB45C', '#949FB1', '#4D5360', '#AC64AD'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                },
                plugins: [ChartDataLabels], // Make sure to register the plugin
                options: {
                    plugins: {
                        datalabels: {
                            color: '#fff',
                            anchor: 'end',
                            align: 'start',
                            formatter: function(value, context) {
                                const percentage = (value / total * 100).toFixed(2) + '%';
                                return context.chart.data.labels[context.dataIndex] + '\n' + percentage;
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error:', error));
}


renderCustomerLocationChart();











document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('genderChart').getContext('2d');
    let genderChart; // Variable to hold the chart instance

    function fetchDataAndUpdateChart(year = null) {
        // Construct the URL based on whether a year is provided
        let url = '/analytics/gender_chart';
        if (year) {
            url += '?gender_year=' + year;  // Append the year parameter if provided
        }

        fetch(url)
            .then(response => response.json())
            .then(genderData => {
                const labels = genderData.map(item => item[0]); // ['female', 'male']
                const data = genderData.map(item => item[1]); // [118, 40]

                // Update or create the chart
                if (genderChart) {
                    genderChart.data.labels = labels;
                    genderChart.data.datasets[0].data = data;
                    genderChart.update();
                } else {
                    genderChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Gender Distribution',
                                data: [120, 80], // Example data: 120 men, 80 women
                                backgroundColor: [
                                    '#36A2EB', // Solid color for men
                                    '#FF6384'  // Solid color for women
                                ],
                                borderColor: [
                                    '#36A2EB', // Border color for men
                                    '#FF6384'  // Border color for women
                                ],
                                borderWidth: 1
                            }]

                        },
                        options: {
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            },
                            plugins: {
                                legend: {
                                    display: true
                                }
                            }
                        }
                    });
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Event listener for the dropdown
    document.getElementById('genderSelectyear').addEventListener('change', function() {
        fetchDataAndUpdateChart(this.value);
    });

    // Fetch default data on initial load
    fetchDataAndUpdateChart();
});





const bookingsSelectYear = document.getElementById('bookingsSelectyear');
let bookingsChart = null;

    // Function to fetch bookings data
function fetchBookingsData(year = '') {
        // Build the URL with an optional year query parameter
        const url = year ? `/analytics/bookings_chart?bookings_year=${year}` : '/analytics/bookings_chart';
        fetch(url)
            .then(response => response.json())
            .then(data => updateChart(data))
            .catch(error => console.error('Error fetching data:', error));
    }

    // Function to update the chart
    function updateChart(data) {
        const ctx = document.getElementById('bookings-Chart').getContext('2d');
        
        // If the chart already exists, destroy it to create a new one with the new data
        if (bookingsChart) {
            bookingsChart.destroy();
        }

        // Create a new chart
        bookingsChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(item => item[0]), // Destination names
                datasets:[{
                    label: 'Number of Bookings',
                    data: data.map(item => item[1]), // Booking counts
                    backgroundColor: 'rgb(0, 123, 255)', // Solid blue color using RGB
                    borderColor: 'rgb(0, 123, 255)',
                    borderWidth: 1
                }]

            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // Event listener for the select element
    bookingsSelectYear.addEventListener('change', function() {
        fetchBookingsData(this.value);
    });

    // Initial chart load
fetchBookingsData();








 


    // Function to fetch revenue data and initialize the chart






    // Function to fetch revenue data and initialize the chart

    // Function to fetch revenue data and initialize the chart




    // Function to fetch revenue data and initialize the chart
    function fetchRevenueData() {
        fetch('/analytics/revenue_chart')
            .then(response => response.json())
            .then(data => {
                const totalRevenue = data.reduce((acc, [year, amount]) => acc + parseFloat(amount.replace(/,/g, '')), 0);
                // Format the total revenue
                const formattedTotalRevenue = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(totalRevenue);
                document.getElementById('total-revenue').textContent = formattedTotalRevenue;
                createRevenueChart(data);
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Adjusted function to determine bar color based on the specified revenue amount ranges
    function getBarColor(amount) {
        if (amount < 50000) return '#ff6384'; // Red for revenues less than $50k
        else if (amount >= 100000 && amount <= 250000) return '#fdd835'; // Yellow for revenues between $100k and $250k
        else return '#4bc0c0'; // Green for all other revenues
    }

    // Function to create the revenue chart
    function createRevenueChart(revenueData) {
        const ctx = document.getElementById('revenue-Chart').getContext('2d');
        const chartLabels = revenueData.map(item => item[0]);
        const chartData = revenueData.map(item => parseFloat(item[1].replace(/,/g, '')));
        const chartColors = chartData.map(getBarColor); // Determine the color for each bar based on the revenue range

        const revenueChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartLabels,
                datasets: [{
                    label: 'Revenue',
                    data: chartData,
                    backgroundColor: chartColors, // Apply the colors based on the revenue range
                    borderColor: chartColors,
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // Call the function to fetch data and create the chart when the page loads
    fetchRevenueData();




// prints page 

function printPage() {
    window.print();
}



