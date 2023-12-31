var x = [1, 2, 3, 4, 5, 6];
var y = [2, 6.5, 1, 10, 7, 8];

function plot(data) {
  var x = data["x"];
  var y = data["y"];
  var colorRanges = [
    { min: 0, max: 5, color: "green" },
    { min: 5, max: 6, color: "yellow" },
    { min: 6, max: 7, color: "orange" },
    { min: 7, max: 8, color: "red" },
    { min: 8, max: 10, color: "#8c0808" },
  ];

  // Create an array to hold the colors based on y values
  var colors = y.map(function (value) {
    for (var i = 0; i < colorRanges.length; i++) {
      if (value >= colorRanges[i].min && value < colorRanges[i].max) {
        return colorRanges[i].color;
      }
    }
    // If no range is matched, use a default color
    return "gray";
  });

  var data = [
    {
      x: x,
      y: y,
      mode: "lines",
      type: "scatter",
      line: {
        color: "grey",
      },
    },
  ];
  // Create shaded regions for color ranges
  var shapes = [];
  for (var i = 0; i < colorRanges.length; i++) {
    shapes.push({
      type: "rect",
      x0: Math.min.apply(Math, x),
      x1: Math.max.apply(Math, x),
      y0: colorRanges[i].min,
      y1: colorRanges[i].max,
      fillcolor: colorRanges[i].color,
      opacity: 0.5,
      line: {
        width: 0,
      },
    });
  }

  // Layout configuration
  var layout = {
    title: "Kp Index",
    xaxis: {
      title: "Day hours",
    },
    yaxis: {
      title: "",
      gridcolor: colors,
    },
    shapes: shapes, // Add the shaded regions to the layout
  };

  // Create the plot
  Plotly.newPlot("plot", data, layout);
}
