
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