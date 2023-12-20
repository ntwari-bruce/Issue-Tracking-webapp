function drawChart() {
  google.charts.load("current", { packages: ["corechart"] });
  google.charts.setOnLoadCallback(fetchChartData);

  function fetchChartData() {
    fetch("/chart_data2/")
      .then((response) => response.json())
      .then((data) => {
        var chartData = [["Ticket Priority", "Number of Tickets"]];
        data.forEach((item) => {
          chartData.push([item.priority, item.ticket_count]);
        });
        var dataTable = google.visualization.arrayToDataTable(chartData);
        var options = {
          width: "100%",
          height: "100%",
        };
        var chart = new google.visualization.PieChart(
          document.getElementById("chart2")
        );
        chart.draw(dataTable, options);
      });
  }
}

drawChart();
