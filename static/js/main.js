// Socket.io connection
const socket = io.connect("http://localhost:5000");

// Admin View - Update Score
function updateScore(runs, isWicket = false) {
    const data = {
        runs: runs,
        is_wicket: isWicket
    };

    fetch('/api/update_score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });
}

// Real-time updates in User View
socket.on('score_update', function(data) {
    document.getElementById('user-score').textContent = data.runs + "/0";  // Modify as per score update structure
});
