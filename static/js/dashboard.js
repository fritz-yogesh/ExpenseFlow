// Dashboard monthly spending chart
window.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('dashChart');
  if (!canvas || !window.Chart || !window.expenseData) return;
  new Chart(canvas, {type:'line',data:{labels:window.expenseData.labels,datasets:[{data:window.expenseData.values,label:'Expenses',borderColor:'#7762e8',backgroundColor:'rgba(119,98,232,.12)',fill:true,tension:.38,pointRadius:3,pointBackgroundColor:'#7762e8',borderWidth:2.5}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{callbacks:{label:(c)=>' ₹'+Number(c.raw).toLocaleString('en-IN')}}},scales:{x:{grid:{display:false},border:{display:false},ticks:{color:'#9aa0b1'}},y:{beginAtZero:true,grid:{color:'#eff0f5'},border:{display:false},ticks:{color:'#9aa0b1',callback:v=>'₹'+Number(v).toLocaleString('en-IN')}}}}});
});
