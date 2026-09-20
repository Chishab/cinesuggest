const metrics = JSON.parse(document.getElementById('qa-metrics').dataset.metrics);

new Chart(document.getElementById('test-result-chart'), {
  type: 'doughnut',
  data: { labels: ['Pass', 'Fail', 'Blocked', 'Not run'], datasets: [{ data: [metrics.passed, metrics.failed, metrics.blocked, metrics.not_run], backgroundColor: ['#2a9d8f', '#e4572e', '#f4a261', '#adb5bd'] }] },
  options: { responsive: true }
});

new Chart(document.getElementById('defect-severity-chart'), {
  type: 'bar',
  data: { labels: ['Critical', 'High', 'Medium', 'Low'], datasets: [{ label: 'Defects', data: ['Critical', 'High', 'Medium', 'Low'].map(key => metrics.severity[key] || 0), backgroundColor: '#e4572e' }] },
  options: { responsive: true, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } }
});

new Chart(document.getElementById('defect-status-chart'), {
  type: 'doughnut',
  data: { labels: Object.keys(metrics.statuses), datasets: [{ data: Object.values(metrics.statuses), backgroundColor: ['#e4572e', '#f4a261', '#2a9d8f', '#264653', '#adb5bd'] }] },
  options: { responsive: true }
});

new Chart(document.getElementById('coverage-chart'), {
  type: 'bar',
  data: { labels: ['Requirements covered', 'Automation passed'], datasets: [{ label: 'Count', data: [metrics.requirements_covered, metrics.automation_passed], backgroundColor: ['#2a9d8f', '#264653'] }] },
  options: { responsive: true, scales: { y: { beginAtZero: true, ticks: { precision: 0 } } } }
});
