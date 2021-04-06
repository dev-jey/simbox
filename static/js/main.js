$(document).ready(function () {

    $("#global-search").click(function() {
        $(".ui-autocomplete").show();
    });

    $("#global-search").autocomplete({

        create: function(event, ui) {
            $(this).data('ui-autocomplete')._renderItem = function(ul, item) {

                //Convert categories into a string
                simulators = ''
                item.simulators.forEach(function(cat) { 
                    simulators += cat + " • "
                })

                return $('<li class="list-group-item border-0">')
                    .attr("data-value", item.value)
                    .append("<a href='/mod/" + item.id + "' class='text-white font-weight-bold'>" + item.value 
                        + "<b class='text-info'> – " + item.type + "</b>" 
                        + "<br/><small class='text-light'>" + simulators + "</small></a>"
                    )         
                    .appendTo(ul)
            };
        },

        source: function(request, response) {
            $.ajax({
                url: $("#global-search").data("url"),
                type: "get",
                dataType: "json",
                data: {
                    search: request.term,
                },
                success: function(data) {
                    response($.map(data, function (item) {
                        return {
                            id: item.id,
                            label: item.title,
                            value: item.title,
                            type: item.type,
                            simulators: item.simulators
                        };
                    }));
                },
            });
        },

    });

    /* MODAL */
    $('*[data-toggle="modal"]').click(function(){
        var target = $(this).data("target");
        $(target).toggleClass('hidden flex');
    });

    $('#modal-close').click(function(){
        $(this).parents().eq(1).toggleClass('flex hidden')  
    });


    /* DROPDOWN MENU */
    $('*[data-toggle="dropdown"]').click(function(){
        var target = $(this).data("target");
        $(target).toggleClass('hidden visible')
    });
});

$(document).on('click', function(event){
    var $trigger = $('*[data-toggle="dropdown"]');
    if($trigger !== event.target && !$trigger.has(event.target).length){
        $('#profile-menu').removeClass('visible').addClass('hidden')
    }
});