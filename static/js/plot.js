var x = [1, 2, 3, 4, 5, 6];
var y = [2, 6.5, 1, 10, 7, 8];

// Define color ranges and corresponding colors
var colorRanges = [
  { min: 0, max: 5, color: "green" },
  { min: 5, max: 6, color: "yellow" },
  { min: 6, max: 7, color: "orange" },
  { min: 7, max: 8, color: "red" },
  { min: 8, max: 15, color: "#8c0808" },
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
    mode: "lines+markers",
    type: "scatter",
    marker: {
      color: colors, // Marker color
      size: 10, // Marker size
      symbol: "circle", // Marker symbol (options: 'circle', 'square', 'diamond', 'cross', etc.)
    },
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
    title: "Time",
  },
  yaxis: {
    title: "",
    gridcolor: colors,
  },
  shapes: shapes, // Add the shaded regions to the layout
};

// Create the plot
Plotly.newPlot("plot", data, layout);
