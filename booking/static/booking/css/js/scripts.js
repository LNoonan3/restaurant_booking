document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('reservation-form');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const csrfToken = formData.get('csrfmiddlewaretoken');

        fetch('/book-table/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                messageDiv.innerHTML = '<p>Reservation successful!</p>';
                form.reset();
            } else {
                messageDiv.innerHTML = '<p>Reservation failed: ' + data.error + '</p>';
            }
        })
        .catch(error => {
            messageDiv.innerHTML = '<p>An error occurred: ' + error.message + '</p>';
        });
    });
});