#!/usr/bin/env python3
"""terminus rich terminal UI."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich import box
except ImportError:
    print("pip install rich")
    sys.exit(1)

from src.core import simulate, fmt_iec, sci

console = Console()

def render_header():
    header = Text()
    header.append("TERMINUS", style="bold cyan")
    header.append("\nRecursive Zip Bomb Simulator", style="dim")
    return Panel(header, style="cyan", box=box.DOUBLE)

def render_results(r):
    table = Table(title="Results", box=box.ROUNDED, style="cyan")
    table.add_column("Metric", style="bold")
    table.add_column("Value", style="green")
    
    table.add_row("Total Files", f"{sci(r['total_files'])}")
    table.add_row("Digits", f"{int(__import__('math').log10(r['total_files'])) + 1}")
    table.add_row("Zip Size", fmt_iec(r['zip_size']))
    table.add_row("Output Size", f"{sci(r['total_bytes'])} bytes")
    table.add_row("Ratio", f"1:{sci(r['ratio'])}")
    
    return table

def render_level_table(r):
    table = Table(title="Level Details", box=box.SIMPLE_HEAVY, show_lines=True)
    table.add_column("Level", style="bold yellow")
    table.add_column("Zip Size", style="cyan")
    table.add_column("Files", style="green")
    table.add_column("Ratio", style="red")
    
    for lv in r['levels']:
        d = lv['depth']
        if d <= 5 or d % 10 == 0 or d == r['level']:
            table.add_row(
                str(d),
                fmt_iec(lv['zip_size']),
                sci(lv['files']),
                f"1:{lv['ratio']:.2e}",
            )
    
    return table

def render_chart(r):
    mx = r['levels'][-1]['zip_size']
    lines = []
    lines.append("[bold]GROWTH CHART[/bold]\n")
    
    for lv in r['levels']:
        d = lv['depth']
        if d % 10 == 0 or d == r['level']:
            sz = lv['zip_size']
            bar_len = int((sz / mx) * 40)
            
            if bar_len < 10:
                color = "green"
            elif bar_len < 25:
                color = "yellow"
            else:
                color = "red"
            
            bar = f"[{color}]{'█' * bar_len}[/{color}]"
            lines.append(f"  L{d:>2}: {fmt_iec(sz):>12} | {bar}")
    
    return Panel("\n".join(lines), title="Visualization", border_style="blue")

def run_interactive():
    console.print(render_header())
    
    console.print("\n[bold]Configuration[/bold]\n")
    
    try:
        branching = int(console.input("  Branching [16]: ").strip() or "16")
        level = int(console.input("  Level [50]: ").strip() or "50")
        payload = int(console.input("  Payload [43]: ").strip() or "43")
        payload_type = console.input("  Type [zeros]: ").strip() or "zeros"
    except (ValueError, EOFError):
        branching, level, payload, payload_type = 16, 50, 43, "zeros"
    
    branching = min(branching, 1000)
    level = min(level, 200)
    payload = min(payload, 10000)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Simulating...", total=100)
        for i in range(100):
            progress.update(task, advance=1)
    
    r = simulate(branching, level, payload, payload_type)
    
    console.print()
    console.print(render_results(r))
    console.print()
    console.print(render_level_table(r))
    console.print()
    console.print(render_chart(r))
    
    console.print("\n[dim]Simulation complete. No files were created.[/dim]\n")

if __name__ == "__main__":
    run_interactive()
