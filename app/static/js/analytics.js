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