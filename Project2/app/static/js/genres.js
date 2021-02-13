(function () {
  'use strict'
  $.get("/countsByGenre", function (data) {
    var chartData = JSON.parse(data);
    var graphDiv = document.getElementById('genres-counts')
    Plotly.plot(graphDiv,
      [{
        type: "bar",
        x: chartData['genre_names'],
        y: chartData['genre_counts']
      }],
      {
        yaxis: {
          title: "Count"
        },
        xaxis: {
          title: "Genre"
        }
      });
  });
})()