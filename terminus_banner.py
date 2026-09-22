#!/usr/bin/env python3
"""
TERMINUS BANNER
ASCII art banner generator for terminals and docs.
"""

import sys

BANNERS = {
    'terminus': r"""
████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗██╗   ██╗███████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██║   ██║██╔════╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║██║   ██║███████╗
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██║   ██║╚════██║
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝███████║
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝""",
    'ultra': r"""
 ╦╔╗╔╔╦╗╔═╗╦═╗╔═╗╔═╗╔═╗╦═╗
 ║║║║ ║ ║╣ ╠╦╝║  ╦  ║╣ ╠╦╝
 ╩╝╚╝ ╩ ╚═╝╩╚═╚═╝╚═╝╚═╝╩╚═
╔═╗╔═╗╦  ╔═╗╔═╗╦═╗╔╗╔╔═╗
╠═╣║╣ ║  ║  ║╣ ╠╦╝║║║║╣ ╩
╩ ╩╚═╝╩═╝╚═╝╚═╝╩╚═╝╚╝╚═╝ ╩""",
    'warning': r"""
╔═══════════════════════════════════════════╗
║  DO NOT EXTRACT                           ║
║  This file expands to 10^61 bytes.        ║
║  Extraction can exhaust all storage.      ║
╚═══════════════════════════════════════════╝""",
    'divider': "=" * 61,
    'wave': "-" * 61,
}


def print_banner(name='terminus', color=True):
    if name not in BANNERS:
        print(f"  unknown banner: {name}")
        print(f"  available: {', '.join(BANNERS.keys())}")
        return

    text = BANNERS[name]
    if color:
        colors = {'terminus': '\033[96m', 'ultra': '\033[93m', 'warning': '\033[91m'}
        c = colors.get(name, '')
        if c:
            print(f"{c}{text}\033[0m")
        else:
            print(text)
    else:
        print(text)


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else 'terminus'
    no_color = '--no-color' in sys.argv
    print_banner(name, not no_color)
