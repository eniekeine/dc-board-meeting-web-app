lastChart = null
function makeChart(keyword, data){
  const ctx = document.getElementById('myChart');
  keys = Object.keys(data)
  console.log(keys)
  values = Object.values(data)
  console.log(values)
  if( lastChart != null )
    lastChart.destroy();
  lastChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: keys,
      datasets: [{
        label: keyword,
        data: values,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}
function onCheckBoxChange(event){
  keyword = event.target.value
  if (event.target.checked) {
    getData(keyword)
  } else {
  }
}
function onload(event){
  elements = document.getElementsByClassName("chk_keyword")
  for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener("change", onCheckBoxChange)
  }
}
window.addEventListener('load', onload );
function getData(keyword)
{
  fetch('keyword/records/' + keyword)
    .then(response => response.json())
    .then(data => {
      makeChart(keyword, data)
    })
    .catch(error => {
      console.error('Error:', error);
    });
}