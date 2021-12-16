// script to create dinamic jsGrid table 

$(document).ready(function() {
    $("#jsGrid").jsGrid({
        height: "auto",
        width: "100%",

        filtering: true,
        inserting: false,
        editing: false,
        sorting: true,
        paging: false,
        autoload: true,
        heading: false, //'true' show heading of the table

        pageSize: 10,
        pageButtonCount: 3,

        deleteConfirm: "Do you want to delete data?",

        noDataContent: "No data in db.",

        controller: {
            
            loadData: function(filter) {
                var d = $.Deferred();
                $.ajax({
                    type: "GET",
                    url: "/abc_api",
                    data: filter
                }).done(function(result) {
                    d.resolve($.map(result, function(item) {
                        return $.extend(item.fields, { 
                                                        N: item.id,
                                                        Name: item.Name, 
                                                        Sales: item.Sales, 
                                                        Sum: item.Sum,
                                                        Class: item.Class,
                                                    });
                    }));
                });

                return d.promise();
            },
        },

        fields: [
            { name: "Name", type: "text", width: 100 },
            { name: "Sales", type: "number", width: 40, filtering: false, align: "left" },
            { name: "Sum", type: "number", width: 40, filtering: false, align: "left" },
            { name: "Class", type: "text", width: 100}
        ]
    });

});