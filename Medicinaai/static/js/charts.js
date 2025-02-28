
document.addEventListener('DOMContentLoaded', async function() {
    const ctx = document.getElementById('healthChart').getContext('2d');
    let healthChart;

    // Fetch health data
    try {
        const response = await fetch('/api/health-history');
        const healthData = await response.json();
        
        const labels = healthData.map(d => d.timestamp);
        const systolicData = healthData.map(d => d.blood_pressure ? parseInt(d.blood_pressure.split('/')[0]) : null);
        const heartRateData = healthData.map(d => d.heart_rate);
        
        healthChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Blood Pressure (Systolic)',
                    data: systolicData,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'Heart Rate',
                    data: heartRateData,
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error fetching health data:', error);
    }

    // Handle health data form submission
    const healthDataForm = document.getElementById('healthDataForm');
    healthDataForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(healthDataForm);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch('/api/health-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            // Update risk score and details
            const riskScore = result.risk_score * 100;
            const riskScoreElement = document.querySelector('#riskScore .display-4');
            const riskLevelElement = document.querySelector('#riskScore .risk-level');
            const riskAdviceElement = document.querySelector('#riskScore .risk-advice');
            
            riskScoreElement.textContent = `${riskScore.toFixed(1)}%`;
            
            // Set risk level and advice
            let level, advice;
            if (riskScore < 20) {
                level = "Low Risk";
                advice = "Maintain healthy lifestyle";
            } else if (riskScore < 40) {
                level = "Moderate Risk";
                advice = "Consider lifestyle improvements";
            } else if (riskScore < 60) {
                level = "Increased Risk";
                advice = "Consult healthcare provider";
            } else {
                level = "High Risk";
                advice = "Urgent medical attention recommended";
            }
            
            riskLevelElement.textContent = level;
            riskAdviceElement.textContent = advice;
            
            // Refresh chart data
            const historyResponse = await fetch('/api/health-history');
            const newHealthData = await historyResponse.json();
            
            healthChart.data.labels = newHealthData.map(d => d.timestamp);
            healthChart.data.datasets[0].data = newHealthData.map(d => d.blood_pressure ? parseInt(d.blood_pressure.split('/')[0]) : null);
            healthChart.data.datasets[1].data = newHealthData.map(d => d.heart_rate);
            healthChart.update();
            
            // Show success message
            alert('Health data updated successfully!');
            
            // Reset form
            healthDataForm.reset();
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to update health data');
        }
    });
});
