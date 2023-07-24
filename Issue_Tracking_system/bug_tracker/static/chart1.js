function drawChart() {
  google.charts.load("current", { packages: ["corechart"] });
  google.charts.setOnLoadCallback(fetchChartData);

  function fetchChartData() {
    fetch("/chart_data/")
      .then((response) => response.json())
      .then((data) => {
        var chartData = [["Ticket Type", "Number of Tickets"]];
        data.forEach((item) => {
          chartData.push([item.ticket_type, item.ticket_count]);
        });
        var dataTable = google.visualization.arrayToDataTable(chartData);
        var options = {
          width: "100%",
          height: "100%",
        };
        var chart = new google.visualization.PieChart(
          document.getElementById("chart1")
        );
        chart.draw(dataTable, options);
      });
  }
}

drawChart();
