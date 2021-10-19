$(document).ready(function() {
    $("#listView").kendoListView({
          template: "<li>${FirstName} ${LastName}</li>",
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
    $("#scheduler").kendoScheduler({
        date: new Date(Date.now()),
        startTime: new Date(Date.now()),
        height: 600,
        views: [
            { type: "agenda", selected: true, eventHeight: 100},
        ],
        timezone: "Etc/UTC",
        dataSource: {
            batch: true,
            transport: {
                read: {
                    url: "/Events/ViewAll/",
                    dataType: "json",
                    type: "GET"
                },
                update: {
                    url: "/Events/Edit/",
                    dataType: "json",
                    type: "POST"
                },
                create: {
                    url: "/Events/Create/",
                    dataType: "json",
                    type: "POST"
                    },
                destroy: {
                    url: "/Events/Delete",
                    dataType: "json",
                    type: "POST"
                },
            },
            schema: {
                model: {
                    id: "id",
                    fields: {
                        id: { from: "id", type: "number" },
                        title: { from: "name", type: "string" },
                        start: { type: "date", from: "start" },
                        end: { type: "date", from: "end" },
                        description: { from: "description" }
                    }
                }
            },
        },
    });
});