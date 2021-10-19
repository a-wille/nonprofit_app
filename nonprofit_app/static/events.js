

$(document).ready(function() {
        $("#scheduler").kendoScheduler({
        date: new Date(Date.now()),
        startTime: new Date(Date.now()),
        height: 600,
        views: [
            "week",
            "month",
            "year",
            { type: "agenda", selected: true, eventHeight: 100},
            { type: "timeline", eventHeight: 50}
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