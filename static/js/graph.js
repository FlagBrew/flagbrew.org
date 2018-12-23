var downloadChart = null
var destroyBtn = false
var showBtn = true
var downloads = []
var labels = []
var name = ""

function loadData(d, n){
    name = n
    l = 0
    for (var i = 0; i < d.length; i++) { 
        labels.push(d[i].time)
        downloads.push(d[i].amount)
        l = d[i].amount
    }

    if(l == 0){
        document.getElementById("showhide").style.display = "None"
    }

}

function loadGraph(){
    var chartData = {
      labels: labels,
      datasets : [{
          label: name,
          fill: true,
          lineTension: 0.1,
          backgroundColor: "rgba(75,192,192,0.4)",
          borderColor: "rgba(75,192,192,1)",
          borderCapStyle: 'butt',
          borderDash: [],
          borderDashOffset: 0.0,
          borderJoinStyle: 'miter',
          pointBorderColor: "rgba(75,192,192,1)",
          pointBackgroundColor: "#fff",
          pointBorderWidth: 1,
          pointHoverRadius: 5,
          pointHoverBackgroundColor: "rgba(75,192,192,1)",
          pointHoverBorderColor: "rgba(220,220,220,1)",
          pointHoverBorderWidth: 2,
          pointRadius: 1,
          pointHitRadius: 10,
          data: downloads,
          spanGaps: false
      }]
    }
     
    var ctx = document.getElementById("downloadsGraph").getContext("2d");
     
    downloadChart = new Chart(ctx, {
      type: 'line',
      data: chartData,
    });
}    



async function loading(){
    document.getElementById("downloadsGraph").style.display = "none"
    document.getElementById("loading").style.display = "block"
    await sleep(2000);
    document.getElementById("loading").style.display = "none"
    document.getElementById("downloadsGraph").style.display = "block"
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  

loadGraph()
document.getElementById("showhide").addEventListener("click", async function(){
    if (showBtn){
        this.innerHTML = 'Hide <i class="far fa-chart-line"></i>'
        showBtn = false
        loading()
    } else {
        this.innerHTML = 'Show <i class="far fa-chart-line"></i>'
        showBtn = true
    }
});