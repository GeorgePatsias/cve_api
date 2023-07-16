$(document).ready(function () {
    $('#tbl-cves').DataTable({
        responsive: true,
        lengthMenu: [
            [10, 15, 25, 50, -1],
            [10, 15, 25, 50, "All"]
        ],
        dom: 'Blfrtip',
        buttons: {
            buttons: [
                { extend: 'copy', className: 'btn-primary rounded' },
                { extend: 'csv', className: 'btn-primary rounded' },
                { extend: 'excel', className: 'btn-primary rounded' }
            ]
        },
        displayLength: 15,
        ajax: {
            url: "/events/datatable",
            type: "GET",
        },
        order: [[1, 'desc']],
        columns: [{
            defaultContent: "-",
            data: "cve",
            // className: 'text-center'
        }, {
            defaultContent: "-",
            data: "keyword",
            // className: 'text-center'
        }],
        columnDefs: [{
            targets: [0],
            render: function (data, type, row) {
                return "<a href='/investigate/" + data + "' target='_blank'> " + data + "</a>";
            }
        }],
    });




});