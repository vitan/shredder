shredder.ajax = {

    statusCode: {
        success: 0
    },

    isSuccessful: function(rc) {
        return (rc == this.statusCode.success)
    },

    post: function(url, data, callback) {
        $.ajax({
            url: url,
            type: 'POST',
            dataType: 'json',
            data: data,
            success: callback
        });
    },

    get: function(url, data, callback) {
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            data: data,
            success: callback
        });
    },
}
