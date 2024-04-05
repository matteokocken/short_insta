const API_URL = ''; //http://localhost:5000

document.getElementById('submitBtn').addEventListener('click', function() {
    const videoUrl = document.getElementById('videoUrl').value;
    if (!videoUrl) {
        showMessage('Please enter a video URL.', 'error');
        return;
    }

    toggleLoading(true);
    fetch(API_URL + '/get_subtitles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ video_url: videoUrl }),
    })
    .then(response => response.json())
    .then(data => {
        toggleLoading(false);
        if (data.error) {
            showMessage(data.error, 'error');
        } else {
            showMessage(data.subtitles, 'success');
        }
    })
    .catch(error => {
        toggleLoading(false);
        showMessage('Failed to fetch subtitles. Please try again.', 'error');
        console.error('Error:', error);
    });
});

function toggleLoading(show) {
    document.getElementById('loading').classList.toggle('hidden', !show);
}

function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = message;
    messageDiv.className = '';
    if (type === 'error') {
        messageDiv.classList.add('error');
    } else {
        messageDiv.classList.add('success');
    }
}