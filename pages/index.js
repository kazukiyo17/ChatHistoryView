var chartDom = document.getElementById("chart");
chartDom.style.height = "300px"; // 设置高度为500px
var myChart = echarts.init(chartDom);
var option;

option = {
  xAxis: {
    type: "category",
    data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  },
  yAxis: {
    type: "value",
  },
  series: [
    {
      data: [150, 230, 224, 218, 135, 147, 260],
      type: "line",
    },
  ],
};

option && myChart.setOption(option);
