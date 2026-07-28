const out = document.getElementById('testResult');

async function call(url) {
  out.textContent = 'Running…';
  try {
    const response = await fetch(url, { method: 'POST' });
    const data = await response.json();
    out.textContent = JSON.stringify(data, null, 2);
    await refreshStatus();
  } catch (error) {
    out.textContent = 'Request failed: ' + error;
  }
}

document.querySelectorAll('[data-action]').forEach((button) => {
  button.addEventListener('click', () => {
    const endpoints = {
      weather: '/api/developer/test-weather',
      preview: '/api/refresh',
      display: '/api/hardware-test',
      scheduler: '/api/restart-scheduler',
    };
    call(endpoints[button.dataset.action]);
  });
});

function text(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
}

function showValue(value, suffix = '') {
  return value === null || value === undefined || value === '' ? '—' : `${value}${suffix}`;
}

async function refreshStatus() {
  try {
    const response = await fetch('/api/developer/status', { cache: 'no-store' });
    const data = await response.json();
    if (!data.ok) return;

    text('lastRefresh', data.status.last_successful_refresh || 'Not yet');
    text('refreshDuration', showValue(data.status.refresh_duration_seconds, ' seconds'));
    text('cpuPercent', showValue(data.system.cpu_percent, '%'));
    text('memoryPercent', showValue(data.system.memory_percent, '%'));
    text('diskPercent', showValue(data.system.disk_percent, '%'));
    text('cpuTemperature', showValue(data.system.temperature_c, '°C'));
    text('heartbeatAge', showValue(data.daemon.heartbeat_age_seconds, ' seconds'));
    text('hostName', data.system.hostname || '—');
    text('displayProfile', data.config.display_profile || 'Default profile');
    text('activeLayout', data.config.layout || data.config.dashboard_layout || 'Weather Station');
    text('activeTheme', data.config.theme || data.config.palette || 'Default');
    text('statusUpdated', 'Updated now');

    const pill = document.getElementById('daemonPill');
    if (pill) {
      pill.textContent = `Daemon ${data.daemon.healthy ? 'healthy' : 'unhealthy'}`;
      pill.classList.toggle('ok', Boolean(data.daemon.healthy));
      pill.classList.toggle('off', !data.daemon.healthy);
    }
  } catch (_) {
    text('statusUpdated', 'Update failed');
  }
}

async function logs() {
  try {
    const response = await fetch('/api/developer/logs', { cache: 'no-store' });
    const data = await response.json();
    const element = document.getElementById('liveLogs');
    element.textContent = (data.lines || []).join('\n') || 'No application log entries yet.';
    element.scrollTop = element.scrollHeight;
  } catch (_) {}
}

document.getElementById('clearLogs')?.addEventListener('click', async () => {
  await fetch('/api/developer/clear-logs', { method: 'POST' });
  logs();
});

document.querySelectorAll('.unit-button').forEach((button) => {
  button.addEventListener('click', async () => {
    const units = button.dataset.units;
    out.textContent = 'Changing temperature units…';
    try {
      const response = await fetch('/api/developer/temperature-units', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ units }),
      });
      const data = await response.json();
      out.textContent = data.message || JSON.stringify(data, null, 2);
      if (data.ok) {
        text('currentUnits', units === 'celsius' ? 'Celsius' : 'Fahrenheit');
        document.querySelectorAll('.unit-button').forEach((candidate) => {
          const selected = candidate.dataset.units === units;
          candidate.classList.toggle('selected', selected);
          candidate.setAttribute('aria-pressed', selected ? 'true' : 'false');
        });
        await refreshStatus();
      }
    } catch (error) {
      out.textContent = 'Unit change failed: ' + error;
    }
  });
});

logs();
refreshStatus();
setInterval(logs, 3000);
setInterval(refreshStatus, 5000);
