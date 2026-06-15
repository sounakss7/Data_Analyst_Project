// Global Data State
let dashboardData = null;
let activeQueryKey = null;
let charts = {};

// 1. Fetch JSON Data & Initialize Dashboard
document.addEventListener("DOMContentLoaded", () => {
    fetch("dashboard_data.json")
        .then(response => response.json())
        .then(data => {
            dashboardData = data;
            initTabs();
            populateKPIs();
            renderCharts();
            populateImpactTable();
            initSQLConsole();
            renderReport();
        })
        .catch(error => {
            console.error("Error loading dashboard data:", error);
            document.querySelectorAll(".kpi-value").forEach(el => el.textContent = "Error");
        });
});

// 2. Tab Navigation System
function initTabs() {
    const navButtons = document.querySelectorAll(".nav-btn");
    const tabContents = document.querySelectorAll(".tab-content");
    const pageTitle = document.getElementById("page-title");
    const pageSubtitle = document.getElementById("page-subtitle");

    const headerDetails = {
        "overview-tab": { title: "Executive Overview", subtitle: "High-level operational metrics and growth trends" },
        "programs-tab": { title: "Program Performance", subtitle: "Operational execution, volunteer mobilization, and completion details" },
        "finance-tab": { title: "Financial Analytics", subtitle: "Funds utilization ratios and sponsor donation distributions" },
        "impact-tab": { title: "Impact Assessment", subtitle: "Regional efficiency analysis and state rankings" },
        "sql-tab": { title: "SQL Query Sandbox Console", subtitle: "Execute analytical queries directly against the relational database" },
        "reports-tab": { title: "Automated Report Engine", subtitle: "Data-driven quarterly and monthly briefs for management" }
    };

    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            // Remove active states
            navButtons.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));

            // Set active tab
            btn.classList.add("active");
            const targetId = btn.getAttribute("data-target");
            document.getElementById(targetId).classList.add("active");

            // Update Header titles
            const info = headerDetails[targetId];
            if (info) {
                pageTitle.textContent = info.title;
                pageSubtitle.textContent = info.subtitle;
            }

            // Redraw charts if needed (resizes nicely inside flexible containers)
            Object.values(charts).forEach(chart => chart.resize());
        });
    });
}

// 3. Populate KPI Values
function populateKPIs() {
    const kpis = dashboardData.kpis;
    
    // Overview KPIs
    document.getElementById("kpi-beneficiaries").textContent = kpis.total_beneficiaries.toLocaleString();
    document.getElementById("kpi-completion").textContent = kpis.completion_rate.toFixed(1) + "%";
    document.getElementById("kpi-funds").textContent = (kpis.total_utilized / 1e6).toFixed(2) + "M INR";
    document.getElementById("kpi-satisfaction").textContent = kpis.avg_satisfaction.toFixed(2) + " / 5";

    // Programs KPIs
    document.getElementById("kpi-attendance").textContent = kpis.avg_attendance.toFixed(1) + "%";
    document.getElementById("kpi-volunteers").textContent = kpis.total_volunteers.toLocaleString();
    document.getElementById("kpi-jobs").textContent = kpis.employment_rate.toFixed(1) + "%";
}

// 4. Render All Visual Charts
function renderCharts() {
    // A. Growth Trend Chart
    const ctxGrowth = document.getElementById("growthChart").getContext("2d");
    
    // Group monthly growth data into quarterly summary for cleaner rendering in browser
    const labels = [];
    const values = [];
    // Select every 3rd month or render yearly totals
    for (let i = 0; i < dashboardData.growth.labels.length; i += 3) {
        labels.push(dashboardData.growth.labels[i]);
        values.push(dashboardData.growth.values[i]);
    }
    
    charts.growth = new Chart(ctxGrowth, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Enrolled Beneficiaries",
                data: values,
                borderColor: "#FF5722",
                backgroundColor: "rgba(255, 87, 34, 0.05)",
                fill: true,
                borderWidth: 2,
                tension: 0.3,
                pointBackgroundColor: "#FF5722"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#9FAFC0" } },
                y: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#9FAFC0" } }
            }
        }
    });

    // B. Category Shares Donut
    const ctxCat = document.getElementById("categoryChart").getContext("2d");
    charts.category = new Chart(ctxCat, {
        type: "doughnut",
        data: {
            labels: dashboardData.program.labels,
            datasets: [{
                data: dashboardData.program.values,
                backgroundColor: ["#FF5722", "#1E88E5", "#FFC107", "#4CAF50", "#9C27B0"],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { color: "#9FAFC0", padding: 12, boxWidth: 12 }
                }
            }
        }
    });

    // C. State completion stacked horizontal bars
    const ctxState = document.getElementById("stateChart").getContext("2d");
    charts.state = new Chart(ctxState, {
        type: "bar",
        data: {
            labels: dashboardData.state_completion.labels,
            datasets: [
                {
                    label: "Completed",
                    data: dashboardData.state_completion.completed,
                    backgroundColor: "#4CAF50"
                },
                {
                    label: "Dropped Out",
                    data: dashboardData.state_completion.dropped,
                    backgroundColor: "#F44336"
                },
                {
                    label: "Ongoing",
                    data: dashboardData.state_completion.ongoing,
                    backgroundColor: "#FFC107"
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: "y",
            plugins: {
                legend: { position: "bottom", labels: { color: "#9FAFC0", boxWidth: 12 } }
            },
            scales: {
                x: { stacked: true, grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#9FAFC0" } },
                y: { stacked: true, grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#9FAFC0" } }
            }
        }
    });

    // D. Vocational Employment Conversion Chart
    const ctxEmp = document.getElementById("employmentChart").getContext("2d");
    charts.employment = new Chart(ctxEmp, {
        type: "bar",
        data: {
            labels: dashboardData.jobs.labels,
            datasets: [
                {
                    label: "Employed",
                    data: dashboardData.jobs.employed,
                    backgroundColor: "#4CAF50"
                },
                {
                    label: "No Livelihood",
                    data: dashboardData.jobs.unemployed,
                    backgroundColor: "#F44336"
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom", labels: { color: "#9FAFC0", boxWidth: 12 } }
            },
            scales: {
                x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#9FAFC0" } },
                y: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#9FAFC0" } }
            }
        }
    });

    // E. Funds Allocated vs Utilized Chart
    const ctxFunds = document.getElementById("fundsChart").getContext("2d");
    charts.funds = new Chart(ctxFunds, {
        type: "bar",
        data: {
            labels: dashboardData.funds.labels,
            datasets: [
                {
                    label: "Allocated Budget",
                    data: dashboardData.funds.allocated,
                    backgroundColor: "#1E88E5"
                },
                {
                    label: "Utilized Spend",
                    data: dashboardData.funds.utilized,
                    backgroundColor: "#FF5722"
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom", labels: { color: "#9FAFC0", boxWidth: 12 } }
            },
            scales: {
                x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#9FAFC0" } },
                y: { 
                    grid: { color: "rgba(255, 255, 255, 0.05)" }, 
                    ticks: { 
                        color: "#9FAFC0",
                        callback: function(value) { return (value / 1e6).toFixed(1) + 'M'; }
                    } 
                }
            }
        }
    });

    // F. Donor Sponsorship Pie
    const ctxDonor = document.getElementById("donorChart").getContext("2d");
    charts.donor = new Chart(ctxDonor, {
        type: "pie",
        data: {
            labels: dashboardData.donor.labels,
            datasets: [{
                data: dashboardData.donor.values,
                backgroundColor: ["#1E88E5", "#FFC107", "#4CAF50", "#9C27B0"],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { color: "#9FAFC0", padding: 12, boxWidth: 12 }
                }
            }
        }
    });
}

// 5. Populate Regional Impact Rankings (Query 5 Output)
function populateImpactTable() {
    const tableBody = document.querySelector("#impact-table tbody");
    tableBody.innerHTML = "";
    
    // We fetch the pre-computed dataset for Query 5 (State-wise operational performance)
    const stateRankings = dashboardData.queries.query_5.result;
    
    stateRankings.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${row.state}</strong></td>
            <td>${row.total_enrolled.toLocaleString()}</td>
            <td>${row.completion_rate_pct.toFixed(2)}%</td>
            <td><span class="badge">${row.completion_rank}</span></td>
            <td>${row.employment_success_pct.toFixed(2)}%</td>
            <td><span class="badge" style="background-color:rgba(76, 175, 80, 0.1); color:#4CAF50; border-color:rgba(76, 175, 80, 0.2);">${row.employment_rank}</span></td>
        `;
        tableBody.appendChild(tr);
    });
}

// 6. SQL Query Sandbox Controller
function initSQLConsole() {
    const btnContainer = document.getElementById("query-buttons-container");
    const codeBlock = document.getElementById("sql-code-block");
    const runBtn = document.getElementById("run-sql-btn");
    const statusText = document.getElementById("sql-status");
    const tableContainer = document.getElementById("sql-table-container");

    const queryTitles = {
        "query_1": "1. Executive KPIs Overview",
        "query_2": "2. Category Performance Summary",
        "query_3": "3. Budget Efficiency Audit",
        "query_4": "4. Donor Segmentation Shares",
        "query_5": "5. State Efficacy Rankings",
        "query_6": "6. YoY Operations Growth"
    };

    // Populate Query Buttons
    Object.keys(dashboardData.queries).forEach((qKey, idx) => {
        const btn = document.createElement("button");
        btn.className = "query-item-btn";
        if (idx === 0) {
            btn.classList.add("active");
            activeQueryKey = qKey;
            codeBlock.textContent = dashboardData.queries[qKey].sql;
        }
        btn.textContent = queryTitles[qKey] || qKey.replace("_", " ").toUpperCase();
        btn.addEventListener("click", () => {
            document.querySelectorAll(".query-item-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            activeQueryKey = qKey;
            codeBlock.textContent = dashboardData.queries[qKey].sql;
            tableContainer.innerHTML = `<p class="placeholder-text">Execute the query to view rows...</p>`;
            statusText.textContent = "Ready";
            statusText.style.color = "var(--text-secondary)";
        });
        btnContainer.appendChild(btn);
    });

    // Run Button Action (Simulated loader for realistic DB audit experience)
    runBtn.addEventListener("click", () => {
        if (!activeQueryKey) return;
        
        statusText.textContent = "Running query...";
        statusText.style.color = "var(--warning-color)";
        tableContainer.innerHTML = `<div class="loader"></div>`;
        
        setTimeout(() => {
            renderSQLResult(dashboardData.queries[activeQueryKey]);
        }, 500);
    });
}

// Helper to render output of query selection
function renderSQLResult(queryData) {
    const tableContainer = document.getElementById("sql-table-container");
    const statusText = document.getElementById("sql-status");
    const rows = queryData.result;
    
    if (rows.length === 0) {
        tableContainer.innerHTML = `<p class="placeholder-text">Query executed successfully. 0 rows returned.</p>`;
        statusText.textContent = "Success (0 rows, 4ms)";
        statusText.style.color = "var(--success-color)";
        return;
    }
    
    // Extract headers
    const cols = Object.keys(rows[0]);
    
    // Build table HTML
    let tableHtml = `<table class="data-table"><thead><tr>`;
    cols.forEach(col => {
        tableHtml += `<th>${col}</th>`;
    });
    tableHtml += `</tr></thead><tbody>`;
    
    rows.forEach(row => {
        tableHtml += `<tr>`;
        cols.forEach(col => {
            let val = row[col];
            if (typeof val === "number" && !Number.isInteger(val)) {
                val = val.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            } else if (typeof val === "number") {
                val = val.toLocaleString();
            }
            tableHtml += `<td>${val === null ? 'NULL' : val}</td>`;
        });
        tableHtml += `</tr>`;
    });
    tableHtml += `</tbody></table>`;
    
    tableContainer.innerHTML = tableHtml;
    statusText.textContent = `Success (${rows.length} rows, 12ms)`;
    statusText.style.color = "var(--success-color)";
}

// 7. Render Automated Markdown Reports
function renderReport() {
    const reportBody = document.getElementById("report-body");
    const reportMd = dashboardData.report_md;
    
    if (!reportMd) {
        reportBody.innerHTML = `<p class="placeholder-text">No reports available.</p>`;
        return;
    }
    
    // Use marked to parse MD text into standard structured HTML
    reportBody.innerHTML = marked.parse(reportMd);
}
