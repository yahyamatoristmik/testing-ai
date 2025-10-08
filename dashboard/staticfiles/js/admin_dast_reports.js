// static/js/admin_dast_reports.js
document.addEventListener('DOMContentLoaded', function() {
    // Handle AI recommendation generation
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('generate-ai-btn')) {
            e.preventDefault();
            const scanId = e.target.dataset.scanId;
            generateAIRecommendations(scanId, e.target);
        }
    });
    
    function generateAIRecommendations(scanId, button) {
        if (confirm('Generate AI recommendations untuk scan ini?')) {
            // Show loading
            const originalText = button.textContent;
            button.textContent = 'Generating...';
            button.disabled = true;
            
            // Make API call
            fetch('/dast-reports/scan/' + scanId + '/generate-ai-recommendations/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('AI recommendations berhasil digenerate!');
                    location.reload();
                } else {
                    alert('Error: ' + data.message);
                    resetButton(button, originalText);
                }
            })
            .catch(error => {
                alert('Error: ' + error);
                resetButton(button, originalText);
            });
        }
    }
    
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
    
    function resetButton(button, text) {
        button.textContent = text;
        button.disabled = false;
    }
});
