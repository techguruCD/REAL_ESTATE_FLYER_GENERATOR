$( document ).ready(function() {
    $('.thumb-preview').click(function() {
        $('.thumb_input').click()
    })
    $('.thumb_input').change(function() {
        let data = new FormData($('.upload-form').get(0))
        let mediaurl = base_url + 'media/'
        $.ajax({
            url:$('.upload-form').attr('action'),
            type:$('.upload-form').attr('method'),
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(data) {
                let link = mediaurl + data.thumb_url
                $('.thumb-preview').attr('src', link)
                $('.thumb_url').val(link)
            }
        })
    })
});