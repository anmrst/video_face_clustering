$(document).ready(function() {
    $('#upload-form').submit(function(event) {
        event.preventDefault(); // Prevent default form submission

        var formData = new FormData(this);

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Handle the successful response without page reload
                alert(response); // You can replace this with your own logic
            },
            error: function(xhr, status, error) {
                // Handle error
                console.error(error);
            }
        });
    });
});