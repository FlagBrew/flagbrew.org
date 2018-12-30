// function masterStats(d){
//     var data = JSON.parse(d)
//     dataSets = []
//     labels = []
//     labels_done = false
//     for(var i = 0; i < data.length; i++){
//         tmpData = []
//         l = 0
//         for (var ii = 0; ii < data[i].length; ii++){
//             if(i == 0){
//                 l = data[i][ii].amount
//                 continue
//             }
//             if(!labels_done){
//                 labels.push(data[i][ii].time)
//             }
//             console.log(data[i])
//             tmpData.push(data[i][ii].amount - l)
//             l = data[i][ii].amount
//         }
//         labels_done = true
    //     dataSets.push({
    //         label: data[i].name + " Daily Downloads",
    //         fill: true,
    //         lineTension: 0.1,
    //         backgroundColor: "rgba(75,192,192,0.4)",
    //         borderColor: "rgba(75,192,192,1)",
    //         borderCapStyle: 'butt',
    //         borderDash: [],
    //         borderDashOffset: 0.0,
    //         borderJoinStyle: 'miter',
    //         pointBorderColor: "rgba(75,192,192,1)",
    //         pointBackgroundColor: "#fff",
    //         pointBorderWidth: 1,
    //         pointHoverRadius: 5,
    //         pointHoverBackgroundColor: "rgba(75,192,192,1)",
    //         pointHoverBorderColor: "rgba(220,220,220,1)",
    //         pointHoverBorderWidth: 2,
    //         pointRadius: 1,
    //         pointHitRadius: 10,
    //         data: tmpData,
    //         spanGaps: false
    //     })
    // }

//     let chartData = {
//         labels: labels,
//         dataSets: dataSets
//     }
//     console.log(labels)
//     let ctx = document.getElementById("statsGraph").getContext("2d");
     
//     let statsChart = new Chart(ctx, {
//       type: 'line',
//       data: chartData,
//       options: {
//         responsive: true
//       }
//     });
// }

function masterStats(data){
    var d = JSON.parse(data)
    labels = []
    labels_done = false
    dataSets = []
    for(var i = 0; i < d.length; i++){
        // skip if no downloads
        if(d[i].downloads.length <= 1){
            continue
        } else if(d[i].downloads[d[i].downloads.length-1].amount == 0){
            // if there are no downloads at all, we can skip...
            continue
        }
        tmpData = []
        l = 0
        for(var ii = 0; ii < d[i].downloads.length; ii++){
            // skip first date
            if(ii == 0){
                l = d[i].downloads[ii].amount
                continue
            }
            
            if(!labels_done){
                labels.push(d[i].downloads[ii].time)
            }
            tmpData.push(d[i].downloads[ii].amount - l)
            l = d[i].downloads[ii].amount
        }
        if(!labels_done){
            labels_done = true
        }
        // credits: https://stackoverflow.com/a/45772013
        var dynamicColors = function() {
            var r = Math.floor(Math.random() * 255);
            var g = Math.floor(Math.random() * 255);
            var b = Math.floor(Math.random() * 255);
            return "rgb(" + r + "," + g + "," + b + ")";
         };

        dataSets.push({
            label: d[i].name + " Daily Downloads",
            fill: true,
            data: tmpData,
            spanGaps: false,
            backgroundColor: dynamicColors()
        })
    }
    let chartData = {
        labels: labels,
        datasets: dataSets
    }
    let ctx = document.getElementById("statsGraph").getContext("2d");  
    let statsChart = new Chart(ctx, {
      type: 'bar',
      data: chartData,
      options: {
        responsive: true
      }
    });
    console.log(dataSets)
}