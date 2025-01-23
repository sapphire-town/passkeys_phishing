// scripts.js

function applyLoan() {
    const loanType = document.getElementById('loan-type').value;
    alert(`Loan application for ${loanType} submitted!`);
}

function createAccount() {
    alert('Account creation process initiated!');
}

function sendMoney() {
    const recipient = document.getElementById('recipient').value;
    const amount = document.getElementById('amount').value;
    if (recipient && amount > 0) {
        alert(`Sent $${amount} to ${recipient}.`);
    } else {
        alert('Please enter valid recipient and amount.');
    }
}

function viewTransactions() {
    const transactionsDiv = document.getElementById('transactions');
    transactionsDiv.innerHTML = `
        <ul>
            <li>Sent $200 to Alice on 2024-12-10</li>
            <li>Received $500 from Bob on 2024-12-12</li>
            <li>Paid $300 for rent on 2024-12-15</li>
        </ul>
    `;
    transactionsDiv.style.display = 'block';
}

function viewBalance() {
    const balanceDisplay = document.getElementById('balance-display');
    balanceDisplay.textContent = 'Your current balance is $1,200.';
}
