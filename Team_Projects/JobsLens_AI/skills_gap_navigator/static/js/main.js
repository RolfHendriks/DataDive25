// Global Digital Skills Gap Navigator - Main Application

// Global state
const appState = {
    countries: null,
    featureImportance: null,
    shapeFunctions: null,
    predictions: null,
    selectedCountry: null,
    filters: {
        riskLevels: [0, 1, 2, 3],
        region: 'all'
    }
};

// Risk level configuration
const RISK_CONFIG = {
    0: { label: 'Ready', color: '#00d4ff' },
    1: { label: 'Emerging', color: '#00ff88' },
    2: { label: 'High', color: '#ffaa00' },
    3: { label: 'Critical', color: '#ff0055' }
};

// Load all data
async function loadData() {
    try {
        const basePath = '../visualizations/data/';

        const [importance, shapes, predictions] = await Promise.all([
            fetch(basePath + 'feature_importance.json').then(r => r.json()),
            fetch(basePath + 'shape_functions.json').then(r => r.json()),
            fetch(basePath + 'country_predictions.json').then(r => r.json())
        ]);

        appState.featureImportance = importance;
        appState.shapeFunctions = shapes;
        appState.predictions = predictions;

        console.log('✓ Data loaded successfully');
        console.log(`  Countries: ${predictions.length}`);
        console.log(`  Features: ${importance.length}`);

        return true;
    } catch (error) {
        console.error('Error loading data:', error);
        alert('Error loading model data. Please ensure the model has been trained.');
        return false;
    }
}

// Initialize application
async function init() {
    console.log('Initializing Global Digital Skills Gap Navigator...');

    // Load data
    const loaded = await loadData();
    if (!loaded) {
        document.getElementById('loading-overlay').classList.add('hidden');
        return;
    }

    // Initialize visualizations
    initFeatureImportance();
    initShapeFunctions();
    initMap();

    // Initialize controls
    initControls();

    // Hide loading overlay
    setTimeout(() => {
        document.getElementById('loading-overlay').classList.add('hidden');
    }, 500);

    console.log('✓ Application initialized');
}

// Initialize feature importance chart
function initFeatureImportance() {
    const data = appState.featureImportance.slice(0, 15); // Top 15

    const trace = {
        type: 'bar',
        y: data.map(d => d.feature).reverse(),
        x: data.map(d => d.importance).reverse(),
        orientation: 'h',
        marker: {
            color: data.map((d, i) => {
                const ratio = i / data.length;
                return `rgba(0, ${Math.floor(212 + 43 * ratio)}, ${Math.floor(255 - 155 * ratio)}, 0.8)`;
            }).reverse(),
            line: {
                color: '#00d4ff',
                width: 1
            }
        },
        hovertemplate: '<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>'
    };

    const layout = {
        margin: { l: 200, r: 20, t: 20, b: 50 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {
            family: 'Inter, sans-serif',
            color: '#a0a8d4',
            size: 11
        },
        xaxis: {
            title: 'Feature Importance',
            gridcolor: 'rgba(0, 212, 255, 0.1)',
            color: '#a0a8d4'
        },
        yaxis: {
            gridcolor: 'rgba(0, 212, 255, 0.1)',
            color: '#a0a8d4'
        },
        hoverlabel: {
            bgcolor: '#1a2038',
            bordercolor: '#00d4ff',
            font: { color: '#ffffff' }
        }
    };

    const config = {
        responsive: true,
        displayModeBar: false
    };

    Plotly.newPlot('feature-importance', [trace], layout, config);
}

// Initialize shape functions
function initShapeFunctions() {
    const select = document.getElementById('shape-feature-select');
    select.innerHTML = '';

    // Populate dropdown
    Object.keys(appState.shapeFunctions).forEach(feature => {
        const option = document.createElement('option');
        option.value = feature;
        option.textContent = feature.replace(/_/g, ' ').toUpperCase();
        select.appendChild(option);
    });

    // Set first feature as default
    if (select.options.length > 0) {
        select.selectedIndex = 0;
        updateShapeFunction(select.value);
    }

    // Event listener
    select.addEventListener('change', (e) => {
        updateShapeFunction(e.target.value);
    });
}

function updateShapeFunction(featureName) {
    const shapeData = appState.shapeFunctions[featureName];
    if (!shapeData) return;

    const trace = {
        type: 'scatter',
        mode: 'lines+markers',
        x: shapeData.feature_values,
        y: shapeData.scores,
        line: {
            color: '#00d4ff',
            width: 3,
            shape: 'spline'
        },
        marker: {
            color: '#ff0055',
            size: 6,
            line: { color: '#ffffff', width: 1 }
        },
        hovertemplate: '<b>' + featureName + '</b><br>Value: %{x}<br>Effect: %{y:.4f}<extra></extra>'
    };

    const layout = {
        margin: { l: 60, r: 40, t: 40, b: 60 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {
            family: 'Inter, sans-serif',
            color: '#a0a8d4'
        },
        xaxis: {
            title: featureName.replace(/_/g, ' ').toUpperCase(),
            gridcolor: 'rgba(0, 212, 255, 0.1)',
            color: '#a0a8d4'
        },
        yaxis: {
            title: 'Effect on Prediction',
            gridcolor: 'rgba(0, 212, 255, 0.1)',
            color: '#a0a8d4',
            zeroline: true,
            zerolinecolor: 'rgba(255, 0, 85, 0.3)',
            zerolinewidth: 2
        },
        title: {
            text: 'Marginal Effect Curve',
            font: { color: '#00d4ff', size: 14 },
            x: 0.5,
            xanchor: 'center'
        },
        hoverlabel: {
            bgcolor: '#1a2038',
            bordercolor: '#00d4ff',
            font: { color: '#ffffff' }
        }
    };

    const config = {
        responsive: true,
        displayModeBar: false
    };

    Plotly.newPlot('shape-functions', [trace], layout, config);
}

// Initialize map (simplified - using Plotly choropleth)
function initMap() {
    // Create country-to-risk mapping
    const countryRisk = {};
    appState.predictions.forEach(pred => {
        countryRisk[pred.country] = pred.prediction;
    });

    // Use ISO-3 country codes for choropleth
    const countries = appState.predictions.map(p => p.country);
    const riskLevels = appState.predictions.map(p => p.prediction);
    const riskLabels = riskLevels.map(r => RISK_CONFIG[r].label);

    const trace = {
        type: 'choropleth',
        locationmode: 'country names',
        locations: countries,
        z: riskLevels,
        text: countries.map((c, i) => `${c}<br>${riskLabels[i]} Risk`),
        hovertemplate: '<b>%{location}</b><br>%{text}<extra></extra>',
        colorscale: [
            [0, '#00d4ff'],
            [0.33, '#00ff88'],
            [0.66, '#ffaa00'],
            [1, '#ff0055']
        ],
        showscale: false,
        marker: {
            line: {
                color: '#0a0e27',
                width: 0.5
            }
        }
    };

    const layout = {
        geo: {
            projection: {
                type: 'natural earth'
            },
            bgcolor: 'rgba(0,0,0,0)',
            lakecolor: 'rgba(0,0,0,0)',
            landcolor: 'rgba(26, 32, 56, 0.3)',
            coastlinecolor: 'rgba(0, 212, 255, 0.2)',
            showcountries: true,
            countrycolor: 'rgba(0, 212, 255, 0.2)',
            showlakes: false,
            showrivers: false
        },
        margin: { l: 0, r: 0, t: 0, b: 0 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        dragmode: false
    };

    const config = {
        responsive: true,
        displayModeBar: false
    };

    Plotly.newPlot('world-map', [trace], layout, config);

    // Add click handler
    document.getElementById('world-map').on('plotly_click', (data) => {
        if (data.points && data.points[0]) {
            const countryName = data.points[0].location;
            selectCountry(countryName);
        }
    });
}

// Select country and update waterfall
function selectCountry(countryName) {
    const pred = appState.predictions.find(p => p.country === countryName);
    if (!pred) {
        console.warn('No prediction found for:', countryName);
        return;
    }

    appState.selectedCountry = pred;

    // Update waterfall plot
    updateWaterfallPlot(pred);

    // Update selected info
    const infoDiv = document.getElementById('selected-country');
    const riskConfig = RISK_CONFIG[pred.prediction];
    infoDiv.innerHTML = `
        <h3 style="color: ${riskConfig.color};">${countryName}</h3>
        <p><strong>Risk Level:</strong> ${riskConfig.label}</p>
        <p><strong>Confidence:</strong> ${(pred.prediction_proba[pred.prediction] * 100).toFixed(1)}%</p>
    `;
    infoDiv.classList.add('active');

    // Update title
    document.getElementById('waterfall-title').textContent = `${countryName} Breakdown`;
}

// Update waterfall plot
function updateWaterfallPlot(pred) {
    if (!pred || !pred.features) {
        document.getElementById('waterfall-plot').innerHTML =
            '<p style="text-align:center; color: #6b7299;">Click a country on the map to see breakdown</p>';
        return;
    }

    // Get top contributing features (positive and negative)
    const features = pred.features
        .sort((a, b) => Math.abs(b.contribution) - Math.abs(a.contribution))
        .slice(0, 10);

    const names = features.map(f => f.name);
    const contributions = features.map(f => f.contribution);
    const colors = contributions.map(c =>
        c > 0 ? '#ff0055' : '#00ff88'
    );

    const trace = {
        type: 'bar',
        y: names.reverse(),
        x: contributions.reverse(),
        orientation: 'h',
        marker: {
            color: colors.reverse(),
            line: {
                color: '#ffffff',
                width: 1
            }
        },
        hovertemplate: '<b>%{y}</b><br>Contribution: %{x:.4f}<extra></extra>'
    };

    const layout = {
        margin: { l: 150, r: 20, t: 20, b: 50 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {
            family: 'Inter, sans-serif',
            color: '#a0a8d4',
            size: 11
        },
        xaxis: {
            title: 'Contribution to Risk',
            gridcolor: 'rgba(0, 212, 255, 0.1)',
            color: '#a0a8d4',
            zeroline: true,
            zerolinecolor: 'rgba(255, 255, 255, 0.2)',
            zerolinewidth: 2
        },
        yaxis: {
            gridcolor: 'rgba(0, 212, 255, 0.1)',
            color: '#a0a8d4'
        },
        hoverlabel: {
            bgcolor: '#1a2038',
            bordercolor: '#00d4ff',
            font: { color: '#ffffff' }
        },
        annotations: [{
            text: 'Red = Increases Risk | Green = Decreases Risk',
            xref: 'paper',
            yref: 'paper',
            x: 0.5,
            y: -0.15,
            showarrow: false,
            font: { size: 10, color: '#6b7299' }
        }]
    };

    const config = {
        responsive: true,
        displayModeBar: false
    };

    Plotly.newPlot('waterfall-plot', [trace], layout, config);
}

// Initialize controls
function initControls() {
    // Risk level filters
    document.querySelectorAll('.risk-filter').forEach(checkbox => {
        checkbox.addEventListener('change', updateFilters);
    });

    // Region filter
    const regionSelect = document.getElementById('region-filter');
    regionSelect.addEventListener('change', updateFilters);

    // Reset button
    document.getElementById('reset-filters').addEventListener('click', resetFilters);

    // Initialize default waterfall message
    document.getElementById('waterfall-plot').innerHTML =
        '<p style="text-align:center; color: #6b7299; padding: 50px;">Click a country on the map to see its feature breakdown</p>';
}

function updateFilters() {
    // Update risk level filters
    appState.filters.riskLevels = Array.from(
        document.querySelectorAll('.risk-filter:checked')
    ).map(cb => parseInt(cb.value));

    // Update region filter
    appState.filters.region = document.getElementById('region-filter').value;

    // Re-render visualizations with filters
    console.log('Filters updated:', appState.filters);
    // TODO: Implement filtering logic
}

function resetFilters() {
    document.querySelectorAll('.risk-filter').forEach(cb => cb.checked = true);
    document.getElementById('region-filter').value = 'all';
    updateFilters();
}

// Initialize on load
window.addEventListener('DOMContentLoaded', init);
