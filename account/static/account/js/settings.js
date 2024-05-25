document.addEventListener('DOMContentLoaded', function() {
    var vidStrideInput = document.getElementById('vid_stride');
    var confidenceInput = document.getElementById('confidence');
    var saveBtn = document.getElementById('save-btn');
    function checkInputs() {
        if (vidStrideInput.value.trim() !== '' && confidenceInput.value.trim() !== '') {
            saveBtn.disabled = false;
        } else {
            saveBtn.disabled = true;
        }
    }
    vidStrideInput.addEventListener('input', checkInputs);
    confidenceInput.addEventListener('input', checkInputs);
    document.getElementById('settings-form').addEventListener('submit', function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        if (this.checkValidity() === false) {
            event.stopPropagation();
        } else {
            fetch(settingsUrl, {
                method: 'POST',
                body: formData, 
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Settings updated successfully:', data);
                document.getElementById('success-alert').style.display = 'block';
                setTimeout(function() {
                    window.location.href = uploadUrl;
                }, 1000);
            })
            .catch(error => {
                console.error('Error updating settings:', error);
                alert('Ayarlar güncellenirken bir hata oluştu.');
            });
        }
        this.classList.add('was-validated'); 
    });
    checkInputs();
});