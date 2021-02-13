(function () {
  'use strict'
  $.get("/countsByCategory", function (data) {
    var chartData = JSON.parse(data);
    var graphDiv = document.getElementById('category-counts')
    Plotly.plot(graphDiv,
      [{
        type: "pie",
        labels: chartData['categories'],
        values: chartData['values']
      }],
      {
        height: 900,
      });
  });
})()