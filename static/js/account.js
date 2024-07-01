document.getElementById('edit-button').addEventListener('click', function() {
    document.getElementById('input-id').removeAttribute('disabled');
    document.getElementById('input-password').removeAttribute('disabled');
    document.getElementById('edit-button').style.display = 'none';
    document.getElementById('save-button').style.display = 'inline-block';
});

document.getElementById('save-button').addEventListener('click', function() {
    // Implement saving logic here if needed
    document.getElementById('input-id').setAttribute('disabled', true);
    document.getElementById('input-password').setAttribute('disabled', true);
    document.getElementById('edit-button').style.display = 'inline-block';
    document.getElementById('save-button').style.display = 'none';
});