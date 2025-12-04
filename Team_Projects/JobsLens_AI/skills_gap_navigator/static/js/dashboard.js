// Global Digital Skills Gap Navigator - Dashboard
// Simplified and robust version

// Global data storage
const appData = {
    predictions: null,
    featureImportance: null,
    haiRaw: null
};

// Risk configuration
const RISK_CONFIG = {
    0: { label: 'Ready', color: '#10b981' },
    1: { label: 'Emerging', color: '#3b82f6' },
    2: { label: 'High', color: '#f59e0b' },
    3: { label: 'Critical', color: '#dc2626' }
};

// Sample HAI data structure for when CSV fails to load
const SAMPLE_COUNTRIES = ['United States', 'China', 'United Kingdom', 'Germany', 'France',
                          'Japan', 'Canada', 'India', 'South Korea', 'Australia'];

// Load all data
async function loadData() {
    console.log('Loading data...');

    try {
        // Load predictions (required)
        const predResponse = await fetch('/visualizations/data/country_predictions.json');
        if (!predResponse.ok) throw new Error('Failed to load predictions');
        appData.predictions = await predResponse.json();
        console.log('✓ Predictions loaded:', appData.predictions.length);

        // Load feature importance (required)
        const impResponse = await fetch('/visualizations/data/feature_importance.json');
        if (!impResponse.ok) throw new Error('Failed to load feature importance');
        appData.featureImportance = await impResponse.json();
        console.log('✓ Feature importance loaded:', appData.featureImportance.length);

        // Update stats
        updateStatistics();

        return true;
    } catch (error) {
        console.error('Error loading data:', error);
        showError('Failed to load model data. Please ensure the model has been trained.');
        return false;
    }
}

// Update statistics from loaded data
function updateStatistics() {
    const riskCounts = { 0: 0, 1: 0, 2: 0, 3: 0 };
    appData.predictions.forEach(p => {
        if (p.prediction !== undefined) {
            riskCounts[p.prediction]++;
        }
    });

    document.getElementById('critical-count').textContent = riskCounts[3] || 0;
    document.getElementById('high-count').textContent = riskCounts[2] || 0;
}

// Show error message
function showError(message) {
    const containers = ['world-map', 'feature-importance', 'risk-distribution',
                       'publications-chart', 'investment-chart', 'country-detail'];

    containers.forEach(id => {
        const elem = document.getElementById(id);
        if (elem) {
            elem.innerHTML = `<div style="text-align:center; padding:40px; color:#dc2626;">
                <p style="font-size:1.2em; margin-bottom:10px;">⚠️ ${message}</p>
                <p style="color:#6b7280; font-size:0.9em;">Check the browser console for details</p>
            </div>`;
        }
    });
}

// Initialize dashboard
async function init() {
    console.log('🚀 Initializing dashboard...');

    const loaded = await loadData();
    if (!loaded) return;

    // Create all visualizations
    try {
        createWorldMap();
        createFeatureImportance();
        createRiskDistribution();
        createTopRiskCountries();

        // Populate dropdowns
        populateDropdowns();

        // Setup event listeners
        setupEventListeners();

        console.log('✓ Dashboard initialized successfully');
    } catch (error) {
        console.error('Error initializing visualizations:', error);
        showError('Error creating visualizations: ' + error.message);
    }
}

// Create world map
function createWorldMap() {
    console.log('Creating world map...');

    const countries = appData.predictions.map(p => p.country);
    const riskLevels = appData.predictions.map(p => p.prediction || 3);
    const riskLabels = riskLevels.map(r => RISK_CONFIG[r].label);

    const trace = {
        type: 'choropleth',
        locationmode: 'country names',
        locations: countries,
        z: riskLevels,
        text: countries.map((c, i) => `${c}<br>${riskLabels[i]} Risk`),
        hovertemplate: '<b>%{location}</b><br>%{text}<extra></extra>',
        colorscale: [
            [0, '#10b981'],
            [0.33, '#3b82f6'],
            [0.66, '#f59e0b'],
            [1, '#dc2626']
        ],
        showscale: true,
        colorbar: {
            title: 'Risk Level',
            tickvals: [0, 1, 2, 3],
            ticktext: ['Ready', 'Emerging', 'High', 'Critical'],
            len: 0.5
        },
        marker: {
            line: {
                color: '#e5e7eb',
                width: 0.5
            }
        }
    };

    const layout = {
        geo: {
            projection: { type: 'natural earth' },
            showframe: false,
            showcoastlines: true,
            coastlinecolor: '#d1d5db',
            landcolor: '#f9fafb',
            showcountries: true,
            countrycolor: '#e5e7eb',
            bgcolor: 'white'
        },
        margin: { l: 0, r: 0, t: 0, b: 0 },
        paper_bgcolor: 'white',
        height: 500
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['lasso2d', 'select2d'],
        displaylogo: false
    };

    Plotly.newPlot('world-map', [trace], layout, config);
    console.log('✓ World map created');
}

// Create feature importance chart
function createFeatureImportance() {
    console.log('Creating feature importance chart...');

    const topFeatures = appData.featureImportance.slice(0, 15);

    const trace = {
        type: 'bar',
        x: topFeatures.map(f => f.importance).reverse(),
        y: topFeatures.map(f => formatFeatureName(f.feature)).reverse(),
        orientation: 'h',
        marker: {
            color: topFeatures.map((f, i) => {
                const ratio = i / topFeatures.length;
                return `rgba(102, 126, 234, ${0.5 + ratio * 0.5})`;
            }).reverse(),
            line: { color: '#764ba2', width: 1 }
        },
        hovertemplate: '<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>'
    };

    const layout = {
        margin: { l: 200, r: 20, t: 20, b: 50 },
        paper_bgcolor: 'white',
        plot_bgcolor: 'white',
        font: { family: 'inherit', size: 12, color: '#1f2937' },
        xaxis: {
            title: 'Feature Importance',
            gridcolor: '#f3f4f6',
            color: '#6b7280'
        },
        yaxis: {
            gridcolor: '#f3f4f6',
            color: '#1f2937'
        },
        height: 400
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false
    };

    Plotly.newPlot('feature-importance', [trace], layout, config);
    console.log('✓ Feature importance chart created');
}

// Create risk distribution
function createRiskDistribution() {
    console.log('Creating risk distribution chart...');

    const riskCounts = { 0: 0, 1: 0, 2: 0, 3: 0 };
    appData.predictions.forEach(p => {
        if (p.prediction !== undefined) {
            riskCounts[p.prediction]++;
        }
    });

    const categories = Object.keys(riskCounts).map(k => RISK_CONFIG[k].label);
    const values = Object.values(riskCounts);
    const colors = Object.keys(riskCounts).map(k => RISK_CONFIG[k].color);

    const trace = {
        type: 'bar',
        x: categories,
        y: values,
        marker: {
            color: colors,
            line: { color: '#ffffff', width: 2 }
        },
        text: values.map(v => v.toString()),
        textposition: 'outside',
        textfont: { size: 14, color: '#1f2937', weight: 'bold' },
        hovertemplate: '<b>%{x}</b><br>Countries: %{y}<extra></extra>'
    };

    const layout = {
        margin: { l: 50, r: 20, t: 40, b: 80 },
        paper_bgcolor: 'white',
        plot_bgcolor: 'white',
        font: { family: 'inherit', color: '#1f2937' },
        xaxis: {
            title: { text: 'Risk Category', font: { size: 14, color: '#4b5563' } },
            gridcolor: '#f3f4f6',
            color: '#6b7280'
        },
        yaxis: {
            title: { text: 'Number of Countries', font: { size: 14, color: '#4b5563' } },
            gridcolor: '#f3f4f6',
            color: '#6b7280'
        },
        height: 400
    };

    const config = {
        responsive: true,
        displayModeBar: false
    };

    Plotly.newPlot('risk-distribution', [trace], layout, config);
    console.log('✓ Risk distribution chart created');
}

// Create top risk countries list
function createTopRiskCountries() {
    console.log('Creating top risk countries list...');

    const ranked = appData.predictions
        .filter(p => p.prediction !== undefined && p.prediction_proba)
        .sort((a, b) => b.prediction - a.prediction || b.prediction_proba[b.prediction] - a.prediction_proba[a.prediction])
        .slice(0, 10);

    const html = `
        <ol style="color: #4b5563; line-height: 2.2; font-size: 1.05em; margin-left: 20px;">
            ${ranked.map((p, i) => {
                const riskLevel = p.prediction || 3;
                const riskInfo = RISK_CONFIG[riskLevel];
                const confidence = p.prediction_proba && p.prediction_proba[riskLevel]
                    ? (p.prediction_proba[riskLevel] * 100).toFixed(1)
                    : 'N/A';

                return `
                    <li style="margin-bottom: 8px;">
                        <strong style="color: #1f2937;">${p.country}</strong>
                        <span class="badge ${riskInfo.label.toLowerCase()}" style="margin-left: 10px;">${riskInfo.label} Risk</span>
                        <span style="color: #9ca3af; margin-left: 10px;">— Confidence: ${confidence}%</span>
                    </li>
                `;
            }).join('')}
        </ol>
    `;

    document.getElementById('top-risk-countries').innerHTML = html;
    console.log('✓ Top risk countries list created');
}

// Create country detail view
function createCountryDetail(country) {
    console.log('Creating country detail for:', country);

    const prediction = appData.predictions.find(p => p.country === country);

    if (!prediction || !prediction.features || prediction.features.length === 0) {
        document.getElementById('country-detail').innerHTML = `
            <div style="text-align:center; padding:50px; color:#9ca3af;">
                <p style="font-size:1.1em;">No detailed prediction data available for ${country}</p>
                <p style="margin-top:10px; font-size:0.9em;">This country may not be in the test set</p>
            </div>
        `;
        return;
    }

    const topFeatures = prediction.features
        .sort((a, b) => Math.abs(b.contribution) - Math.abs(a.contribution))
        .slice(0, 15);

    const trace = {
        type: 'bar',
        x: topFeatures.map(f => f.contribution).reverse(),
        y: topFeatures.map(f => formatFeatureName(f.name)).reverse(),
        orientation: 'h',
        marker: {
            color: topFeatures.map(f => f.contribution > 0 ? '#dc2626' : '#10b981').reverse(),
            line: { color: '#ffffff', width: 1 }
        },
        hovertemplate: '<b>%{y}</b><br>Contribution: %{x:.4f}<extra></extra>'
    };

    const riskInfo = RISK_CONFIG[prediction.prediction || 3];
    const confidence = prediction.prediction_proba && prediction.prediction_proba[prediction.prediction]
        ? (prediction.prediction_proba[prediction.prediction] * 100).toFixed(1)
        : 'N/A';

    const layout = {
        margin: { l: 200, r: 20, t: 60, b: 70 },
        paper_bgcolor: 'white',
        plot_bgcolor: 'white',
        font: { family: 'inherit', size: 12, color: '#1f2937' },
        xaxis: {
            title: {
                text: 'Contribution to Risk Score<br><span style="font-size:0.85em; color:#6b7280;">Red = Increases Risk | Green = Decreases Risk</span>',
                font: { size: 13, color: '#4b5563' }
            },
            gridcolor: '#f3f4f6',
            color: '#6b7280',
            zeroline: true,
            zerolinecolor: '#9ca3af',
            zerolinewidth: 2
        },
        yaxis: {
            gridcolor: '#f3f4f6',
            color: '#1f2937'
        },
        title: {
            text: `<b>${country}</b> — <span style="color:${riskInfo.color};">${riskInfo.label} Risk</span> (${confidence}% confidence)`,
            font: { size: 16, color: '#1f2937' },
            x: 0.5,
            xanchor: 'center'
        },
        height: 500
    };

    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false
    };

    Plotly.newPlot('country-detail', [trace], layout, config);
    console.log('✓ Country detail created');
}

// Populate dropdowns
function populateDropdowns() {
    console.log('Populating dropdowns...');

    const countries = appData.predictions
        .map(p => p.country)
        .sort();

    // Country detail dropdown
    const detailSelect = document.getElementById('country-detail-select');
    if (detailSelect) {
        detailSelect.innerHTML = '<option value="">Select a country...</option>';
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.textContent = country;
            detailSelect.appendChild(option);
        });
    }

    // Publications and investment dropdowns (simplified)
    ['pub-country-select', 'invest-country-select'].forEach(id => {
        const select = document.getElementById(id);
        if (select) {
            select.innerHTML = '<option value="all">All Countries (Top 10)</option>';
            SAMPLE_COUNTRIES.forEach(country => {
                const option = document.createElement('option');
                option.value = country;
                option.textContent = country;
                select.appendChild(option);
            });
        }
    });

    console.log('✓ Dropdowns populated');
}

// Setup event listeners
function setupEventListeners() {
    console.log('Setting up event listeners...');

    const detailSelect = document.getElementById('country-detail-select');
    if (detailSelect) {
        detailSelect.addEventListener('change', (e) => {
            if (e.target.value) {
                createCountryDetail(e.target.value);
            } else {
                document.getElementById('country-detail').innerHTML = `
                    <div style="text-align:center; padding:50px; color:#9ca3af;">
                        <p>Select a country to see detailed risk breakdown</p>
                    </div>
                `;
            }
        });
    }

    // Simplified handlers for pub and invest (show message)
    ['pub-country-select', 'invest-country-select'].forEach(id => {
        const select = document.getElementById(id);
        if (select) {
            select.addEventListener('change', (e) => {
                const chartId = id.includes('pub') ? 'publications-chart' : 'investment-chart';
                const chartName = id.includes('pub') ? 'Publications' : 'Investment';
                document.getElementById(chartId).innerHTML = `
                    <div style="text-align:center; padding:50px; color:#6b7280;">
                        <p style="font-size:1.1em; margin-bottom:10px;">${chartName} trends for ${e.target.value}</p>
                        <p style="font-size:0.9em;">Feature available in advanced dashboard</p>
                        <p style="margin-top:20px;">
                            <a href="/advanced" style="color:#667eea; text-decoration:none; font-weight:600;">
                                → View Advanced Dashboard
                            </a>
                        </p>
                    </div>
                `;
            });
        }
    });

    console.log('✓ Event listeners set up');
}

// Utility: Format feature names
function formatFeatureName(name) {
    return name
        .replace(/_/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ')
        .replace(/Ai /gi, 'AI ')
        .replace(/Pct/gi, '%')
        .replace(/Yoy/gi, 'YoY')
        .replace(/3y/gi, '3-Year');
}

// Initialize on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

console.log('Dashboard script loaded');
