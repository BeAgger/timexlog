$(document).ready(function() {

    $('.updateButton').on('click', function() {

        let timelog_id = $(this).attr('timelog_id');
        let customer = $('#customer'+timelog_id).val();
        let project = $('#project'+timelog_id).val();
        let task = $('#task'+timelog_id).val();
        // let start = $('#start'+timelog_id).val();
        let comment = $('#comment'+timelog_id).val();
        

        console.log(timelog_id +', '+ customer +', '+  project +', '+  
            task +', '+ comment
        );// +', '+  start);

        $.ajax({
            url : '/timelog/update',
            type : 'POST',
            data : { 
                customer : customer, 
                project : project, 
                task : task, 
                //start : start, 
                comment:comment,
                id : timelog_id 
            },
            success: function(response) {
                console.log(response);
            }
        })

        .done(function(data) {

            $('#timelogRow'+timelog_id).fadeOut(1000).fadeIn(1000);

        });
    

    });

});