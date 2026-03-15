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

function toggleSidebar(){
  document.querySelector(".sidebar").classList.toggle("open");
}

const sidebar = document.querySelector(".sidebar");
const overlay = document.getElementById("overlay");
const toggleBtn = document.getElementById("sidebarToggle");

toggleBtn.addEventListener("click", () => {
  sidebar.classList.toggle("open");
  overlay.classList.toggle("show");
});

// Close sidebar when clicking outside
overlay.addEventListener("click", () => {
  sidebar.classList.remove("open");
  overlay.classList.remove("show");
});

function animateNumber(elementId, targetValue, duration = 1000) {
    const element = document.getElementById(elementId);
    const startValue = 0;
    const startTime = performance.now();

    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1); // Ensure progress doesn't exceed 1

        // Calculate the current value
        const currentValue = startValue + (targetValue - startValue) * progress;

        // Update the element with the current value (rounded to two decimal places)
        element.textContent = `₹${currentValue.toFixed(2)}`;

        // If not done, request another animation frame
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }

    // Start the animation
    requestAnimationFrame(updateNumber);
}

function loadDailySales(){
    const startDate = getTodayDate("00:00:00");
    const endDate = getTodayDate("23:59:59");

    loadSales(startDate, endDate, 'daily')
  }

function loadCustomSales(){
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    var formattedStartDate = new Date(startDate).toISOString().slice(0, 19).replace('T', ' ');
    var formattedEndDate = new Date(endDate).toISOString().slice(0, 19).replace('T', ' ');

    // Ensure both dates are selected
    if (!formattedStartDate || !formattedEndDate) {
        alert("Please select both start and end dates.");
        return;
    }
    loadSales(formattedStartDate, formattedEndDate, 'custom')
  }

//// Function to load daily sales
function loadSales(startDate, endDate, tableType) {
    fetch(`/order/summary?start_date=${startDate}&end_date=${endDate}`)
        .then(response => response.json())
        .then(data => {
            let tableBody;
            if (tableType === 'daily') {
                tableBody = document.querySelector('#dailySalesTable tbody');
            } else if (tableType === 'custom') {
                tableBody = document.querySelector('#customSalesTable tbody');
            } else {
                console.error('Invalid table type');
                return;
            }
            tableBody.innerHTML = '';

            let totalOrders = 0;
            let totalCash = 0;
            let totalOnline = 0;

            data.forEach(order => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>₹${order.cart_price}</td>
                                <td>${order.payment_mode}</td>
                                <td>${order.user_phone}</td>
                                <td>${order.order_id}</td>
                                <td>${new Date(order.order_date * 1000).toLocaleString()}</td>`;
                tableBody.appendChild(row);

                totalOrders++
                if (order.payment_mode.toLowerCase() === 'cash') {
                    totalCash += order.cart_price;
                } else if (order.payment_mode.toLowerCase() === 'online') {
                    totalOnline += order.cart_price;
                }
            });
            if (tableType === 'daily') {
                animateNumber('total-collection-daily', totalCash + totalOnline);
                document.getElementById('total-orders-daily').textContent = totalOrders;
                document.getElementById('cash-collection-daily').textContent = `₹${totalCash.toFixed(2)}`;
                document.getElementById('online-collection-daily').textContent = `₹${totalOnline.toFixed(2)}`;
            } else if (tableType === 'custom') {
                animateNumber('total-collection-custom', totalCash + totalOnline);
                document.getElementById('total-orders-custom').textContent = totalOrders;
                document.getElementById('cash-collection-custom').textContent = `₹${totalCash.toFixed(2)}`;
                document.getElementById('online-collection-custom').textContent = `₹${totalOnline.toFixed(2)}`;
            } else {
                console.error('Invalid table type');
                return;
            }
        })
        .catch(error => {
            console.error("Error fetching sales data:", error);
    });
}

function loadMenu() {
    fetch('/order/menu-items')
        .then(response => response.json())
        .then(menuItems => {
            const menuTableBody = document.querySelector('#menuTable tbody');
            menuTableBody.innerHTML = ''; // Clear existing rows
            const bulkSaveBtnContainer = document.querySelector('.bulk-save-container');
            if (bulkSaveBtnContainer) {
              bulkSaveBtnContainer.innerHTML = '';
            }

            menuItems.forEach(item => {
                const row = document.createElement('tr');
                row.dataset.itemId = item.id; // Store the item ID in the row for easy access

                row.innerHTML = `
<!--                    <td><input type="text" value="${item.id}" class="edit-id" disabled></td>-->
                    <td><input type="text" value="${item.name}" class="edit-name" disabled></td>
                    <td><input type="text" value="${item.description}" class="edit-description" disabled></td>
                    <td><input type="text" value="${item.food_category}" class="edit-category" disabled></td>
                    <td><input type="number" value="${item.price}" class="edit-price" disabled></td>
                    <td>
                        <button class="edit-btn">Edit</button>
                    </td>
                `;
                menuTableBody.appendChild(row);

                const editBtn = row.querySelector('.edit-btn');

                editBtn.addEventListener('click', function() {
                    // Enable the inputs for editing
                    row.querySelectorAll('input').forEach(input => input.disabled = false);

                    // Hide the "Edit" button and show the "Save" button for bulk update
                    editBtn.style.display = 'none';

                    // Enable the bulk save button
                    if (!bulkSaveBtnContainer.querySelector('.save-btn')) {
                        const saveBtn = document.createElement('button');
                        saveBtn.classList.add('save-btn');
                        saveBtn.textContent = 'Save All Changes';
                        saveBtn.addEventListener('click', function() {
                            saveAllChanges(menuItems);
                        });
                        bulkSaveBtnContainer.appendChild(saveBtn);
                    }
                });
            });
        })
        .catch(error => {
            console.error('Error fetching menu items:', error);
        });
}

// Function to save all changes at once
function saveAllChanges(menuItems) {
    const updatedItems = [];

    // Loop through the menu items and collect updated data
    const rows = document.querySelectorAll('#menuTable tbody tr');
    rows.forEach(row => {
        const itemId = row.dataset.itemId;
        const name = row.querySelector('.edit-name').value;
        const description = row.querySelector('.edit-description').value;
        const foodCategory = row.querySelector('.edit-category').value;
        const price = parseInt(row.querySelector('.edit-price').value, 10); // Ensure price is an integer

        // Check if there are any changes
        if (menuItems.some(item => item.id === parseInt(itemId))) {
            updatedItems.push({
                id: itemId,
                name: name,
                description: description,
                food_category: foodCategory,
                price: price
            });
        }
    });

    // Send all updated items in one request
    if (updatedItems.length > 0) {
        fetch('/order/menu-items', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedItems),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Items updated successfully!');
                loadMenu();  // Reload the updated menu after saving
            } else {
                alert('Error updating items.');
            }
        })
        .catch(error => {
            console.error('Error updating menu items:', error);
            alert('Failed to update items.');
        });
    } else {
        alert('No changes detected.');
    }
}


document.addEventListener("DOMContentLoaded", function() {
    loadDailySales();
    loadMenu();
});

document.querySelector('button').addEventListener('click', function() {
    loadCustomSales();
});

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

let currentPage = 1;
let pageSize = window.innerWidth < 768 ? 10 : 25;
let totalPages = 1;

// for vendor management
function loadVendorExpenses(page = 1){
  currentPage = page;
  fetch(`/order/vendor-expenses?page=${currentPage}&page_size=${pageSize}`)
    .then(response => response.json())
    .then(data => {
      totalPages = data.total_pages;
      const tableBody = document.querySelector('#vendorExpenseTable tbody');
      tableBody.innerHTML='';

      let totalVendorExpense=0;
      let totalVendorPaid=0;
      let totalVendorBalance=0;

      const labels = {
          "purchase_pay_cash": "Purchase & Pay Cash",
          "purchase_pay_online": "Purchase & Pay Online",
          "purchase_on_credit": "Purchase on Credit",
          "vendor_payment_cash": "Vendor Payment Cash",
          "vendor_payment_online": "Vendor Payment Online"
      };

      data.data.forEach(expense=>{
        console.log('expense is:: '+expense.vendor)
        console.log('expense is:: '+expense.payment_mode)

        const row=document.createElement('tr');

        row.innerHTML=`<td>${expense.vendor}</td>
                       <td>${expense.material}</td>
                       <td>₹${expense.amount}</td>
                       <td>${expense.payment_mode}</td>
                       <td>${new Date(expense.date).toLocaleString()}</td>`;
        tableBody.appendChild(row);

        // Calculate totals based on type
        switch(expense.payment_mode) {
          case "purchase_pay_cash":
          case "purchase_pay_online":
            totalVendorExpense += expense.amount;
            totalVendorPaid += expense.amount;
            break;

          case "purchase_on_credit":
            totalVendorExpense += expense.amount;
            // Not paid yet, so do not increase totalPaid
            break;

          case "vendor_payment_cash":
          case "vendor_payment_online":
            totalVendorPaid += expense.amount;
            break;
        }
      });
      totalVendorBalance = totalVendorExpense - totalVendorPaid;
      document.getElementById('vendor-expense-total').textContent = `₹${totalVendorExpense.toFixed(2)}`;
      document.getElementById('vendor-expense-paid').textContent = `₹${totalVendorPaid.toFixed(2)}`;
      document.getElementById('vendor-expense-balance').textContent=`₹${totalVendorBalance.toFixed(2)}`;

      // Update pagination display
      document.getElementById("pageNumber").innerText = `Page ${data.page} of ${data.total_pages}`;
      document.getElementById("prevBtn").disabled = data.page === 1;
      document.getElementById("nextBtn").disabled = data.page === data.total_pages;
    })
    .catch(error=>{
      console.error("Error loading vendor expenses:",error);
    });
  }
function openVendorExpenseModal(){
  document.getElementById("vendorExpenseModal").style.display="block";
}

function closeVendorExpenseModal(){
  document.getElementById("vendorExpenseModal").style.display="none";
}

function addVendorExpense(){
  console.log('hi 1')

  const vendor=document.getElementById('vendorName').value;
  const material=document.getElementById('materialName').value;
  const amount=Number(document.getElementById('expenseAmount').value);
  const paymentMode=document.getElementById('expensePaymentMode').value;
  const expenseDate=document.getElementById("expenseDate").value;

  if(!vendor || !material || !amount){
    alert("Please fill all fields");
    return;
  }

fetch('/order/vendor-expenses',{

  method:'POST',

  headers:{
  'Content-Type':'application/json'
  },

  body:JSON.stringify({
    vendor:vendor,
    material:material,
    amount:amount,
    payment_mode:paymentMode,
    date:expenseDate
  })

})
.then(res=>res.json())
.then(data=>{

    alert("Expense Added Successfully"+expenseDate);
    closeVendorExpenseModal();

    document.getElementById('vendorName').value='';
    document.getElementById('materialName').value='';
    document.getElementById('expenseAmount').value='';
    document.getElementById('expensePaymentMode').value='';
    document.getElementById('expenseDate').value='';
    loadVendorExpenses();
  })
  .catch(error=>{
    console.error("Error adding expense:", error);
    alert("Failed to add expense"+ error.message);
    });
}

document.addEventListener("DOMContentLoaded", function() {
  loadDailySales();
  loadMenu();
  loadVendorExpenses(1);
});

function nextPage(){
  if(currentPage < totalPages){
    currentPage++;
    loadVendorExpenses(currentPage);
  }
}

function prevPage(){
  if(currentPage > 1){
    currentPage--;
    loadVendorExpenses(currentPage);
  }
}
