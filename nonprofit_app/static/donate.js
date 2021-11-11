function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
            }
        }
    }
    return cookieValue;
}

var event_id = 0;

function unrestricted_donation() {
    $("#unrestricted_window").show().kendoWindow({
        content: {
            url: 'donate_unrestricted'
        },
        width: 250,
        height: 300,
    });
};

function restricted_donation(data_id) {
    $("#restricted_window").show().kendoWindow({
        title: 'Event ' + event_id + ': ' + data_id,
        content: {
            url: 'donate_restricted/'+event_id
        },
        width: 450,
        height: 320,
    });
}

$(document).ready(function() {
    const csrftoken = getCookie('csrftoken');
    $('#ud').kendoButton({
        click: function(e) {
            e.preventDefault();
            unrestricted_donation();
        }
    });
    $("#donation_grid").kendoGrid({
        dataSource: {
            transport: {
                type: "GET",
                read: {
                    url: "/Donate/GetAllEvents/",
                    dataType: "json",
                },
                pageSize: 20
            },},
            height: 400,
            groupable: false,
            sortable: true,
            pageable: {
                refresh: true,
                pageSizes: true
            },
            columns: [
                {field: 'start', title: 'Date', type: 'date', width: "12%", template: '#= kendo.toString(start,"MM/dd/yyyy") #'},
                {field: 'start', title: 'Start Time', type: 'date', width: "12%",template: '#= kendo.toString(start,"h:mm tt") #'},
                {field: 'end', title: 'End Time', type: 'date', width: "12%", template: '#= kendo.toString(end, "h:mm tt") #'},
                {field: 'name', title: 'Event', type: 'string', width: "20%"},
                {field: 'description', title: 'Description', type: 'string', width: "10%"},
                {field: 'location', title: 'Location', type: 'string', width: "12%"},
                { command: [{
                        name: "donate",

                        click: function(e) {
                            e.preventDefault();
                            var dataItem = this.dataItem($(e.currentTarget).closest("tr"));
                            event_id = dataItem.id
                            restricted_donation(dataItem.name);

                            // console.log(dataItem);
                            // $.ajax({
                            //     type: "POST",
                            //     url: "/Donate/EventDonation/",
                            //     headers: {'X-CSRFToken': csrftoken},
                            //     data: {'id': dataItem.id},
                            //     contentType: "application/x-www-form-urlencoded",
                            //     success: function(response) {
                            //         console.log(response)
                            //         if(response == '{"success": "false"}'){
                            //             alert("Sorry, you aren't signed up to volunteer for this event because there are already enough volunteers for this event.")
                            //         }
                            //         else{
                            //             $('#donation_grid').data('kendoGrid').dataSource.read();
                            //         }
                            //     }
                            // });
                        }

                    }],
                    title: "Donate", width: "12%"
                }
            ],
    });

});
