google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var data = google.visualization.arrayToDataTable([
    ['Task', 'Hours per Day'],
    ['Work', 8],
    ['Eat', 2],
    ['TV', 4],
    ['Gym', 2],
    ['Sleep', 8]
  ]);

  var options = {
    'width': '100%',
    'height': '100%'
  };

  var chart = new google.visualization.PieChart(document.getElementById('chart1'));
  chart.draw(data, options);
}
