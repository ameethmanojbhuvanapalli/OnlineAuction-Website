

function formatTime(seconds) {
    var days = Math.floor(seconds / (24 * 60 * 60));
    var hours = Math.floor((seconds % (24 * 60 * 60)) / (60 * 60));
    var minutes = Math.floor((seconds % (60 * 60)) / 60);
    var remainingSeconds = seconds % 60;

    return `${days}d ${hours}hrs ${minutes}min ${remainingSeconds}sec`;
}

function timeStringToSeconds(timeString) {
    var parts = timeString.split(':');
    var hours = parseInt(parts[0], 10);
    var minutes = parseInt(parts[1], 10);
    var seconds = parseInt(parts[2], 10);
    return hours * 3600 + minutes * 60 + seconds;
}

function openModal(auctionId, auctionText) {
    // Set modal title
    document.getElementById('modalTitle').innerText = auctionText;

    // Clear existing rows in the modal table
    var modalTableBody = document.getElementById('modalTableBody');
    modalTableBody.innerHTML = '';

    // Fetch bid data using auctionId
    fetch(`/myBids/${auctionId}`)
        .then(response => response.json())
        .then(data => {
            data.forEach(function (bid) {
                var row = modalTableBody.insertRow();
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);

                cell1.innerHTML = bid.Bid_amt;
                cell2.innerHTML = bid.Bid_time;
            });

            // Show the Bootstrap modal
            var myModal = new bootstrap.Modal(document.getElementById('bidsModal'));
            myModal.show();
        })
        .catch(error => console.error('Error fetching bid data:', error));
}

function closeModal() {
    // Close the Bootstrap modal
    var myModal = new bootstrap.Modal(document.getElementById('bidsModal'));
    myModal.hide();
}