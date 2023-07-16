$(document).ready(function () {

    if ($("#top-search").val() == "") {
        $(".card-body").hide();
    }




    $.ajax({
        url: "/investigate/twitter-traffic",
        data: { "cveId": $("#top-search").val() },
        success: function (results) {
            const data = JSON.parse(results)

            var xValues = [];
            var yValues = [];

            data.forEach((item) => {
                xValues.push(item.timestamp_start);
                yValues.push(item.audience);
            });

            new Chart("twitterAreaChart", {
                type: "line",
                data: {
                    labels: xValues,
                    datasets: [{
                        data: yValues,
                        label: "Audience",
                        lineTension: 0.3,
                        backgroundColor: "rgba(2,117,216,0.2)",
                        borderColor: "rgba(2,117,216,1)",
                        pointRadius: 5,
                        pointBackgroundColor: "rgba(2,117,216,1)",
                        pointBorderColor: "rgba(255,255,255,0.8)",
                        pointHoverRadius: 5,
                        pointHoverBackgroundColor: "rgba(2,117,216,1)",
                        pointHitRadius: 50,
                        pointBorderWidth: 2,
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