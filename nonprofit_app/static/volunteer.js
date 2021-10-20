$(document).ready(function() {
    $("#listView").kendoListView({
          dataSource: {
              transport: {
                    read: {
                        url: "/Volunteer/GetEvents/",
                        dataType: "json",
                        type: "GET"
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
                {field: 'name', title: 'Event', type: 'string'},
                {field: 'start', title: 'Date', type: 'date', template: '#= kendo.toString(start,"MM/dd/yyyy") #'},
                {field: 'end', title: 'End Date', type: 'date', template: '#= kendo.toString(end,"MM/dd/yyyy") #'},
                {field: 'location', title: 'Location', type: 'string'},
                {field: 'description', title: 'Description', type: 'string'},
                {field: 'volunteers_needed', title: 'Number of Volunteers Needed', type: 'string'},
            ],
    });
});