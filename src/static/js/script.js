function getTodayDate(time = "00:00:00") {
    const today = new Date();
    const yyyy = today.getFullYear();
    let mm = today.getMonth() + 1; // Months are zero-based
    let dd = today.getDate();
    if (mm < 10) mm = '0' + mm;
    if (dd < 10) dd = '0' + dd;

    // Return the date in the format YYYY-MM-DD with a customizable time (default to "00:00:00")
    return `${yyyy}-${mm}-${dd} ${time}`;
}

//// Function to load daily sales
function loadDailySales() {
    const startDate = getTodayDate("00:00:00");
    const endDate = getTodayDate("23:59:59");
    console.log('-------------------')
    console.log(startDate)
    console.log(endDate)
    fetch(`/order/summary?start_date=${startDate}&end_date=${endDate}`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#dailySalesTable tbody');
            tableBody.innerHTML = '';

            let totalOrders = 0;
            let totalCash = 0;
            let totalOnline = 0;

            data.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>₹${order.cart_price}</td>
                                <td>${order.payment_mode}</td>
                                <td>${order.user_phone}</td>
                                <td>${new Date(order.order_date * 1000).toLocaleString()}</td>`;
                tableBody.appendChild(row);

                totalOrders++
                if (order.payment_mode.toLowerCase() === 'cash') {
                    totalCash += order.cart_price;
                } else if (order.payment_mode.toLowerCase() === 'online') {
                    totalOnline += order.cart_price;
                }
            });
            document.getElementById('total-collection').textContent = `₹${(totalCash + totalOnline).toFixed(2)}`;
            document.getElementById('total-orders').textContent = totalOrders;
            document.getElementById('cash-collection').textContent = `₹${totalCash.toFixed(2)}`;
            document.getElementById('online-collection').textContent = `₹${totalOnline.toFixed(2)}`;
        })
        .catch(error => {
            console.error("Error fetching sales data:", error);
    });
}

document.addEventListener("DOMContentLoaded", function() {
    loadDailySales(); // Call the function once the DOM is loaded
});

//// Handle custom sales report form submission
//document.getElementById('customSalesForm').addEventListener('submit', function (event) {
//    event.preventDefault();
//    const startDate = document.getElementById('start_date').value;
//    const endDate = document.getElementById('end_date').value;
//
//    const formData = new FormData();
//    formData.append('start_date', startDate);
//    formData.append('end_date', endDate);
//
//    fetch('/custom_sales', {
//        method: 'POST',
//        body: formData
//    })
//    .then(response => response.json())
//    .then(data => {
//        const tableBody = document.querySelector('#customSalesTable tbody');
//        tableBody.innerHTML = '';
//        data.forEach(sale => {
//            const row = document.createElement('tr');
//            row.innerHTML = `<td>${sale.food_name}</td><td>$${sale.total_sales}</td>`;
//            tableBody.appendChild(row);
//        });
//    });
//});
//
//// Fetch inventory data
//fetch('/inventory')
//    .then(response => response.json())
//    .then(data => {
//        const tableBody = document.querySelector('#inventoryTable tbody');
//        tableBody.innerHTML = '';
//        data.forEach(item => {
//            const row = document.createElement('tr');
//            row.innerHTML = `<td>${item.name}</td><td>${item.quantity}</td>`;
//            tableBody.appendChild(row);
//        });
//    });
//
// Function to show the selected section and hide others
function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.style.display = 'none');

    // Show the selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}

// Load daily sales by default
showSection('daily_sales');
