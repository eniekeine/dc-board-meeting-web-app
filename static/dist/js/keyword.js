myChart = null
keyword_data_map = {}

function unique(ary){
  ary = ary.filter(function(value, index, self) {
    return self.indexOf(value) === index;
  });
  return ary
}

function initChart()
{
  const ctx = document.getElementById('myChart');
  myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: []
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
function makeYearToCount()
{
  var year_to_count = {}
  for( var keyword in keyword_data_map )
  {
    var data = keyword_data_map[keyword]
    for( var year in data )
    {
      if( year_to_count.hasOwnProperty(year) == false )
        year_to_count[year] = {}
      year_to_count[year][keyword] = data[year]
    }
  }
  return year_to_count
}
function updateChart()
{
  year_to_count = makeYearToCount()
  labels = Object.keys(year_to_count)
  datasets = []
  for( var keyword in keyword_data_map )
  {
    dataset = {
      label: keyword,
      data: [],
      borderWidth: 1,
    }
    for( var year in year_to_count )
      dataset.data.push(year_to_count[year][keyword])
    datasets.push(dataset)
  }
  myChart.data.labels = labels
  myChart.data.datasets = datasets
  myChart.update()
}
function getData(keyword)
{
  fetch('keyword/records/' + keyword)
    .then(response => response.json())
    .then(data => {
      keyword_data_map[keyword] = data
      updateChart()
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
function onCheckBoxChange(event){
  keyword = event.target.value
  if (event.target.checked) {
    getData(keyword)
  } else {
    delete keyword_data_map[keyword]
    updateChart()
  }
}
function onload(event){
  initChart()
  elements = document.getElementsByClassName("chk_keyword")
  for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener("change", onCheckBoxChange)
  }
}
window.addEventListener('load', onload );
