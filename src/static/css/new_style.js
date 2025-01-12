/* General Styles */
body {
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f6f9;
    color: #333;
    box-sizing: border-box;
}

/* Container (Sidebar and Content) */
.container {
    display: flex;
    min-height: 100vh;
    transition: margin-left 0.3s ease;
}

/* Sidebar Styles */
.sidebar {
    width: 250px;
    background-color: #2C3E50;
    color: white;
    padding: 20px;
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 100;
    box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1);
}

.sidebar h2 {
    text-align: center;
    margin-bottom: 40px;
    font-size: 24px;
    font-weight: 600;
    color: #ecf0f1;
}

.nav {
    list-style: none;
    padding: 0;
}

.nav li {
    margin: 15px 0;
}

.nav li a {
    color: white;
    text-decoration: none;
    font-size: 16px;
    display: block;
    padding: 12px 20px;
    border-radius: 4px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.nav li a:hover {
    background-color: #34495E;
    transform: translateX(5px);
}

/* Active Link */
.nav li a.active {
    background-color: #1ABC9C;
    font-weight: bold;
}

/* Content Area Styles */
.content {
    flex: 1;
    padding: 30px;
    margin-left: 270px; /* Add margin to make space for the sidebar */
    transition: margin-left 0.3s ease;
}

h2 {
    font-size: 28px;
    font-weight: 600;
    color: #2C3E50;
    margin-bottom: 20px;
}

/* Sales Summary Box Styles */
.sales-summary {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px;
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.sales-summary > div {
    flex: 1;
    padding: 15px;
    margin: 0 10px;
    background-color: #ecf0f1;
    border-radius: 8px;
    text-align: left;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.sales-summary h3 {
    font-size: 18px;
    font-weight: 600;
    color: #34495E;
    margin-bottom: 10px;
}

.sales-summary p {
    font-size: 20px;
    font-weight: 700;
    color: #27ae60;
    text-align: right;
}

/* Button Styles */
button {
    padding: 12px 20px;
    background-color: #1ABC9C;
    color: white;
    border: none;
    cursor: pointer;
    margin-bottom: 20px;
    font-size: 16px;
    border-radius: 8px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover {
    background-color: #16a085;
    transform: translateY(-3px);
}

/* Table Styles */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 30px;
    border-radius: 8px;
    overflow: hidden;
    background-color: #ffffff;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

table, th, td {
    border: 1px solid #ddd;
}

th, td {
    padding: 15px;
    text-align: left;
    font-size: 14px;
}

th {
    background-color: #f4f6f9;
    font-weight: bold;
}

td {
    color: #555;
}

#dailySalesTable tbody tr:nth-child(even) {
    background-color: #f9f9f9;
}

#dailySalesTable tbody tr:hover {
    background-color: #ecf0f1;
    cursor: pointer;
}

/* Currency Symbol Styling */
strong {
    font-size: 1.2em;
    color: #333;
}

/* Responsive Design */
@media (max-width: 1200px) {
    .container {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        height: auto;
    }

    .content {
        margin-left: 0;
    }

    .sales-summary {
        flex-direction: column;
        align-items: flex-start;
    }

    .sales-summary > div {
        margin-bottom: 20px;
    }

    .nav li a {
        font-size: 14px;
        padding: 10px;
    }
}

/* Tablet (portrait) */
@media (max-width: 1024px) {
    .container {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        position: relative;
        height: auto;
    }

    .content {
        margin-left: 0;
    }

    .sales-summary {
        flex-direction: column;
        margin-bottom: 20px;
    }

    .sales-summary > div {
        width: 100%;
        margin-bottom: 10px;
    }

    button {
        width: 100%;
        padding: 15px;
    }
}

/* Mobile (portrait) */
@media (max-width: 768px) {
    .container {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        position: relative;
        height: auto;
    }

    .content {
        margin-left: 0;
    }

    .sales-summary {
        flex-direction: column;
        align-items: flex-start;
    }

    .sales-summary > div {
        width: 100%;
        margin-bottom: 20px;
    }

    .nav li a {
        font-size: 14px;
        padding: 10px;
    }

    table, th, td {
        font-size: 12px;
    }

    button {
        width: 100%;
        padding: 12px;
    }

    .sales-summary h3 {
        font-size: 16px;
    }

    .sales-summary p {
        font-size: 18px;
    }
}
