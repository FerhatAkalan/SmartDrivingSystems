// Dosya türünü kontrol et
function checkFileType(input) {
    var file = input.files[0];
    var fileType = file.type;
    var allowedTypes = ['image/jpeg', 'video/mp4'];
    if (!allowedTypes.includes(fileType)) {
        // Dosya türü desteklenmiyorsa uygun hata mesajını göster
        var errorId = input.id === 'fileInputInside' ? '#fileTypeErrorInside' : '#fileTypeErrorOutside';
        $(errorId).show();
        input.value = ''; // Dosyayı temizle
    } else {
        // Dosya türü destekleniyorsa hata mesajını gizle
        var errorId = input.id === 'fileInputInside' ? '#fileTypeErrorInside' : '#fileTypeErrorOutside';
        $(errorId).hide();
    }
}

// Dosya yükleme işlemi sırasında spinner'ı ve loading metnini göster
$(document).ready(function() {
    $('#uploadForm').submit(function(event) {
        event.preventDefault(); // Formun gönderilmesini engelle
        if (this.checkValidity() === false) {
            event.stopPropagation(); // Olayın üst sınıfa yayılmasını engelle
        } else {
            $('#spinner').show();
            $('#uploadButtonContainer').hide();
            this.submit(); // Formu gönder
        }
        this.classList.add('was-validated'); // Bootstrap'den gelen stilleri uygula
    });
});