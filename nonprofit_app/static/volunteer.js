$(document).ready(function() {
    $("#listView").kendoListView({
        template: "<li>${data}</li>",
        dataSource: {
              transport: {
                    type: "GET",
                    read: {
                        url: "/Volunteer/GetEvents/",
                        dataType: "json",
                    }
              },
          }
      });
    $("#grid").kendoGrid({
        dataSource: {
            transport: {
                type: "GET",
                read: {
                    url: "/Volunteer/GetAllEvents/",
                    dataType: "json",
                },
                pageSize: 20
            },},
            height: 600,
            groupable: true,
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
                {field: 'volunteers_needed', title: '# Volunteers Needed', width: "12%", type: 'string'},
                {field: 'volunteers', hidden: "true"},
                { command: [{
                        name: "signup",

                        click: function(e) {
                            e.preventDefault();
                            var dataItem = this.dataItem($(e.currentTarget).closest("tr"));
                            console.log(dataItem);
                            $.ajax({
                                type: "POST",
                                url: "/Volunteer/SignUp/",
                                headers: {'X-CSRFToken': csrftoken},
                                data: {'id': dataItem.id},
                                contentType: "application/x-www-form-urlencoded",
                                success: function(response) {
                                    if(response['success'] == 'true'){
                                        location.reload();
                                    }
                                    else{
                                        alert("Sorry, you aren't signed up to volunteer for this event because there are already enough volunteers for this event.")
                                    }
                                }
                            });
                        }

                    }],
                    title: "Sign Up", width: "12%"
                }
            ],
    });
});