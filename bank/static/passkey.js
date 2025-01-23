document.getElementById('register-passkey-btn').addEventListener('click', async () => {
    const response = await fetch('/register-passkey/', { method: 'POST' });
    const options = await response.json();

    const credential = await navigator.credentials.create({ publicKey: options });
    const result = await fetch('/verify-registration/', {
        method: 'POST',
        body: JSON.stringify(credential),
        headers: { 'Content-Type': 'application/json' },
    });

    if (result.ok) {
        alert('Passkey registered successfully!');
    } else {
        alert('Registration failed.');
    }
});

document.getElementById('login-passkey-btn').addEventListener('click', async () => {
    const response = await fetch('/authenticate-passkey/', { method: 'POST' });
    const options = await response.json();

    const assertion = await navigator.credentials.get({ publicKey: options });
    const result = await fetch('/verify-authentication/', {
        method: 'POST',
        body: JSON.stringify(assertion),
        headers: { 'Content-Type': 'application/json' },
    });

    if (result.ok) {
        alert('Logged in successfully!');
    } else {
        alert('Authentication failed.');
    }
});
