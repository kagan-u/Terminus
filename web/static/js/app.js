async function runSimulation() {
    const config = {
        branching: parseInt(document.getElementById('branching').value) || 16,
        level: parseInt(document.getElementById('level').value) || 50,
        payload: parseInt(document.getElementById('payload').value) || 43,
        payload_type: document.getElementById('payload_type').value,
    };

    document.getElementById('simulate-btn').textContent = 'SIMULATING...';
    document.getElementById('simulate-btn').disabled = true;

    try {
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config),
        });
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Simulation error:', error);
        alert('Simulation failed. Check console for details.');
    } finally {
        document.getElementById('simulate-btn').textContent = 'SIMULATE';
        document.getElementById('simulate-btn').disabled = false;
    }
}

function displayResults(data) {
    document.getElementById('results').style.display = 'block';

    document.getElementById('total-files').textContent = data.results.total_files_sci;
    document.getElementById('total-files-sci').textContent = `${data.results.total_files_digits} digits`;
    document.getElementById('zip-size').textContent = data.results.zip_size_human;
    document.getElementById('output-size').textContent = `${data.results.total_bytes.toExponential(2)} bytes`;
    document.getElementById('ratio').textContent = `1:${data.results.ratio_sci}`;

    const levels = data.levels;

    // zip size chart
    Plotly.newPlot('chart-zip-size', [{
        x: levels.map(l => l.depth),
        y: levels.map(l => l.zip_size),
        type: 'scatter',
        mode: 'lines+markers',
        fill: 'tozeroy',
        line: { color: '#58a6ff', width: 2 },
        fillcolor: 'rgba(88, 166, 255, 0.3)',
    }], {
        title: { text: 'Zip Size Growth', font: { color: '#e6edf3' } },
        paper_bgcolor: '#0d1117',
        plot_bgcolor: '#0d1117',
        xaxis: { title: 'Level', color: '#8b949e', gridcolor: '#30363d' },
        yaxis: { title: 'Size (bytes)', color: '#8b949e', gridcolor: '#30363d' },
        margin: { t: 50, b: 50, l: 60, r: 20 },
    }, { responsive: true });

    // file count chart (log)
    Plotly.newPlot('chart-file-count', [{
        x: levels.map(l => l.depth),
        y: levels.map(l => l.files),
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#f85149', width: 2 },
    }], {
        title: { text: 'File Count (Log Scale)', font: { color: '#e6edf3' } },
        paper_bgcolor: '#0d1117',
        plot_bgcolor: '#0d1117',
        xaxis: { title: 'Level', color: '#8b949e', gridcolor: '#30363d' },
        yaxis: { title: 'Files', color: '#8b949e', gridcolor: '#30363d', type: 'log' },
        margin: { t: 50, b: 50, l: 60, r: 20 },
    }, { responsive: true });

    // ratio chart (log)
    const filtered = levels.filter(l => l.depth >= 3);
    Plotly.newPlot('chart-ratio', [{
        x: filtered.map(l => l.depth),
        y: filtered.map(l => l.ratio),
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#f0883e', width: 2 },
    }], {
        title: { text: 'Compression Ratio (Log Scale)', font: { color: '#e6edf3' } },
        paper_bgcolor: '#0d1117',
        plot_bgcolor: '#0d1117',
        xaxis: { title: 'Level', color: '#8b949e', gridcolor: '#30363d' },
        yaxis: { title: 'Ratio', color: '#8b949e', gridcolor: '#30363d', type: 'log' },
        margin: { t: 50, b: 50, l: 60, r: 20 },
    }, { responsive: true });

    // comparison bar chart
    const refs = ['Wikipedia', 'Internet', 'Stars', 'Sand', 'Cells', 'Atoms'];
    const refSizes = [20e9, 120e27, 1e24, 7.5e18, 3.7e13, 1e80];
    const terminusSize = data.results.total_bytes;

    Plotly.newPlot('chart-comparison', [{
        x: [...refs, 'Terminus'],
        y: [...refSizes, terminusSize],
        type: 'bar',
        marker: {
            color: ['#8b949e', '#8b949e', '#8b949e', '#8b949e', '#8b949e', '#8b949e', '#f85149'],
        },
    }], {
        title: { text: 'Scale Comparison', font: { color: '#e6edf3' } },
        paper_bgcolor: '#0d1117',
        plot_bgcolor: '#0d1117',
        xaxis: { color: '#8b949e' },
        yaxis: { title: 'Bytes', color: '#8b949e', gridcolor: '#30363d', type: 'log' },
        margin: { t: 50, b: 80, l: 60, r: 20 },
    }, { responsive: true });

    // table
    const tbody = document.querySelector('#level-table tbody');
    tbody.innerHTML = '';
    const visibleLevels = levels.filter(l => l.depth <= 5 || l.depth % 10 === 0 || l.depth === data.config.level);
    visibleLevels.forEach(l => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${l.depth}</td>
            <td>${l.zip_size_human}</td>
            <td>${l.files_sci}</td>
            <td>1:${l.ratio_sci}</td>
        `;
        tbody.appendChild(row);
    });

    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}
