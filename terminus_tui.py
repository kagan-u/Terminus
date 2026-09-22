#!/usr/bin/env python3
"""
TERMINUS TUI
interactive terminal interface using curses.
"""

import curses
import sys
import os
import math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.core import simulate, fmt_iec, sci


class TerminusTUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.branching = 16
        self.level = 50
        self.payload = 43
        self.cursor = 0
        self.fields = ['branching', 'level', 'payload']
        self.running = True
        self.result = None

    def draw(self):
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        # title
        title = " TERMINUS TUI "
        self.stdscr.addstr(0, (w - len(title)) // 2, title, curses.A_REVERSE)

        # config box
        y = 2
        self.stdscr.addstr(y, 2, "CONFIGURATION", curses.A_BOLD | curses.A_UNDERLINE)
        y += 1

        values = [str(self.branching), str(self.level), str(self.payload)]
        for i, field in enumerate(self.fields):
            marker = ">" if i == self.cursor else " "
            attr = curses.A_REVERSE if i == self.cursor else curses.A_NORMAL
            self.stdscr.addstr(y + i, 4, f" {marker} {field:<12}: {values[i]:>8} ", attr)

        y += len(self.fields) + 1
        self.stdscr.addstr(y, 4, " [Enter] simulate   [Up/Down] select   [+/-] change   [q] quit")
        y += 2

        # results
        if self.result:
            r = self.result
            self.stdscr.addstr(y, 2, "RESULTS", curses.A_BOLD | curses.A_UNDERLINE)
            y += 1
            lines = [
                f"  Total Files : {sci(r['total_files'])}",
                f"  Zip Size    : {fmt_iec(r['zip_size'])}",
                f"  Output Size : {sci(r['total_bytes'])} bytes",
                f"  Ratio       : 1:{sci(r['ratio'])}",
                "",
                "  LEVEL TABLE",
                f"  {'Lvl':>4} {'Zip':>12} {'Files':>14} {'Ratio':>14}",
                "  " + "-" * 48,
            ]
            for lv in r['levels']:
                d = lv['depth']
                if d <= 3 or d % 10 == 0 or d == r['level']:
                    lines.append(
                        f"  {d:>4} {fmt_iec(lv['zip_size']):>12} {sci(lv['files']):>14} 1:{lv['ratio']:.2e}"
                    )

            for line in lines:
                if y < h - 1:
                    self.stdscr.addstr(y, 2, line[:w - 4])
                    y += 1

            # bar chart
            y += 1
            if y < h - 3:
                self.stdscr.addstr(y, 2, "  ZIP GROWTH", curses.A_BOLD)
                y += 1
                mx = r['levels'][-1]['zip_size']
                for lv in r['levels']:
                    d = lv['depth']
                    if (d % 10 == 0 or d == r['level']) and y < h - 1:
                        bar = int((lv['zip_size'] / mx) * (w - 20))
                        self.stdscr.addstr(y, 4, f"L{d:>2}: " + "#" * max(bar, 1))
                        y += 1

        self.stdscr.refresh()

    def run(self):
        curses.curs_set(0)
        self.stdscr.keypad(True)

        while self.running:
            self.draw()
            key = self.stdscr.getch()

            if key in (ord('q'), ord('Q')):
                self.running = False
            elif key == curses.KEY_UP:
                self.cursor = (self.cursor - 1) % len(self.fields)
            elif key == curses.KEY_DOWN:
                self.cursor = (self.cursor + 1) % len(self.fields)
            elif key in (ord('+'), ord('=')):
                self.adjust(1)
            elif key == ord('-'):
                self.adjust(-1)
            elif key == ord('\n'):
                self.result = simulate(self.branching, self.level, self.payload)

    def adjust(self, delta):
        if self.fields[self.cursor] == 'branching':
            self.branching = max(2, min(1000, self.branching + delta * (2 if delta > 0 else 1)))
            if delta > 0:
                steps = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1000]
                self.branching = next((s for s in steps if s > self.branching), 1000)
            else:
                steps = [1000, 512, 256, 128, 64, 32, 16, 8, 4, 2]
                self.branching = next((s for s in steps if s < self.branching), 2)
        elif self.fields[self.cursor] == 'level':
            self.level = max(1, min(200, self.level + delta * 5))
        elif self.fields[self.cursor] == 'payload':
            steps = [1, 2, 4, 8, 16, 32, 43, 64, 128, 256, 512, 1024, 4096, 10000]
            if delta > 0:
                self.payload = next((s for s in steps if s > self.payload), 10000)
            else:
                self.payload = next((s for s in reversed(steps) if s < self.payload), 1)


def main():
    curses.wrapper(lambda stdscr: TerminusTUI(stdscr).run())


if __name__ == "__main__":
    main()
