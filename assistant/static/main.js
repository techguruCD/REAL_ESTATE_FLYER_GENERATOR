$( document ).ready(function() {
    $('.thumb-preview').click(function() {
        $('.thumb_input').click()
    })
    $('.thumb_input').change(function() {
        let headers = {
            Authorization: 'Bearer 213e102e799007ded0c959b01965235101ae3fa1',
            'Content-Type': 'multipart/form-data',
            'Accept': '*/*',
        }
        let data = new FormData($('.upload-form').get(0))
        let mediaurl = base_url + 'media/'
        $('.spinner').show()
        axios({
            method: 'post',
            url: 'https://api.imgur.com/3/upload',
            headers,
            data
        }).then(({data: {data: {link}}}) => {
            console.log(link)
            $('.thumb-preview').attr('src', link)
            $('.thumb_url').val(link)
        }).catch(err => {

        }).finally(() => {
            $('.spinner').hide()
        })
        // $.ajax({
        //     url:$('.upload-form').attr('action'),
        //     type:$('.upload-form').attr('method'),
        //     data: data,
        //     cache: false,
        //     processData: false,
        //     contentType: false,
        //     success: function(data) {
        //         let link = mediaurl + data.thumb_url
        //         $('.thumb-preview').attr('src', link)
        //         $('.thumb_url').val(link)
        //     }
        // })
    })
});