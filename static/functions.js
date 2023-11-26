
function openDialog(auctionId,auctionText) {
    document.getElementById('dialogTitle').innerText = auctionText;
    // Get the table body in the dialog
    var dialogTableBody = document.getElementById('dialogTable').getElementsByTagName('tbody')[0];
    
    // Clear existing rows in the dialog table
    dialogTableBody.innerHTML = '';
    
    // Fetch bid data using auctionId
    fetch(`/myBids/${auctionId}`)
        .then(response => response.json())
        .then(data => {
            data.forEach(function(bid) {

            var row = dialogTableBody.insertRow();
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);

            cell1.innerHTML = bid.Bid_amt;
            cell2.innerHTML = bid.Bid_time;
        });

        document.getElementById('bidsDialog').showModal();
    })
    .catch(error => console.error('Error fetching bid data:', error));
}
    
function closeDialog() {
    document.getElementById('bidsDialog').close();
}

document.addEventListener("DOMContentLoaded", function () {
    // Get today's date in the format expected by datetime-local input
    var today = new Date().toISOString().slice(0, 16);
    // Set the minimum value for the Start Date input
    var startDateInput = document.getElementsByName("startDate")[0];
    startDateInput.min = today;

    // Set up event listener for Start Date input
    startDateInput.addEventListener("input", function () {
        var startDate = new Date(startDateInput.value);
        startDate.setMinutes(startDate.getMinutes() + 24 * 60 + 5 * 60 + 30);
        var endDate = startDate.toISOString().slice(0, 16);
        var endDateInput = document.getElementsByName("endDate")[0];
        endDateInput.value = endDate;
        endDateInput.min = endDate;
    });
});