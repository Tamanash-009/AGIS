/* ═══════════════════════════════════════════════════════════════
   AGIS Dashboard — Enterprise JavaScript
   Clean charts, realistic data, incident management
   ═══════════════════════════════════════════════════════════════ */

// ─── Chart.js Defaults (Enterprise) ──────────────────────────
Chart.defaults.color = '#94A3B8';
Chart.defaults.borderColor = 'rgba(148, 163, 184, 0.08)';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.pointStyle = 'circle';
Chart.defaults.plugins.legend.labels.padding = 14;
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(15, 23, 42, 0.95)';
Chart.defaults.plugins.tooltip.borderColor = 'rgba(59, 130, 246, 0.15)';
Chart.defaults.plugins.tooltip.borderWidth = 1;
Chart.defaults.plugins.tooltip.cornerRadius = 6;
Chart.defaults.plugins.tooltip.padding = 10;
Chart.defaults.elements.point.radius = 2;
Chart.defaults.elements.point.hoverRadius = 5;
Chart.defaults.elements.line.tension = 0.35;
Chart.defaults.animation.duration = 800;
Chart.defaults.animation.easing = 'easeOutQuart';

// ─── Enterprise Color Palette ────────────────────────────────
const C = {
    blue:    '#3B82F6',
    purple:  '#8B5CF6',
    teal:    '#06B6D4',
    green:   '#22C55E',
    red:     '#EF4444',
    amber:   '#F59E0B',
    orange:  '#F97316',
    pink:    '#EC4899',
    slate:   '#64748B',
    blueDim: 'rgba(59, 130, 246, 0.12)',
    fill: (ctx, color, a1 = 0.15, a2 = 0.01) => {
        const g = ctx.createLinearGradient(0, 0, 0, 300);
        g.addColorStop(0, color.replace(')', `, ${a1})`).replace('rgb', 'rgba').replace('#', ''));
        g.addColorStop(1, color.replace(')', `, ${a2})`).replace('rgb', 'rgba').replace('#', ''));
        // Fallback for hex
        return `rgba(${parseInt(color.slice(1,3),16)},${parseInt(color.slice(3,5),16)},${parseInt(color.slice(5,7),16)},${a1})`;
    }
};

const GRID = { color: 'rgba(148, 163, 184, 0.06)' };
const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

// ─── Noise Utility ───────────────────────────────────────────
function noise(base, pct = 0.03) {
    return +(base * (1 + (Math.random() - 0.5) * 2 * pct)).toFixed(1);
}


// ═══════════════════════════════════════════════════════════════
// NAVIGATION
// ═══════════════════════════════════════════════════════════════
const pageTitles = {
    executive:     'Executive Overview',
    flights:       'Flight Operations',
    core:          'Propulsion Analytics',
    maintenance:   'Maintenance & Incidents',
    manufacturing: 'Manufacturing Intelligence',
    finance:       'Financial Analysis',
    missions:      'Mission Intelligence Center',
    geo:           'Geographic Intelligence',
    predict:       'Predictive Analytics',
    insights:      'Executive Insights'
};

document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
        const page = item.dataset.page;
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        item.classList.add('active');
        document.querySelectorAll('.dashboard-page').forEach(p => p.classList.remove('active'));
        document.getElementById(`page-${page}`).classList.add('active');
        document.getElementById('page-title').textContent = pageTitles[page];
        document.getElementById('sidebar').classList.remove('open');
    });
});

document.getElementById('menu-toggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('open');
});

// Keyboard nav (1-0)
document.addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    const keys = { '1':'executive','2':'flights','3':'core','4':'maintenance','5':'manufacturing','6':'finance','7':'missions','8':'geo','9':'predict','0':'insights' };
    if (keys[e.key]) document.querySelector(`.nav-item[data-page="${keys[e.key]}"]`)?.click();
    if (e.key === 'Escape') closeNotifs();
});

// Clock
function updateClock() {
    const d = new Date();
    const el = document.getElementById('date-display');
    if (el) el.textContent = d.toLocaleString('en-US', {
        weekday:'short', year:'numeric', month:'short', day:'numeric',
        hour:'2-digit', minute:'2-digit', second:'2-digit'
    });
}
updateClock();
setInterval(updateClock, 1000);

// Notifications
const badge = document.getElementById('alert-badge');
const drawer = document.getElementById('notif-drawer');
const backdrop = document.getElementById('notif-backdrop');
function openNotifs() { drawer?.classList.add('open'); backdrop?.classList.add('open'); }
function closeNotifs() { drawer?.classList.remove('open'); backdrop?.classList.remove('open'); }
badge?.addEventListener('click', openNotifs);
document.getElementById('notif-close')?.addEventListener('click', closeNotifs);
backdrop?.addEventListener('click', closeNotifs);


// ═══════════════════════════════════════════════════════════════
// PAGE 1: EXECUTIVE OVERVIEW
// ═══════════════════════════════════════════════════════════════

// Flight Volume — seasonal: dip in winter (Dec-Feb), peak in spring/summer
(function() {
    const ctx = document.getElementById('chart-flight-trend').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: MONTHS,
            datasets: [
                {
                    label: 'Flights',
                    data: [178, 165, 203, 248, 287, 312, 298, 334, 321, 346, 289, 218],
                    backgroundColor: 'rgba(59, 130, 246, 0.5)',
                    borderColor: C.blue,
                    borderWidth: 1,
                    borderRadius: 4,
                    borderSkipped: false,
                    order: 2,
                },
                {
                    label: 'Success %',
                    data: [94.2, 93.1, 89.2, 94.8, 95.1, 96.3, 93.4, 95.7, 94.6, 93.8, 95.2, 93.7],
                    type: 'line',
                    borderColor: C.green,
                    backgroundColor: 'transparent',
                    pointBackgroundColor: C.green,
                    borderWidth: 2,
                    yAxisID: 'y1',
                    order: 1,
                }
            ]
        },
        options: {
            responsive: true,
            interaction: { intersect: false, mode: 'index' },
            scales: {
                y: { beginAtZero: true, grid: GRID, title: { display: true, text: 'Flights', color: '#64748B' } },
                y1: { position: 'right', min: 85, max: 100, grid: { display: false },
                      title: { display: true, text: 'Success %', color: '#64748B' },
                      ticks: { callback: v => v + '%' } },
                x: { grid: { display: false } }
            }
        }
    });
})();

// Fleet Capability — grouped bar (replaces radar for enterprise readability)
(function() {
    const ctx = document.getElementById('chart-fleet-matrix').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Speed', 'Efficiency', 'Stability', 'Range', 'Stealth', 'Payload'],
            datasets: [
                { label: 'AG-X2 Tactical', data: [92,78,85,70,88,45], backgroundColor: 'rgba(59,130,246,0.6)', borderRadius: 3 },
                { label: 'AG-X4 Stealth', data: [88,85,82,90,96,35], backgroundColor: 'rgba(139,92,246,0.6)', borderRadius: 3 },
                { label: 'AG-X7 Command', data: [72,70,90,85,60,92], backgroundColor: 'rgba(6,182,212,0.6)', borderRadius: 3 }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, max: 100, grid: GRID },
                x: { grid: { display: false } }
            },
            plugins: { legend: { position: 'bottom' } }
        }
    });
})();

// Mission Types
(function() {
    const ctx = document.getElementById('chart-mission-types').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Test Flight', 'Endurance', 'Combat Sim', 'Recon', 'Cargo', 'Calibration'],
            datasets: [{
                data: [27.3, 19.1, 14.8, 15.2, 12.4, 11.2],
                backgroundColor: [C.blue, C.purple, C.orange, C.green, C.teal, C.pink],
                borderColor: '#1E293B',
                borderWidth: 2,
                hoverOffset: 6,
            }]
        },
        options: {
            responsive: true,
            cutout: '62%',
            plugins: { legend: { position: 'right', labels: { font: { size: 10 } } } }
        }
    });
})();

// Revenue vs R&D — realistic with flat Q3-2023
(function() {
    const ctx = document.getElementById('chart-revenue-rd').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['2021', '2022', '2023', '2024', '2025'],
            datasets: [
                {
                    label: 'Revenue ($M)',
                    data: [118, 214, 367, 584, 980],
                    borderColor: C.green,
                    backgroundColor: 'rgba(34, 197, 94, 0.06)',
                    fill: true, borderWidth: 2,
                    pointBackgroundColor: C.green,
                },
                {
                    label: 'R&D ($M)',
                    data: [82, 108, 143, 189, 242],
                    borderColor: C.purple,
                    backgroundColor: 'rgba(139, 92, 246, 0.06)',
                    fill: true, borderWidth: 2,
                    pointBackgroundColor: C.purple,
                },
                {
                    label: 'CapEx ($M)',
                    data: [195, 148, 287, 176, 423],
                    borderColor: C.amber,
                    borderWidth: 1.5, borderDash: [5, 5],
                    pointBackgroundColor: C.amber,
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, grid: GRID, ticks: { callback: v => '$' + v + 'M' } },
                x: { grid: { display: false } }
            }
        }
    });
})();


// ═══════════════════════════════════════════════════════════════
// PAGE 2: FLIGHT OPERATIONS
// ═══════════════════════════════════════════════════════════════

(function() {
    const ctx = document.getElementById('chart-altitude-profile').getContext('2d');
    const n = 60;
    const alt1 = [], alt2 = [], alt3 = [];
    for (let i = 0; i < n; i++) {
        const t = i / n;
        alt1.push(Math.sin(t * Math.PI) * 28000 + (Math.random() - 0.5) * 1200);
        alt2.push(Math.sin(t * Math.PI) * 16000 * (t < 0.5 ? t * 2 : 2 - t * 2) + (Math.random() - 0.5) * 800 + 4000);
        alt3.push(Math.sin(t * Math.PI * 0.9) * 31000 + (Math.random() - 0.5) * 1500);
    }
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: n}, (_, i) => ''),
            datasets: [
                { label: 'FLT-2847 (AG-X4)', data: alt3, borderColor: C.blue, borderWidth: 1.5, pointRadius: 0 },
                { label: 'FLT-2846 (AG-X2)', data: alt1, borderColor: C.purple, borderWidth: 1.5, pointRadius: 0 },
                { label: 'FLT-2845 (AG-X6)', data: alt2, borderColor: C.teal, borderWidth: 1, pointRadius: 0, borderDash: [4,4] },
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { title: { display: true, text: 'Altitude (m)' }, grid: GRID },
                x: { display: false }
            }
        }
    });
})();

(function() {
    const ctx = document.getElementById('chart-vel-stability').getContext('2d');
    const d1 = [], d2 = [];
    for (let i = 0; i < 80; i++) {
        const v = 100 + Math.random() * 1400;
        const s = 95 - (v/1500)*30 + (Math.random()-0.5)*18;
        d1.push({ x: +v.toFixed(0), y: +Math.max(38,Math.min(100,s)).toFixed(1) });
    }
    for (let i = 0; i < 35; i++) {
        const v = 200 + Math.random() * 800;
        const s = 88 - (v/1000)*22 + (Math.random()-0.5)*12;
        d2.push({ x: +v.toFixed(0), y: +Math.max(45,Math.min(100,s)).toFixed(1) });
    }
    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                { label: 'Active Fleet', data: d1, backgroundColor: 'rgba(59,130,246,0.4)', borderColor: C.blue, borderWidth: 1, pointRadius: 3 },
                { label: 'Maintenance Hold', data: d2, backgroundColor: 'rgba(249,115,22,0.4)', borderColor: C.orange, borderWidth: 1, pointRadius: 3 },
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Velocity (m/s)' }, grid: GRID },
                y: { title: { display: true, text: 'Stability Index' }, min: 35, max: 100, grid: GRID }
            }
        }
    });
})();

(function() {
    const ctx = document.getElementById('chart-phase-dist').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Takeoff', 'Climb', 'Cruise', 'Descent', 'Landing'],
            datasets: [{ data: [11.3, 17.2, 38.4, 19.8, 13.3],
                backgroundColor: [C.green, C.blue, C.purple, C.teal, C.amber],
                borderRadius: 4, borderSkipped: false }]
        },
        options: {
            responsive: true, indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: { x: { ticks: { callback: v => v + '%' }, grid: GRID }, y: { grid: { display: false } } }
        }
    });
})();

(function() {
    const ctx = document.getElementById('chart-mission-status').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Completed', 'Aborted', 'Anomaly Detected', 'In Progress'],
            datasets: [{ data: [2318, 167, 214, 148],
                backgroundColor: [C.green, C.red, C.amber, C.blue],
                borderColor: '#1E293B', borderWidth: 2 }]
        },
        options: { responsive: true, cutout: '58%', plugins: { legend: { position: 'right' } } }
    });
})();


// ═══════════════════════════════════════════════════════════════
// PAGE 3: PROPULSION ANALYTICS
// ═══════════════════════════════════════════════════════════════

(function() {
    const ctx = document.getElementById('chart-energy-lift').getContext('2d');
    // Seasonal pattern: higher energy in summer testing
    const energy = [98, 94, 102, 118, 132, 148, 141, 153, 137, 128, 112, 104];
    const lift = [37.2, 36.8, 38.4, 41.2, 43.8, 46.1, 44.3, 47.2, 43.9, 42.1, 39.8, 38.6];
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: MONTHS,
            datasets: [
                { label: 'Energy (MW)', data: energy, borderColor: C.amber, backgroundColor: 'rgba(245,158,11,0.04)', fill: true, borderWidth: 2 },
                { label: 'Lift (kN)', data: lift, borderColor: C.blue, backgroundColor: 'rgba(59,130,246,0.04)', fill: true, borderWidth: 2, yAxisID: 'y1' }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { title: { display: true, text: 'Energy (MW)' }, grid: GRID },
                y1: { position: 'right', title: { display: true, text: 'Lift (kN)' }, grid: { display: false } },
                x: { grid: { display: false } }
            }
        }
    });
})();

(function() {
    const ctx = document.getElementById('chart-temp-trend').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: MONTHS,
            datasets: [
                { label: 'Avg Temp', data: [178, 174, 182, 191, 198, 204, 197, 208, 201, 194, 186, 181],
                    borderColor: C.amber, borderWidth: 2, pointBackgroundColor: C.amber },
                { label: 'Max Temp', data: [234, 228, 247, 261, 278, 293, 284, 301, 289, 271, 254, 241],
                    borderColor: C.red, borderWidth: 1.5, borderDash: [5,5], pointBackgroundColor: C.red },
                { label: 'Critical Limit', data: Array(12).fill(280),
                    borderColor: 'rgba(239,68,68,0.3)', borderWidth: 1, borderDash: [10,5], pointRadius: 0 }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { title: { display: true, text: 'Temperature (°C)' }, grid: GRID },
                x: { grid: { display: false } }
            }
        }
    });
})();

(function() {
    const ctx = document.getElementById('chart-health-model').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['AG-X1', 'AG-X2', 'AG-X3', 'AG-X4', 'AG-X5', 'AG-X6', 'AG-X7'],
            datasets: [{ label: 'Avg Core Health',
                data: [0.823, 0.764, 0.851, 0.712, 0.887, 0.798, 0.743],
                backgroundColor: function(ctx) {
                    const v = ctx.raw;
                    if (v >= 0.8) return 'rgba(34,197,94,0.5)';
                    if (v >= 0.7) return 'rgba(245,158,11,0.5)';
                    return 'rgba(239,68,68,0.5)';
                },
                borderRadius: 4 }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { min: 0.5, max: 1, grid: GRID }, x: { grid: { display: false } } }
        }
    });
})();

(function() {
    const ctx = document.getElementById('chart-stress-index').getContext('2d');
    const pts = [];
    for (let i = 0; i < 50; i++) {
        const stress = Math.random() * 0.85;
        const stab = 96 - stress * 55 + (Math.random() - 0.5) * 18;
        pts.push({ x: +stress.toFixed(3), y: +Math.max(35, Math.min(100, stab)).toFixed(1) });
    }
    new Chart(ctx, {
        type: 'scatter',
        data: { datasets: [{ label: 'Aircraft', data: pts, backgroundColor: 'rgba(139,92,246,0.4)', borderColor: C.purple, pointRadius: 4 }] },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Core Stress Index' }, grid: GRID },
                y: { title: { display: true, text: 'Stability Score' }, grid: GRID }
            }
        }
    });
})();


// ═══════════════════════════════════════════════════════════════
// PAGE 4: MAINTENANCE & INCIDENTS
// ═══════════════════════════════════════════════════════════════

// Risk Grid
(function() {
    const grid = document.getElementById('risk-grid');
    if (!grid) return;
    const aircraft = [];
    // Deterministic seed-like approach for consistency
    const risks = [87,82,74,71,68,63,58,54,51,47,43,41,38,35,32,28,24,21,18,16,14,12,9,7,4];
    for (let i = 0; i < 25; i++) {
        const r = risks[i] + Math.floor(Math.random() * 5 - 2);
        let cls = 'risk-low';
        if (r > 75) cls = 'risk-critical';
        else if (r > 55) cls = 'risk-high';
        else if (r > 30) cls = 'risk-medium';
        aircraft.push({ id: `AG-${String(i+1).padStart(4,'0')}`, risk: Math.max(2,Math.min(98,r)), cls });
    }
    aircraft.sort((a,b) => b.risk - a.risk);
    aircraft.forEach(ac => {
        const cell = document.createElement('div');
        cell.className = `risk-cell ${ac.cls}`;
        cell.innerHTML = `<span class="risk-id">${ac.id}</span><span class="risk-pct">${ac.risk}%</span>`;
        cell.title = `${ac.id}: ${ac.risk}% failure probability`;
        grid.appendChild(cell);
    });
})();

// Maintenance Cost
(function() {
    const ctx = document.getElementById('chart-maint-cost').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Corrective', 'Preventive', 'Predictive', 'Emergency'],
            datasets: [
                { label: 'FY2024', data: [4.2, 2.8, 1.9, 3.4], backgroundColor: 'rgba(139,92,246,0.5)', borderRadius: 4 },
                { label: 'FY2025', data: [3.7, 3.4, 2.9, 2.1], backgroundColor: 'rgba(59,130,246,0.5)', borderRadius: 4 }
            ]
        },
        options: {
            responsive: true,
            scales: { y: { title: { display: true, text: 'Cost ($M)' }, grid: GRID }, x: { grid: { display: false } } }
        }
    });
})();

// Incident Table
(function() {
    const tbody = document.getElementById('incident-tbody');
    if (!tbody) return;
    const incidents = [
        { id: 'INC-2025-047', aircraft: 'AG-0032', desc: 'AG Core thermal runaway — field stability fluctuation at 28,400m', severity: 'critical', status: 'open', team: 'Propulsion Eng.', time: '2025-05-29 08:14' },
        { id: 'INC-2025-046', aircraft: 'AG-0017', desc: 'Emergency shutdown during high-G maneuver — power core overheat', severity: 'critical', status: 'resolved', team: 'Safety Ops', time: '2025-05-28 14:32' },
        { id: 'INC-2025-045', aircraft: 'AG-0044', desc: 'Navigation drift event — 340m deviation from planned trajectory', severity: 'high', status: 'investigating', team: 'Flight Ops', time: '2025-05-27 11:47' },
        { id: 'INC-2025-044', aircraft: 'AG-0009', desc: 'Stabilizer actuator degradation — intermittent vibration at cruise', severity: 'medium', status: 'scheduled', team: 'Maintenance', time: '2025-05-26 09:03' },
        { id: 'INC-2025-043', aircraft: 'AG-0028', desc: 'Energy grid micro-fracture — efficiency drop 4.2% below baseline', severity: 'high', status: 'resolved', team: 'Propulsion Eng.', time: '2025-05-25 16:21' },
        { id: 'INC-2025-042', aircraft: 'AG-0035', desc: 'Hydraulic pressure anomaly — left dampener below operating range', severity: 'medium', status: 'resolved', team: 'Maintenance', time: '2025-05-24 07:45' },
        { id: 'INC-2025-041', aircraft: 'AG-0011', desc: 'Software fault in flight controller — auto-corrected, logged for review', severity: 'low', status: 'closed', team: 'Avionics', time: '2025-05-23 13:12' },
        { id: 'INC-2025-040', aircraft: 'AG-0021', desc: 'Thermal shield erosion detected during post-flight inspection', severity: 'medium', status: 'scheduled', team: 'Materials Eng.', time: '2025-05-22 10:38' },
    ];
    incidents.forEach(inc => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="id-cell">${inc.id}</td>
            <td style="font-family:'JetBrains Mono',monospace;font-weight:600;color:var(--text-primary)">${inc.aircraft}</td>
            <td>${inc.desc}</td>
            <td><span class="severity-badge ${inc.severity}">${inc.severity}</span></td>
            <td><span class="status-badge ${inc.status}">${inc.status.replace('investigating','invest.').replace('scheduled','sched.')}</span></td>
            <td style="white-space:nowrap">${inc.team}</td>
            <td style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;white-space:nowrap">${inc.time}</td>
        `;
        tbody.appendChild(tr);
    });
})();

// Failure Categories
(function() {
    const ctx = document.getElementById('chart-failure-cat').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Mechanical', 'Electrical', 'Thermal', 'Software', 'Structural', 'Hydraulic'],
            datasets: [{ data: [27.4, 21.8, 16.3, 14.7, 11.2, 8.6],
                backgroundColor: [C.blue, C.purple, C.red, C.teal, C.amber, C.green].map(c => c + '80'),
                borderColor: [C.blue, C.purple, C.red, C.teal, C.amber, C.green],
                borderWidth: 1, borderRadius: 4 }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { ticks: { callback: v => v + '%' }, grid: GRID }, x: { grid: { display: false } } }
        }
    });
})();

// Downtime Trend — with target line and realistic variance
(function() {
    const ctx = document.getElementById('chart-downtime').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: MONTHS,
            datasets: [
                { label: 'Downtime (hrs)',
                    data: [438, 392, 467, 318, 284, 347, 401, 273, 256, 312, 248, 231],
                    borderColor: C.amber, backgroundColor: 'rgba(245,158,11,0.06)', fill: true, borderWidth: 2 },
                { label: 'Target',
                    data: Array(12).fill(300),
                    borderColor: 'rgba(34,197,94,0.4)', borderWidth: 1.5, borderDash: [5,5], pointRadius: 0 }
            ]
        },
        options: {
            responsive: true,
            scales: { y: { title: { display: true, text: 'Hours' }, grid: GRID }, x: { grid: { display: false } } }
        }
    });
})();


// ═══════════════════════════════════════════════════════════════
// PAGE 5: MANUFACTURING
// ═══════════════════════════════════════════════════════════════

(function() {
    const ctx = document.getElementById('chart-defect-comp').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['AG Core', 'Stabilizer', 'Power Cell', 'Thermal Shield', 'Control Unit',
                     'Dampener', 'Processor', 'Nozzle', 'Energy Grid', 'Frame'],
            datasets: [{ label: 'Defect %',
                data: [4.3, 3.2, 5.7, 2.1, 6.4, 3.8, 7.1, 4.6, 2.8, 1.9],
                backgroundColor: 'rgba(59,130,246,0.5)',
                borderColor: C.blue, borderWidth: 1, borderRadius: 4 }]
        },
        options: {
            responsive: true, indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: { x: { ticks: { callback: v => v + '%' }, grid: GRID }, y: { grid: { display: false } } }
        }
    });
})();

(function() {
    const ctx = document.getElementById('chart-factory-perf').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Titan Works', 'Aurora', 'Nebula Forge', 'Quantum Bay', 'Vortex Plant', 'Eclipse', 'Helios Hub', 'Zenith Stn'],
            datasets: [
                { label: 'Yield %', data: [96.3, 97.8, 94.7, 98.1, 92.9, 95.4, 93.8, 95.6],
                    backgroundColor: 'rgba(59,130,246,0.4)', borderColor: C.blue, borderWidth: 1, borderRadius: 4 },
                { label: 'Output (units)', data: [4180, 7240, 5380, 6310, 3740, 4870, 2790, 3180],
                    type: 'line', borderColor: C.amber, borderWidth: 2, pointBackgroundColor: C.amber, yAxisID: 'y1' }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { title: { display: true, text: 'Yield %' }, min: 90, max: 100, grid: GRID },
                y1: { position: 'right', title: { display: true, text: 'Units' }, grid: { display: false } },
                x: { grid: { display: false }, ticks: { font: { size: 9 } } }
            }
        }
    });
})();

(function() {
    const ctx = document.getElementById('chart-quality-grade').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['A+ (Premium)', 'A (Standard)', 'B (Acceptable)', 'C (Review)', 'D (Reject)'],
            datasets: [{ data: [33.4, 31.2, 20.8, 9.4, 5.2],
                backgroundColor: [C.green, C.blue, C.purple, C.amber, C.red],
                borderColor: '#1E293B', borderWidth: 2 }]
        },
        options: { responsive: true, cutout: '62%' }
    });
})();

(function() {
    const ctx = document.getElementById('chart-prod-cost-trend').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Q1-21','Q2-21','Q3-21','Q4-21','Q1-22','Q2-22','Q3-22','Q4-22',
                     'Q1-23','Q2-23','Q3-23','Q4-23','Q1-24','Q2-24','Q3-24','Q4-24',
                     'Q1-25','Q2-25','Q3-25','Q4-25'],
            datasets: [{
                label: 'Cost/Unit ($K)',
                data: [18.4,17.6,16.9,16.3,15.8,15.2,14.7,14.3,14.1,13.6,13.8,12.9,12.6,12.4,12.2,11.8,11.9,11.6,11.4,11.2],
                borderColor: C.blue, backgroundColor: 'rgba(59,130,246,0.04)', fill: true, borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { title: { display: true, text: 'Cost ($K)' }, grid: GRID },
                x: { grid: { display: false }, ticks: { font: { size: 9 }, maxRotation: 45 } }
            }
        }
    });
})();


// ═══════════════════════════════════════════════════════════════
// PAGE 6: FINANCIAL ANALYSIS
// ═══════════════════════════════════════════════════════════════

(function() {
    const ctx = document.getElementById('chart-budget-actual').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: MONTHS,
            datasets: [
                { label: 'Budget', data: [8.2,8.4,8.1,8.5,8.8,9.0,9.1,9.2,9.0,9.3,9.5,9.7],
                    backgroundColor: 'rgba(139,92,246,0.4)', borderColor: C.purple, borderWidth: 1, borderRadius: 4 },
                { label: 'Actual', data: [8.6,8.1,9.2,8.3,9.4,8.7,10.1,9.0,9.7,9.1,10.3,9.4],
                    backgroundColor: 'rgba(59,130,246,0.4)', borderColor: C.blue, borderWidth: 1, borderRadius: 4 },
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { title: { display: true, text: 'Amount ($M)' }, grid: GRID },
                x: { grid: { display: false } }
            }
        }
    });
})();

(function() {
    const ctx = document.getElementById('chart-rd-dept').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['R&D Propulsion', 'R&D Materials', 'Engineering', 'Manufacturing', 'Flight Ops', 'QA'],
            datasets: [{ label: 'R&D ($M)', data: [82, 54, 38, 28, 22, 18],
                backgroundColor: 'rgba(59,130,246,0.5)',
                borderRadius: 4, borderSkipped: false }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { title: { display: true, text: '$M' }, grid: GRID }, x: { grid: { display: false }, ticks: { font: { size: 9 } } } }
        }
    });
})();

(function() {
    const ctx = document.getElementById('chart-revenue-growth').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Q1-21','Q2-21','Q3-21','Q4-21','Q1-22','Q2-22','Q3-22','Q4-22',
                     'Q1-23','Q2-23','Q3-23','Q4-23','Q1-24','Q2-24','Q3-24','Q4-24',
                     'Q1-25','Q2-25','Q3-25','Q4-25'],
            datasets: [
                { label: 'Revenue ($M)',
                    data: [24,28,32,34,42,48,55,69,78,88,94,107,128,143,158,175,198,231,261,290],
                    borderColor: C.green, backgroundColor: 'rgba(34,197,94,0.04)', fill: true, borderWidth: 2, pointBackgroundColor: C.green },
                { label: 'Forecast',
                    data: [null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,null,198,231,261,290],
                    borderColor: C.green, borderDash: [5,5], borderWidth: 1.5, pointRadius: 0, spanGaps: false }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { title: { display: true, text: 'Revenue ($M)' }, grid: GRID },
                x: { grid: { display: false }, ticks: { font: { size: 9 }, maxRotation: 45 } }
            }
        }
    });
})();

(function() {
    const ctx = document.getElementById('chart-cost-breakdown').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['R&D', 'Operations', 'Manufacturing', 'Maintenance', 'Personnel', 'G&A'],
            datasets: [{ data: [31.4, 24.8, 18.3, 12.7, 8.1, 4.7],
                backgroundColor: [C.purple, C.blue, C.amber, C.red, C.green, C.teal],
                borderColor: '#1E293B', borderWidth: 2, hoverOffset: 6 }]
        },
        options: { responsive: true, cutout: '58%', plugins: { legend: { position: 'right' } } }
    });
})();


// ═══════════════════════════════════════════════════════════════
// KPI ANIMATION
// ═══════════════════════════════════════════════════════════════
function animateValue(el, start, end, duration, prefix = '', suffix = '') {
    if (!el) return;
    const t0 = performance.now();
    const isFloat = String(end).includes('.');
    function step(t) {
        const p = Math.min((t - t0) / duration, 1);
        const e = 1 - Math.pow(1 - p, 3);
        const v = start + (end - start) * e;
        el.textContent = isFloat ? prefix + v.toFixed(1) + suffix : prefix + Math.floor(v).toLocaleString() + suffix;
        if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
}

window.addEventListener('load', () => {
    animateValue(document.getElementById('val-total-flights'), 0, 2847, 1500);
    animateValue(document.getElementById('val-success-rate'), 0, 93.7, 1500, '', '%');
    animateValue(document.getElementById('val-efficiency'), 0, 0.847, 1500);

    // Scorecard bars
    document.querySelectorAll('.sc-bar').forEach(bar => {
        const w = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => { bar.style.width = w; }, 200);
    });
});


// ═══════════════════════════════════════════════════════════════
// PAGE 7: MISSION INTELLIGENCE CENTER
// ═══════════════════════════════════════════════════════════════

// Mission Timeline — horizontal bar showing recent missions color-coded by status
(function() {
    const ctx = document.getElementById('chart-mission-timeline');
    if (!ctx) return;
    const ids = ['OPS-Eclipse','OPS-Aurora','OPS-Zenith','OPS-Vortex','OPS-Titan','OPS-Nebula','OPS-Helios','OPS-Phantom','OPS-Shadow','OPS-Apex','OPS-Nova','OPS-Storm'];
    const statuses = ['Completed','Completed','Active','Completed','Aborted','Completed','Active','Completed','Delayed','Completed','Active','Completed'];
    const colors = statuses.map(s => s==='Completed'?'rgba(34,197,94,0.6)':s==='Active'?'rgba(59,130,246,0.7)':s==='Aborted'?'rgba(239,68,68,0.6)':'rgba(245,158,11,0.6)');
    const durations = [4.2,3.8,2.1,5.4,1.3,4.7,3.2,6.1,0.8,3.9,1.7,4.4];
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ids,
            datasets: [{ label: 'Duration (hrs)', data: durations, backgroundColor: colors, borderRadius: 4, borderSkipped: false }]
        },
        options: {
            responsive: true, indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: { x: { title: { display: true, text: 'Duration (hrs)' }, grid: GRID }, y: { grid: { display: false }, ticks: { font: { size: 10, family: "'JetBrains Mono', monospace" } } } }
        }
    });
})();

// Mission Status Distribution
(function() {
    const ctx = document.getElementById('chart-mission-status-dist');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Completed', 'Active', 'Scrubbed', 'Delayed', 'Aborted', 'Planning'],
            datasets: [{ data: [1847, 23, 87, 64, 167, 312], backgroundColor: [C.green, C.blue, C.slate, C.amber, C.red, C.purple], borderColor: '#1E293B', borderWidth: 2, hoverOffset: 6 }]
        },
        options: { responsive: true, cutout: '58%', plugins: { legend: { position: 'right' } } }
    });
})();

// Duration by Mission Type
(function() {
    const ctx = document.getElementById('chart-dur-by-type');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Test Flight','Endurance','Combat Sim','Recon','Cargo','Calibration'],
            datasets: [
                { label: 'Avg (hrs)', data: [3.8, 6.2, 2.4, 4.1, 5.7, 1.9], backgroundColor: 'rgba(59,130,246,0.5)', borderRadius: 4 },
                { label: 'Max (hrs)', data: [5.4, 9.8, 4.1, 6.3, 8.2, 3.1], backgroundColor: 'rgba(139,92,246,0.4)', borderRadius: 4 }
            ]
        },
        options: { responsive: true, scales: { y: { title: { display: true, text: 'Hours' }, grid: GRID }, x: { grid: { display: false } } } }
    });
})();

// Weather Impact
(function() {
    const ctx = document.getElementById('chart-weather-impact');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Clear', 'Cloudy', 'Rain', 'High Wind', 'Storm', 'Fog'],
            datasets: [
                { label: 'Flights', data: [1240, 487, 312, 198, 47, 163], backgroundColor: 'rgba(59,130,246,0.4)', borderRadius: 4, yAxisID: 'y' },
                { label: 'Success %', data: [96.8, 94.2, 89.7, 82.4, 68.1, 87.3], type: 'line', borderColor: C.green, borderWidth: 2, pointBackgroundColor: C.green, yAxisID: 'y1' }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { title: { display: true, text: 'Flights' }, grid: GRID },
                y1: { position: 'right', min: 60, max: 100, title: { display: true, text: 'Success %' }, grid: { display: false }, ticks: { callback: v => v+'%' } },
                x: { grid: { display: false } }
            }
        }
    });
})();

// Priority Breakdown
(function() {
    const ctx = document.getElementById('chart-priority-breakdown');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Critical', 'High', 'Medium', 'Low', 'Routine'],
            datasets: [{ data: [127, 384, 892, 631, 813], backgroundColor: [C.red+'90', C.orange+'90', C.amber+'90', C.blue+'90', C.slate+'90'], borderRadius: 4, borderSkipped: false }]
        },
        options: { responsive: true, indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { grid: GRID }, y: { grid: { display: false } } } }
    });
})();

// Monthly Mission Success Trend
(function() {
    const ctx = document.getElementById('chart-mission-success-trend');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: MONTHS,
            datasets: [
                { label: 'Success %', data: [94.2,93.1,89.2,94.8,95.1,96.3,93.4,95.7,94.6,93.8,91.4,92.1], borderColor: C.blue, backgroundColor: 'rgba(59,130,246,0.04)', fill: true, borderWidth: 2, pointBackgroundColor: C.blue },
                { label: 'Target', data: Array(12).fill(95), borderColor: 'rgba(34,197,94,0.4)', borderWidth: 1.5, borderDash: [5,5], pointRadius: 0 }
            ]
        },
        options: { responsive: true, scales: { y: { min: 85, max: 100, grid: GRID, ticks: { callback: v => v+'%' } }, x: { grid: { display: false } } } }
    });
})();

// Risk vs Duration Scatter
(function() {
    const ctx = document.getElementById('chart-risk-dur-scatter');
    if (!ctx) return;
    const pts = [];
    for (let i = 0; i < 60; i++) {
        const dur = 0.5 + Math.random() * 8;
        const risk = 10 + dur * 4 + (Math.random() - 0.5) * 25;
        pts.push({ x: +dur.toFixed(1), y: +Math.max(2, Math.min(90, risk)).toFixed(1) });
    }
    new Chart(ctx, {
        type: 'scatter',
        data: { datasets: [{ label: 'Missions', data: pts, backgroundColor: 'rgba(59,130,246,0.35)', borderColor: C.blue, pointRadius: 3.5 }] },
        options: { responsive: true, scales: { x: { title: { display: true, text: 'Duration (hrs)' }, grid: GRID }, y: { title: { display: true, text: 'Risk Score' }, grid: GRID } } }
    });
})();


// ═══════════════════════════════════════════════════════════════
// PAGE 8: GEOGRAPHIC INTELLIGENCE
// ═══════════════════════════════════════════════════════════════

(function() {
    const map = document.getElementById('geo-map');
    const svg = document.getElementById('geo-routes');
    const statsEl = document.getElementById('geo-stats');
    if (!map || !svg) return;

    const facilities = [
        { name: 'Houston MCC',      x: 23.6, y: 37, type: 'hq',  missions: 487, risk: 18, color: '#3B82F6' },
        { name: 'Berlin MFG',       x: 53.6, y: 22, type: 'mfg', missions: 234, risk: 21, color: '#8B5CF6' },
        { name: 'Mumbai Test',      x: 70.0, y: 40, type: 'hub', missions: 412, risk: 31, color: '#22C55E' },
        { name: 'Dubai R&D',        x: 65.3, y: 35, type: 'hub', missions: 198, risk: 24, color: '#06B6D4' },
        { name: 'Bengaluru Eng',    x: 71.4, y: 44, type: 'hub', missions: 347, risk: 28, color: '#22C55E' },
        { name: 'Singapore Hub',    x: 78.9, y: 51, type: 'hub', missions: 289, risk: 34, color: '#F59E0B' },
        { name: 'Tokyo ARC',        x: 88.6, y: 30, type: 'hub', missions: 312, risk: 22, color: '#EC4899' }
    ];

    // Draw facility markers
    facilities.forEach(f => {
        const dot = document.createElement('div');
        dot.className = `facility-dot ${f.type === 'mfg' ? 'mfg' : f.type === 'hub' ? 'hub' : ''}`;
        dot.style.left = f.x + '%';
        dot.style.top = f.y + '%';
        dot.style.background = f.color;
        dot.title = `${f.name} — ${f.missions} missions, Risk: ${f.risk}`;
        map.appendChild(dot);

        const label = document.createElement('div');
        label.className = 'facility-label';
        label.style.left = f.x + '%';
        label.style.top = f.y + '%';
        label.textContent = f.name;
        map.appendChild(label);
    });

    // Draw route curves
    const routes = [[0,2],[0,3],[2,4],[4,5],[5,6],[1,3],[0,6],[2,5],[3,4],[1,0]];
    routes.forEach(([a,b]) => {
        const f1 = facilities[a], f2 = facilities[b];
        const x1 = f1.x * 10, y1 = f1.y * 5;
        const x2 = f2.x * 10, y2 = f2.y * 5;
        const cx = (x1 + x2) / 2, cy = Math.min(y1, y2) - 30 - Math.random() * 20;
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', `M${x1},${y1} Q${cx},${cy} ${x2},${y2}`);
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke', 'rgba(59,130,246,0.12)');
        path.setAttribute('stroke-width', '1.5');
        path.setAttribute('stroke-dasharray', '4 4');
        svg.appendChild(path);
    });

    // Stats
    const stats = [
        { label: 'Total Missions', value: '2,279' },
        { label: 'Active Routes', value: '10' },
        { label: 'Avg Risk Score', value: '25.4' },
        { label: 'Flight Hours', value: '14,832' },
        { label: 'Coverage', value: '78%' },
        { label: 'Incidents (30d)', value: '12' }
    ];
    stats.forEach(s => {
        const div = document.createElement('div');
        div.className = 'geo-stat';
        div.innerHTML = `<div class="geo-stat-value">${s.value}</div><div class="geo-stat-label">${s.label}</div>`;
        statsEl.appendChild(div);
    });
})();

// Regional Operations Volume
(function() {
    const ctx = document.getElementById('chart-regional-ops');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['South Asia','Middle East','East Asia','Europe','North America'],
            datasets: [
                { label: 'Missions', data: [759, 198, 312, 234, 487], backgroundColor: [C.green+'80', C.teal+'80', C.pink+'80', C.purple+'80', C.blue+'80'], borderRadius: 4 }
            ]
        },
        options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { grid: GRID }, x: { grid: { display: false } } } }
    });
})();

// Facility Performance
(function() {
    const ctx = document.getElementById('chart-facility-perf');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Houston','Mumbai','Bengaluru','Tokyo','Singapore','Berlin','Dubai'],
            datasets: [
                { label: 'Success %', data: [96.2, 93.8, 94.7, 95.1, 91.3, 97.4, 94.9], backgroundColor: 'rgba(59,130,246,0.4)', borderRadius: 4, yAxisID: 'y' },
                { label: 'Risk Score', data: [18, 31, 28, 22, 34, 21, 24], type: 'line', borderColor: C.amber, borderWidth: 2, pointBackgroundColor: C.amber, yAxisID: 'y1' }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { min: 85, max: 100, grid: GRID, ticks: { callback: v => v+'%' } },
                y1: { position: 'right', min: 0, max: 50, grid: { display: false }, title: { display: true, text: 'Risk' } },
                x: { grid: { display: false }, ticks: { font: { size: 9 } } }
            }
        }
    });
})();


// ═══════════════════════════════════════════════════════════════
// PAGE 9: PREDICTIVE ANALYTICS
// ═══════════════════════════════════════════════════════════════

// Prediction Cards
(function() {
    const grid = document.getElementById('prediction-grid');
    if (!grid) return;

    const predictions = [
        { id:'AG-0032', prob:87, rul:8,  conf:91, model:'AG-X4', action:'Ground immediately — schedule core replacement', risk:'crit' },
        { id:'AG-0017', prob:82, rul:13, conf:88, model:'AG-X2', action:'Schedule preventive maintenance within 7 days', risk:'crit' },
        { id:'AG-0044', prob:76, rul:18, conf:84, model:'AG-X6', action:'Escalate to propulsion engineering team', risk:'crit' },
        { id:'AG-0009', prob:71, rul:24, conf:82, model:'AG-X3', action:'Schedule stabilizer actuator inspection', risk:'crit' },
        { id:'AG-0028', prob:63, rul:31, conf:79, model:'AG-X4', action:'Monitor energy grid — order replacement parts', risk:'high' },
        { id:'AG-0035', prob:54, rul:42, conf:76, model:'AG-X1', action:'Include in next scheduled maintenance window', risk:'high' },
        { id:'AG-0011', prob:41, rul:58, conf:73, model:'AG-X7', action:'Continue monitoring — low priority', risk:'med' },
        { id:'AG-0021', prob:34, rul:73, conf:71, model:'AG-X2', action:'Thermal shield inspection at next cycle', risk:'med' },
        { id:'AG-0048', prob:23, rul:94, conf:68, model:'AG-X5', action:'No action required — within safe limits', risk:'low' },
        { id:'AG-0003', prob:12, rul:147,conf:65, model:'AG-X1', action:'Nominal — next review in 60 days', risk:'low' }
    ];

    predictions.forEach(p => {
        const probCls = p.prob >= 70 ? 'high' : p.prob >= 40 ? 'med' : 'low';
        const barColor = p.prob >= 70 ? '#EF4444' : p.prob >= 40 ? '#F59E0B' : '#22C55E';
        const card = document.createElement('div');
        card.className = `pred-card risk-${p.risk}`;
        card.innerHTML = `
            <div class="pred-header">
                <span class="pred-id">${p.id}</span>
                <span class="pred-prob ${probCls}">${p.prob}%</span>
            </div>
            <div class="pred-bar-track"><div class="pred-bar-fill" style="width:${p.prob}%;background:${barColor}"></div></div>
            <div class="pred-detail">
                <span>RUL: ${p.rul} days</span>
                <span>Conf: ${p.conf}%</span>
                <span>${p.model}</span>
            </div>
            <div class="pred-action">${p.action}</div>
        `;
        grid.appendChild(card);
    });
})();

// Failure Probability Distribution
(function() {
    const ctx = document.getElementById('chart-fail-prob-dist');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['0-10%','10-20%','20-30%','30-40%','40-50%','50-60%','60-70%','70-80%','80-90%','90-100%'],
            datasets: [{
                label: 'Aircraft Count',
                data: [8, 7, 6, 5, 4, 3, 4, 5, 3, 2],
                backgroundColor: function(ctx) {
                    const i = ctx.dataIndex;
                    if (i >= 7) return 'rgba(239,68,68,0.5)';
                    if (i >= 4) return 'rgba(245,158,11,0.5)';
                    return 'rgba(34,197,94,0.5)';
                },
                borderRadius: 4
            }]
        },
        options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { title: { display: true, text: 'Aircraft' }, grid: GRID }, x: { grid: { display: false } } } }
    });
})();

// RUL Distribution
(function() {
    const ctx = document.getElementById('chart-rul-dist');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['0-15d','15-30d','30-60d','60-90d','90-120d','120-180d','180d+'],
            datasets: [{
                label: 'Aircraft',
                data: [4, 6, 8, 7, 9, 8, 5],
                backgroundColor: ['rgba(239,68,68,0.6)','rgba(249,115,22,0.5)','rgba(245,158,11,0.5)','rgba(59,130,246,0.4)','rgba(59,130,246,0.4)','rgba(34,197,94,0.4)','rgba(34,197,94,0.4)'],
                borderRadius: 4
            }]
        },
        options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { title: { display: true, text: 'Aircraft' }, grid: GRID }, x: { grid: { display: false } } } }
    });
})();

// Component Health Ranking
(function() {
    const ctx = document.getElementById('chart-comp-health-rank');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Frame','Energy Grid','Nozzle','Dampener','Thermal Shield','Stabilizer','Power Cell','Control Unit','AG Core','Processor'],
            datasets: [{ label: 'Health Score',
                data: [94.2, 91.8, 89.4, 87.1, 84.3, 82.7, 79.4, 76.8, 73.2, 68.1],
                backgroundColor: function(ctx) {
                    const v = ctx.raw;
                    if (v >= 85) return 'rgba(34,197,94,0.5)';
                    if (v >= 75) return 'rgba(245,158,11,0.5)';
                    return 'rgba(239,68,68,0.5)';
                },
                borderRadius: 4 }]
        },
        options: { responsive: true, indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { min: 50, max: 100, grid: GRID }, y: { grid: { display: false } } } }
    });
})();

// Maintenance Cost Forecast
(function() {
    const ctx = document.getElementById('chart-maint-forecast');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan-F','Feb-F','Mar-F'],
            datasets: [
                { label: 'Actual ($M)', data: [1.4,1.2,1.8,1.3,1.6,1.1,2.3,1.5,1.7,1.4,1.9,1.6,null,null,null], borderColor: C.blue, backgroundColor: 'rgba(59,130,246,0.04)', fill: true, borderWidth: 2, spanGaps: false },
                { label: 'Forecast ($M)', data: [null,null,null,null,null,null,null,null,null,null,null,1.6,1.8,2.1,1.7], borderColor: C.purple, borderDash: [5,5], borderWidth: 2, pointStyle: 'triangle', pointBackgroundColor: C.purple },
                { label: 'W/O Predictive', data: [null,null,null,null,null,null,null,null,null,null,null,1.6,2.7,3.2,2.9], borderColor: C.red, borderDash: [3,3], borderWidth: 1.5, pointRadius: 0 }
            ]
        },
        options: { responsive: true, scales: { y: { title: { display: true, text: 'Cost ($M)' }, grid: GRID }, x: { grid: { display: false } } } }
    });
})();


// ═══════════════════════════════════════════════════════════════
// PAGE 10: EXECUTIVE INSIGHTS
// ═══════════════════════════════════════════════════════════════

// Portfolio Metrics Bar
(function() {
    const bar = document.getElementById('portfolio-bar');
    if (!bar) return;
    const metrics = [
        { value: '1M+', label: 'Telemetry Records' },
        { value: '50', label: 'Aircraft Monitored' },
        { value: '2,847', label: 'Missions Tracked' },
        { value: '4,231', label: 'Maintenance Events' },
        { value: '1,247', label: 'ML Predictions' },
        { value: '287K', label: 'Manufactured Units' },
        { value: '853K', label: 'Data Points Processed' }
    ];
    metrics.forEach(m => {
        const div = document.createElement('div');
        div.className = 'port-item';
        div.innerHTML = `<div class="port-value">${m.value}</div><div class="port-label">${m.label}</div>`;
        bar.appendChild(div);
    });
})();

// AI Insight Cards
(function() {
    const grid = document.getElementById('insight-grid');
    if (!grid) return;
    const insights = [
        {
            tag: 'fleet', cls: 'warn', tagLabel: 'FLEET READINESS',
            title: 'Fleet readiness declined 2.1% MoM — AG-X4 class driving downtime',
            body: '3 AG-X4 aircraft (AG-0032, AG-0017, AG-0044) currently grounded for thermal shield replacements. Core temperature exceeded safety thresholds in 4 of 12 recent flights. Parts backlog with Northwind Composites expected to resolve by June 8.',
            impact: 'High', confidence: '92%', source: 'Telemetry + Maintenance'
        },
        {
            tag: 'ops', cls: '', tagLabel: 'MISSION OPS',
            title: 'March mission success dropped to 89.2% — weather-driven',
            body: 'Extreme weather conditions at Mumbai Test Range disrupted 12 scheduled flights. 3 missions aborted mid-flight due to wind shear above 28,000m. Recommend: Implement enhanced weather-gate criteria for monsoon pre-season (March-April).',
            impact: 'Medium', confidence: '88%', source: 'Flight Ops + Weather'
        },
        {
            tag: 'mfg', cls: 'crit', tagLabel: 'MANUFACTURING',
            title: 'Control Unit defect rate at Berlin Complex spiked to 6.4%',
            body: 'Batch B-2025-047 showed micro-fractures in 14 of 218 control units. Root cause traced to supplier tooling wear at Precision Dynamics GmbH. Production halted pending QA review. 3 affected units already installed in fleet — recall assessment underway.',
            impact: 'Critical', confidence: '95%', source: 'QA + Supply Chain'
        },
        {
            tag: 'ml', cls: 'good', tagLabel: 'PREDICTIVE MODEL',
            title: 'ML model prevented 38 unplanned failures — $12.4M cost avoidance',
            body: 'Random Forest v2.3 detected degradation patterns 13-42 days before failure in Q2. False positive rate reduced from 18% to 11% after latest retraining. Highest impact: AG-0028 energy grid micro-fracture detected 31 days early, avoiding estimated $2.1M emergency repair.',
            impact: 'Positive', confidence: '84%', source: 'ML Pipeline v2.3'
        },
        {
            tag: 'fin', cls: '', tagLabel: 'FINANCIAL',
            title: 'R&D burn rate 3.1% over budget — propulsion core optimization driving overrun',
            body: 'YTD R&D spend of $242.3M vs $235.0M budget. Overrun concentrated in propulsion engineering ($4.2M) due to accelerated AG-X6 core optimization program. ROI tracking positive: efficiency gains projected to save $18M annually in fuel costs by Q4.',
            impact: 'Medium', confidence: '91%', source: 'Finance + R&D'
        },
        {
            tag: 'ops', cls: 'good', tagLabel: 'PROPULSION',
            title: 'Propulsion efficiency improved 4.6% following Q1 optimization',
            body: 'AG-X6 class showing strongest gains (+7.2% efficiency). New core calibration profile reduced energy consumption by 340 kW average per flight hour. Recommendation: Apply optimized profile to AG-X3 and AG-X4 fleet during next maintenance cycle.',
            impact: 'Positive', confidence: '94%', source: 'Propulsion Eng.'
        }
    ];
    insights.forEach(ins => {
        const card = document.createElement('div');
        card.className = `insight-card ${ins.cls}`;
        card.innerHTML = `
            <div class="insight-tag ${ins.tag}">${ins.tagLabel}</div>
            <div class="insight-title">${ins.title}</div>
            <div class="insight-body">${ins.body}</div>
            <div class="insight-meta">
                <span>Impact: <strong>${ins.impact}</strong></span>
                <span>Confidence: <strong>${ins.confidence}</strong></span>
                <span>Source: <strong>${ins.source}</strong></span>
            </div>
        `;
        grid.appendChild(card);
    });
})();

// KPI Health Summary
(function() {
    const ctx = document.getElementById('chart-kpi-health');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Safety Compliance','Propulsion Efficiency','Mission Success','Mfg Yield','Fleet Readiness','Maint Health','Budget Adherence','Component Reliability'],
            datasets: [
                { label: 'Actual', data: [97.2, 84.7, 93.7, 95.8, 78.4, 76.3, 68.3, 91.4], backgroundColor: function(ctx) { const v = ctx.raw; return v >= 90 ? 'rgba(34,197,94,0.5)' : v >= 75 ? 'rgba(245,158,11,0.5)' : 'rgba(239,68,68,0.5)'; }, borderRadius: 4 },
                { label: 'Target', data: [95, 85, 95, 96, 85, 85, 100, 95], backgroundColor: 'rgba(148,163,184,0.15)', borderColor: 'rgba(148,163,184,0.3)', borderWidth: 1, borderRadius: 4 }
            ]
        },
        options: { responsive: true, indexAxis: 'y', scales: { x: { min: 50, max: 100, grid: GRID }, y: { grid: { display: false } } } }
    });
})();

// Operational Risk Trend
(function() {
    const ctx = document.getElementById('chart-ops-risk-trend');
    if (!ctx) return;
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: MONTHS,
            datasets: [
                { label: 'Mission Risk', data: [32,34,41,35,33,30,36,31,29,34,37,34], borderColor: C.red, borderWidth: 2, pointBackgroundColor: C.red },
                { label: 'Maintenance Risk', data: [28,26,31,27,24,22,29,25,23,27,32,28], borderColor: C.amber, borderWidth: 2, pointBackgroundColor: C.amber },
                { label: 'Financial Risk', data: [15,14,18,16,19,21,17,20,22,18,24,21], borderColor: C.purple, borderWidth: 1.5, borderDash: [4,4], pointBackgroundColor: C.purple },
                { label: 'Threshold', data: Array(12).fill(40), borderColor: 'rgba(239,68,68,0.25)', borderWidth: 1, borderDash: [8,8], pointRadius: 0 }
            ]
        },
        options: { responsive: true, scales: { y: { title: { display: true, text: 'Risk Score' }, grid: GRID }, x: { grid: { display: false } } } }
    });
})();

// Diagnostic Drill-Down Panel
(function() {
    const panel = document.getElementById('diagnostic-panel');
    if (!panel) return;
    const diagnostics = [
        { kpi: 'Fleet Readiness (78.4%)', what: 'Dropped 6.6pp below 85% target', why: '3 AG-X4 grounded for thermal shield issues; parts backlog from Northwind Composites delayed repairs by 12 days', next: 'Expected recovery to 83% by June 15 as replacement shields arrive. Full recovery to 86% by July.' },
        { kpi: 'Maintenance Health (76.3)', what: 'Below 85.0 target for 2nd consecutive month', why: 'Emergency maintenance events increased 40% due to aging AG-X3 fleet. Mean time between failures declining on aircraft >3 years old.', next: 'Predictive model flagged 4 additional aircraft. Proactive replacement should reduce emergency rate by 25% in Q3.' },
        { kpi: 'Mission Success (93.7%)', what: '1.3pp below 95% target', why: 'March weather disruptions (12 affected flights) and 2 software faults in AG-X7 flight controllers. Controllers patched in v4.2.1.', next: 'Weather-gate criteria being tightened. Forecast: 94.8% success rate in June with improved pre-flight protocols.' },
        { kpi: 'Budget Variance (+$4.7M)', what: 'Over tolerance band (±$2.0M)', why: 'Accelerated R&D spend on AG-X6 propulsion optimization ($4.2M over plan). Emergency maintenance spike added $1.8M. Offset by $1.3M manufacturing cost savings.', next: 'R&D program completing in Q3. Maintenance costs forecast to decline 34% with predictive model improvements.' },
    ];
    diagnostics.forEach(d => {
        const row = document.createElement('div');
        row.style.cssText = 'padding:12px;margin-bottom:8px;background:rgba(255,255,255,0.02);border-radius:6px;border-left:3px solid var(--accent)';
        row.innerHTML = `
            <div style="font-weight:700;color:var(--text-primary);font-size:0.82rem;margin-bottom:6px">${d.kpi}</div>
            <div style="font-size:0.7rem;color:var(--text-secondary);margin-bottom:4px"><strong style="color:var(--accent)">What happened:</strong> ${d.what}</div>
            <div style="font-size:0.7rem;color:var(--text-secondary);margin-bottom:4px"><strong style="color:var(--warning)">Why:</strong> ${d.why}</div>
            <div style="font-size:0.7rem;color:var(--text-secondary)"><strong style="color:var(--success)">What's next:</strong> ${d.next}</div>
        `;
        panel.appendChild(row);
    });
})();
