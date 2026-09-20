#!/usr/bin/env python3
"""terminus cli entry point."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from src.core import simulate, fmt_iec, sci

def main():
    parser = argparse.ArgumentParser(
        prog='terminus',
        description='Terminus - Recursive Zip Bomb Simulator',
    )
    subparsers = parser.add_subparsers(dest='command', help='commands')
    
    sim_parser = subparsers.add_parser('simulate', help='run simulation')
    sim_parser.add_argument('-b', '--branching', type=int, default=16, help='branching factor')
    sim_parser.add_argument('-l', '--level', type=int, default=50, help='depth level')
    sim_parser.add_argument('-p', '--payload', type=int, default=43, help='payload size')
    sim_parser.add_argument('-t', '--type', default='zeros', help='payload type')
    
    chart_parser = subparsers.add_parser('chart', help='generate charts')
    chart_parser.add_argument('-o', '--output', default='terminus_charts', help='output directory')
    
    args = parser.parse_args()
    
    if args.command == 'simulate':
        r = simulate(args.branching, args.level, args.payload, args.type)
        print(f"\n  TERMINUS SIMULATION")
        print(f"  {'='*40}")
        print(f"  Branching:  {r['branching']}")
        print(f"  Level:      {r['level']}")
        print(f"  Payload:    {r['payload']} bytes ({r['payload_type']})")
        print(f"  {'='*40}")
        print(f"  Total Files: {sci(r['total_files'])}")
        print(f"  Zip Size:    {fmt_iec(r['zip_size'])}")
        print(f"  Output Size: {sci(r['total_bytes'])} bytes")
        print(f"  Ratio:       1:{sci(r['ratio'])}")
        print(f"  {'='*40}\n")
    
    elif args.command == 'chart':
        from terminus_graph import generate_all
        generate_all()
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
