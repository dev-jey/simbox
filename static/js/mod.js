$(document).ready(function () {

    $("#like_button").click(function () {
        var serializedData = $("#mod-actions").serialize();

        $.ajax({
            url: $("#mod-actions").data('url'),
            data: serializedData + "&action=like",
            type: 'post',
            success: function (response) {
                console.log(response)
                if ($("#like_button").data('action') == 'like') {
                    $("#like_button").removeClass().addClass('btn-remove-like').data('action', 'remove-like')
                    $("#messages").addClass('alert-success').toggleClass('hide show').append(response.message).delay(8000).queue(function () {
                        $(this).toggleClass('show hide').empty()
                    });
                } else {
                    $("#like_button").removeClass().addClass('btn-like').data('action', 'like')
                    $("#messages").addClass('alert-success').toggleClass('hide show').append(response.message).delay(8000).queue(function () {
                        $(this).toggleClass('show hide').empty()
                    });
                }
            }
        })
    });


    $("#create-list-btn").click(function () {
        $("#new-list-name").toggleClass('hidden')
        $("#save-new-list").toggleClass('hidden')
    });

    $("#save-new-list").click(function () {
        var serializedData = $("#create-list").serialize();

        $.ajax({
            url: $("create-list").data('url'),
            data: serializedData + "&action=create-list",
            type: 'post',
            success: function (response) {
                $("#id_list_name").append($('<option></option>').val(response.list_id).text(response.list_name));
                $("#new-list-name").toggleClass('visible invisible')
                $("#save-new-list").toggleClass('visible invisible')
            },
        })
    });


    $("#save-to-list").click(function () {
        list_id = $("#id_list_name option:selected").attr("value");
        var serializedData = $("#add-to-list").serialize();

        $.ajax({
            url: $("#add-to-list").data('url'),
            data: serializedData + "&action=add-to-list",
            type: 'post',
            success: function (response) {
                $("#list-modal").modal('toggle')
                $("#messages").addClass('alert-success').toggleClass('hide show').append(response.message).delay(8000).queue(function () {
                    $(this).toggleClass('show hide').empty()
                });
            },
        })
    });

    $("#toggle-comment-form").click(function () {
        $("#comment-form").fadeToggle(200).toggleClass('hidden ')
    });

    $("#save-comment").click(function () {
        var serializedData = $("#comment-form").serialize();

        $.ajax({
            url: $("#save-comment").data('url'),
            data: serializedData + "&action=save-comment",
            type: 'post',
            success: function (response) {
                $("#messages").addClass('alert-success').toggleClass('hide show').append(response.message).delay(8000).queue(function () {
                    $(this).toggleClass('show hide').empty()
                });

                location.reload()
                
                setTimeout(function(){
                    $('html, body').animate({
                        scrollTop: $(document).height()
                    }, slow)
                });
            },
        })
    });

    $("#download").click(function () {
        var serializedData = $("#download-form").serialize();

        $.ajax({
            url: $("#download-form").data('url'),
            data: serializedData + "&action=download",
            type: 'post',
            success: function (response) {
            
            },
        })
    });


    $("[id^=delete-comment-btn-]").click(function () {
        comment = $(this).attr("id").split("-")[3];
        var serializedData = $("#delete-comment-form-" + comment).serialize();

        $.ajax({
            url: $("delete-comment-form").data('url'),
            data: serializedData + "&comment=" + comment + "&action=delete-comment",
            type: 'post',
            success: function (response) {
                $("#messages").addClass('alert-warning').toggleClass('hide show').append(response.message).delay(8000).queue(function () {
                    $(this).toggleClass('show hide').empty()
                });

                location.reload()
            },
        })
    });

});