function runSimulation() {
    const branching = parseInt(document.getElementById('branching').value) || 16;
    const level = parseInt(document.getElementById('level').value) || 50;
    const payload = parseInt(document.getElementById('payload').value) || 43;

    document.getElementById('simulate-btn').textContent = 'SIMULATING...';
    document.getElementById('simulate-btn').disabled = true;

    setTimeout(() => {
        const sim = new TerminusSimulator(branching, level, payload);
        const result = sim.simulate();
        displayResults(result);
        document.getElementById('simulate-btn').textContent = 'SIMULATE';
        document.getElementById('simulate-btn').disabled = false;
    }, 100);
}

function displayResults(data) {
    document.getElementById('results').style.display = 'block';

    document.getElementById('total-files').textContent = TerminusSimulator.sci(data.results.totalFiles);
    document.getElementById('total-files-digits').textContent = `${Math.floor(Math.log10(data.results.totalFiles)) + 1} digits`;
    document.getElementById('zip-size').textContent = TerminusSimulator.fmtIEC(data.results.zipSize);
    document.getElementById('output-size').textContent = `${data.results.totalBytes.toExponential(2)} bytes`;
    document.getElementById('ratio').textContent = `1:${data.results.ratio.toExponential(2)}`;

    const levels = data.levels;

    Plotly.newPlot('chart-zip-size', [{
        x: levels.map(l => l.depth),
        y: levels.map(l => l.zipSize),
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

    const filtered = levels.filter(l => l.depth >= 3);
    Plotly.newPlot('chart-ratio', [{
        x: filtered.map(l => l.depth),
        y: filtered.map(l => l.ratio),
        type: 'scatter',
        mode: 'lines+markers',
        line: { color: '#f0883e', width: 2 },
    }], {
        title: { text: 'Compression Ratio (Log)', font: { color: '#e6edf3' } },
        paper_bgcolor: '#0d1117',
        plot_bgcolor: '#0d1117',
        xaxis: { title: 'Level', color: '#8b949e', gridcolor: '#30363d' },
        yaxis: { title: 'Ratio', color: '#8b949e', gridcolor: '#30363d', type: 'log' },
        margin: { t: 50, b: 50, l: 60, r: 20 },
    }, { responsive: true });

    const refs = ['Wikipedia', 'Internet', 'Stars', 'Sand', 'Cells', 'Atoms', 'Terminus'];
    const refSizes = [20e9, 120e27, 1e24, 7.5e18, 3.7e13, 1e80, data.results.totalBytes];

    Plotly.newPlot('chart-comparison', [{
        x: refs,
        y: refSizes,
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

    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}
