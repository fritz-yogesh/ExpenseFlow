// Chart.js visualizations use aggregates computed by the Pandas analytics module.
window.addEventListener('DOMContentLoaded', () => {
 const d=window.analyticsData;if(!d||!window.Chart)return;
 Chart.defaults.font.family="'DM Sans',sans-serif"; Chart.defaults.color='#8b91a3';
 const money={callbacks:{label:c=>' '+c.dataset.label+': ₹'+Number(c.raw).toLocaleString('en-IN')}};
 const base={responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:money},scales:{x:{grid:{display:false},border:{display:false}},y:{beginAtZero:true,grid:{color:'#eff0f5'},border:{display:false},ticks:{callback:v=>'₹'+Number(v).toLocaleString('en-IN')}}}};
 const colors=['#7966e8','#55b59a','#f4a26c','#6ba8df','#e98698','#a88bdd','#dfc45c','#75bdc4'];
 const line=document.getElementById('expenseLine');if(line)new Chart(line,{type:'line',data:{labels:d.monthlyLabels,datasets:[{label:'Expenses',data:d.monthlyExpenses,borderColor:'#7966e8',backgroundColor:'rgba(121,102,232,.12)',fill:true,tension:.36,pointRadius:3,borderWidth:2.5}]},options:base});
 const bar=document.getElementById('incomeBar');if(bar)new Chart(bar,{type:'bar',data:{labels:d.monthlyLabels,datasets:[{label:'Income',data:d.monthlyLabels.map(x=>{const i=d.incomeLabels.indexOf(x);return i<0?0:d.monthlyIncome[i]}),backgroundColor:'#64bea1',borderRadius:5},{label:'Expenses',data:d.monthlyLabels.map(x=>{const i=d.monthlyLabels.indexOf(x);return i<0?0:d.monthlyExpenses[i]}),backgroundColor:'#f19182',borderRadius:5}]},options:{...base,plugins:{...base.plugins,legend:{display:true,position:'bottom',labels:{usePointStyle:true,boxWidth:7}}}}});
 const donut=document.getElementById('categoryDonut');if(donut)new Chart(donut,{type:'doughnut',data:{labels:d.categoryLabels,datasets:[{data:d.categoryValues,backgroundColor:colors,borderWidth:3,borderColor:'#fff',hoverOffset:5}]},options:{responsive:true,maintainAspectRatio:false,cutout:'66%',plugins:{legend:{position:'bottom',labels:{usePointStyle:true,boxWidth:8,padding:14}},tooltip:money}}});
 const top=document.getElementById('topBar');if(top)new Chart(top,{type:'bar',data:{labels:d.topLabels,datasets:[{label:'Expenses',data:d.topValues,backgroundColor:colors,borderRadius:5}]},options:{...base,indexAxis:'y'}});
});
