$(document).ready(function () {

    $('#tbl-monitoring').DataTable({
        responsive: true,
        lengthMenu: [
            [10, 25, 50, -1],
            [10, 25, 50, "All"]
        ],
        dom: 'lfrtip',
        order: [[2, 'desc']],
        displayLength: 25,
        ajax: {
            url: "/monitoring/datatable",
            type: "GET",
        },
        columns: [{
            defaultContent: "-",
            data: "monitoring_keyword",
        }, {
            defaultContent: "-",
            data: "frequency",
        }, {
            defaultContent: "-",
            data: "created_at",
        }, {
            defaultContent: "-",
            data: "edited_at",
        }, {
            defaultContent: "-",
            data: "updated_at",
        }, {
            data: "actions",
            className: 'text-center'
        }],
        columnDefs: [{
            targets: [5],
            data: null,
            defaultContent: "<button type='button' class='btn btn-danger btn-sm'><i class='fa-solid fa-trash-can'></i></button>"
        }],
    });


    $('#tbl-monitoring tbody').on('click', 'button', function () {
        var tr = $(this).closest('tr');
        var row_data = $('#tbl-monitoring').DataTable().row(tr).data();

        $.ajax({
            url: "/monitoring/delete",
            data: {"keyword": row_data.monitoring_keyword},
            success: function () {
                location.reload();
            }
        });
    });






    $(function () {
        $('input')
            .on('change', function (event) {
                var $element = $(event.target);
                var $container = $element.closest('.example');

                if (!$element.data('tagsinput')) return;

                var val = $element.val();
                if (val === null) val = 'null';
                var items = $element.tagsinput('items');

                $('code', $('pre.val', $container)).html(
                    $.isArray(val)
                        ? JSON.stringify(val)
                        : '"' + val.replace('"', '\\"') + '"'
                );
                $('code', $('pre.items', $container)).html(
                    JSON.stringify($element.tagsinput('items'))
                );
            })
            .trigger('change');
    });



});