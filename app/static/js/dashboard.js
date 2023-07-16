
$(document).ready(function () {

    $('#tbl-cves').DataTable({
        responsive: true,
        lengthMenu: [
            [10, 25, 50, -1],
            [10, 25, 50, "All"]
        ],
        dom: 'tip',
        displayLength: 10,
        ajax: {
            url: "/dashboard/datatable",
            type: "GET",
        },
        columns: [{
            defaultContent: "PENDING",
            data: "severity",
            className: "text-nowrap"

        }, {
            defaultContent: "-",
            data: "cve",
            className: "text-nowrap"

        }, {
            defaultContent: "-",
            data: "description",
            className: "dt-body-justify"
        }],
        columnDefs: [{
            targets: [0],
            render: function (data, type, row) {
                if (data == "CRITICAL") {
                    return "<span class='text-danger fw-bold bg-dark'>CRITICAL</span>";
                } else if (data == "HIGH") {
                    return "<span class='text-danger fw-bold'>HIGH</span>";
                } else if (data == "MEDIUM") {
                    return "<span class='text-warning fw-bold'>MEDIUM</span>";
                } else if (data == "LOW") {
                    return "<span class='text-primary fw-bold'>LOW</span>";
                } else if (data == "PENDING") {
                    return "<span class='text-muted fw-bold'>PENDING</span>";
                }
                return data;
            }
        }, {
            targets: [1],
            render: function (data, type, row) {
                return '<a href="/investigate/' + data + '" target="_blank">' + data + '</a>';
            }
        }, {
            targets: [2],
            render: function (data, type, row) {
                return data.substr(0, 120) + ' ... <a href="/investigate/' + row.cve + '" target="_blank"><i class="fa-solid fa-arrow-up-right-from-square"></i></a>'
            }
        },],
    });











    $.ajax({
        url: "/dashboard/trending-posts",
        success: function (results) {
            const data = JSON.parse(results)

            var xValues = [];
            var yValues = [];

            data.forEach((item) => {
                xValues.push(item.cve);
                yValues.push(item.audience_size);
            });


            var bar_ctx = document.getElementById('audienceChart').getContext('2d');
            var gradient_color = bar_ctx.createLinearGradient(0, 0, 0, 700);
            gradient_color.addColorStop(0, 'DeepSkyBlue');
            gradient_color.addColorStop(1, 'Black');

            new Chart(bar_ctx, {
                type: "bar",
                data: {
                    labels: xValues,
                    datasets: [{
                        backgroundColor: gradient_color,
                        hoverBorderWidth: 2,
                        hoverBorderColor: 'red',
                        hoverBackgroundColor: gradient_color,
                        data: yValues
                    }]
                },
                options: {
                    responsive: true,
                    animation: true,
                    legend: { display: false },
                    plugins: {
                        legend: {
                            display: false,
                        }
                    }
                },

            });
        }
    });























});