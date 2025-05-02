document.getElementById('expense-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const data = {
        category: document.getElementById('category').value,
        description: document.getElementById('description').value,
        amount: document.getElementById('amount').value,
        date: document.getElementById('date').value
    };

    fetch('/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(res => res.json())
        .then(() => {
            document.getElementById('expense-form').reset();
            loadExpenses();
        });
});

function loadExpenses() {
    fetch('/expenses')
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById('expense-table');
            const totalField = document.getElementById('total');
            table.innerHTML = '<tr><th>Category</th><th>Description</th><th>Amount (₹)</th><th>Date</th></tr>';

            let total = 0;
            data.forEach(item => {
                const row = table.insertRow();
                row.innerHTML = `<td>${item[0]}</td><td>${item[1]}</td><td>₹${item[2]}</td><td>${item[3]}</td>`;
                total += parseFloat(item[2]);
            });
            totalField.textContent = total.toFixed(2);
        });
}

loadExpenses();
