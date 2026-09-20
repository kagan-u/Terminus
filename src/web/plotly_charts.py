#!/usr/bin/env python3
"""terminus plotly interactive charts."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    print("pip install plotly")
    sys.exit(1)

from src.core import simulate, fmt_iec, sci

OUTPUT_DIR = "terminus_interactive"

def generate_interactive():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    r = simulate(16, 50, 43)
    levels = r['levels']
    
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            'Zip Size Growth',
            'File Count Explosion',
            'Compression Ratio',
            'Zip vs Output Size',
            'Growth Breakdown',
            'Scale Comparison',
        ),
        specs=[
            [{"type": "scatter"}, {"type": "scatter"}],
            [{"type": "scatter"}, {"type": "scatter"}],
            [{"type": "bar"}, {"type": "bar"}],
        ],
    )
    
    fig.add_trace(go.Scatter(
        x=[l['depth'] for l in levels],
        y=[l['zip_size'] for l in levels],
        fill='tozeroy',
        name='Zip Size',
        line=dict(color='#58a6ff', width=2),
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=[l['depth'] for l in levels],
        y=[l['files'] for l in levels],
        name='File Count',
        line=dict(color='#f85149', width=2),
    ), row=1, col=2)
    
    filtered = [l for l in levels if l['depth'] >= 3]
    fig.add_trace(go.Scatter(
        x=[l['depth'] for l in filtered],
        y=[l['ratio'] for l in filtered],
        name='Ratio',
        line=dict(color='#f0883e', width=2),
    ), row=2, col=1)
    
    fig.add_trace(go.Scatter(
        x=[l['depth'] for l in levels],
        y=[l['zip_size'] for l in levels],
        name='Zip Size (dual)',
        line=dict(color='#58a6ff', width=2),
    ), row=2, col=2)
    
    fig.add_trace(go.Scatter(
        x=[l['depth'] for l in levels],
        y=[l['uncompressed'] for l in levels],
        name='Output Size',
        yaxis='y8',
        line=dict(color='#f85149', width=2),
    ), row=2, col=2)
    
    fig.add_trace(go.Bar(
        x=['Wikipedia', 'Internet', 'Stars', 'Sand', 'Cells', 'Atoms', 'Terminus'],
        y=[20e9, 120e27, 1e24, 7.5e18, 3.7e13, 1e80, r['total_bytes']],
        name='Scale',
        marker_color=['#8b949e']*6 + ['#f85149'],
    ), row=3, col=1)
    
    zip_overhead = [l['zip_size'] - 120 for l in levels]
    payload_total = [l['uncompressed'] for l in levels]
    
    fig.add_trace(go.Bar(
        x=[l['depth'] for l in levels],
        y=zip_overhead,
        name='Zip Overhead',
    ), row=3, col=2)
    
    fig.add_trace(go.Bar(
        x=[l['depth'] for l in levels],
        y=payload_total,
        name='Payload Total',
    ), row=3, col=2)
    
    fig.update_layout(
        title='TERMINUS - Interactive Analysis',
        template='plotly_dark',
        paper_bgcolor='#0d1117',
        plot_bgcolor='#0d1117',
        height=1200,
        showlegend=True,
        legend=dict(x=0, y=1.02, orientation='h'),
    )
    
    fig.update_yaxes(type='log', row=1, col=2)
    fig.update_yaxes(type='log', row=2, col=1)
    fig.update_yaxes(type='log', row=3, col=1)
    fig.update_yaxes(type='log', row=3, col=2)
    
    fig.write_html(f'{OUTPUT_DIR}/terminus_interactive.html')
    print(f"  saved: {OUTPUT_DIR}/terminus_interactive.html")
    
    fig.write_image(f'{OUTPUT_DIR}/terminus_overview.png', width=1920, height=1200)
    print(f"  saved: {OUTPUT_DIR}/terminus_overview.png")

if __name__ == "__main__":
    print("\n  TERMINUS PLOTLY GENERATOR\n")
    generate_interactive()
