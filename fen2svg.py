#!/usr/bin/env python3
#
# Copyright 2021 Gerry Sumner Hayes
# Chess pieces from Colin M.L. Burnett, licensed under the GPL.
#
# The goal is to generate a compact SVG (since a chess book may contain hundreds of board SVGs)
# from a specified FEN string.
#
# FEN is described at https://en.wikipedia.org/wiki/Forsyth%%E2%%80%%93Edwards_Notation
# as an example, run:
#
# fen2svg.py rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR -o output.svg
#
import argparse
import sys


parser = argparse.ArgumentParser("Generate an SVG image of a chess board based on a FEN string.", 
    epilog="""Chess pieces from SVGs by Colin M.L. Burnett https://en.wikipedia.org/wiki/User:Cburnett

This work is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or any later version. This work is distributed in the hope that it will be useful, but without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. See version 2 and version 3 of the GNU General Public License for more details. https://www.gnu.org/licenses/old-licenses/gpl-2.0.html""")

parser.add_argument("--template-file", default=None)
parser.add_argument("--output", "-o", default=None)
parser.add_argument("--force", "-f", help="Overwrite existing files", action="store_true")
parser.add_argument("--dark-color", default="#bbb", help="Color to use for the dark squares (default: #bbb)")
parser.add_argument("--light-color", default="#fff", help="Color to use for the dark squares (default: #fff)")
parser.add_argument("fen", help="FEN for a board position: e.g. 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/' for a starting position. https://en.wikipedia.org/wiki/Forsyth%%E2%%80%%93Edwards_Notation Truncated FENs are allowed, and slashes are optional.", default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/', nargs='?')

args = parser.parse_args()

svgTemplate = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="800" height="800" viewBox="0 0 800 800" version="1.1" id="chessboard" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svg="http://www.w3.org/2000/svg" style="fill:{dark_color};stroke:none" >
  <defs id="defs2" />
  <rect style="fill:{light_color};stroke-width:0" id="board" width="810" height="810" x="-5" y="-5" />
  <rect id="b8" width="100" height="100" x="100" y="0" />
  <rect id="d8" width="100" height="100" x="300" y="0" />
  <rect id="f8" width="100" height="100" x="500" y="0" />
  <rect id="h8" width="100" height="100" x="700" y="0" />
  <rect id="a7" width="100" height="100" x="0" y="100" />
  <rect id="c7" width="100" height="100" x="200" y="100" />
  <rect id="e7" width="100" height="100" x="400" y="100" />
  <rect id="g7" width="100" height="100" x="600" y="100" />
  <rect id="b6" width="100" height="100" x="100" y="200" />
  <rect id="d6" width="100" height="100" x="300" y="200" />
  <rect id="f6" width="100" height="100" x="500" y="200" />
  <rect id="h6" width="100" height="100" x="700" y="200" />
  <rect id="a5" width="100" height="100" x="0" y="300" />
  <rect id="c5" width="100" height="100" x="200" y="300" />
  <rect id="e5" width="100" height="100" x="400" y="300" />
  <rect id="g5" width="100" height="100" x="600" y="300" />
  <rect id="b4" width="100" height="100" x="100" y="400" />
  <rect id="d4" width="100" height="100" x="300" y="400" />
  <rect id="f4" width="100" height="100" x="500" y="400" />
  <rect id="h4" width="100" height="100" x="700" y="400" />
  <rect id="a3" width="100" height="100" x="0" y="500" />
  <rect id="c3" width="100" height="100" x="200" y="500" />
  <rect id="e3" width="100" height="100" x="400" y="500" />
  <rect id="g3" width="100" height="100" x="600" y="500" />
  <rect id="b2" width="100" height="100" x="100" y="600" />
  <rect id="d2" width="100" height="100" x="300" y="600" />
  <rect id="f2" width="100" height="100" x="500" y="600" />
  <rect id="h2" width="100" height="100" x="700" y="600" />
  <rect id="a1" width="100" height="100" x="0" y="700" />
  <rect id="c1" width="100" height="100" x="200" y="700" />
  <rect id="e1" width="100" height="100" x="400" y="700" />
  <rect id="g1" width="100" height="100" x="600" y="700" />
  {pieces}
</svg>
"""

pieceAnchors = {
}

# Adjustments to appropriately center the pieces in their respective squares; the pawns are defined
# slightly differently from the pieces
pieceOffsets = {
        "bb": (0, -1.28),
        "bk": (0, -3.15),
        "bn": (0, -1.67),
        "bp": (50, 17.2),
        "bq": (0, -2),
        "br": (0, -1.69),
        "wb": (0, -1.28),
        "wk": (0, -3.15),
        "wn": (0, -1.67),
        "wp": (50, 17.2),
        "wq": (0, -2),
        "wr": (0, -1.69),
}

#
# Templates retrieved from https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces; licensed
# under the GPL.
#
pieceTemplates = {
    "bb": """<g style="fill:none;fill-rule:evenodd;stroke:#000;stroke-width:1.5;stroke-linejoin:round;" transform="matrix(2.22,0,0,2.22,%.2f,%.2f)" id="bb"> <g style="fill:#000;stroke-linecap:butt" id="g1061"> <path d="m 9,36 c 3.39,-0.97 10.11,0.43 13.5,-2 3.39,2.43 10.11,1.03 13.5,2 0,0 1.65,0.54 3,2 -0.68,0.97 -1.65,0.99 -3,0.5 -3.39,-0.97 -10.11,0.46 -13.5,-1 C 19.11,38.96 12.39,37.53 9,38.5 7.65,38.99 6.68,38.97 6,38 7.35,36.54 9,36 9,36 Z" id="p1055" /> <path d="m 15,32 c 2.5,2.5 12.5,2.5 15,0 0.5,-1.5 0,-2 0,-2 0,-2.5 -2.5,-4 -2.5,-4 5.5,-1.5 6,-11.5 -5,-15.5 -11,4 -10.5,14 -5,15.5 0,0 -2.5,1.5 -2.5,4 0,0 -0.5,0.5 0,2 z" id="p1057" /> <path d="m 25,8 a 2.5,2.5 0 1 1 -5,0 2.5,2.5 0 1 1 5,0 z" id="p1059" /> </g> <path d="m 17.5,26 h 10 M 15,30 H 30 M 22.5,15.5 v 5 M 20,18 h 5" style="stroke:#fff;stroke-linejoin:miter" id="p1063" /> </g>""",
    "bk": """<g style="fill:none;fill-rule:evenodd;stroke:#000;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" id="bk" transform="matrix(2.22,0,0,2.22,%.2f,%.2f)"> <path d="M 22.5,11.63 V 6" id="p6570" /> <path d="m 22.5,25 c 0,0 4.5,-7.5 3,-10.5 0,0 -1,-2.5 -3,-2.5 -2,0 -3,2.5 -3,2.5 -1.5,3 3,10.5 3,10.5" style="fill:#000;stroke-linecap:butt" id="p1129" /> <path d="m 12.5,37 c 5.5,3.5 14.5,3.5 20,0 v -7 c 0,0 9,-4.5 6,-10.5 -4,-6.5 -13.5,-3.5 -16,4 V 27 23.5 C 20,16 10.5,13 6.5,19.5 c -3,6 6,10.5 6,10.5 v 7" style="fill:#000" id="p1131" /> <path d="m 20,8 h 5" id="p1133" /> <path d="m 32,29.5 c 0,0 8.5,-4 6.03,-9.65 C 34.15,14 25,18 22.5,24.5 v 2.1 -2.1 C 20,18 10.85,14 6.97,19.85 4.5,25.5 13,29.5 13,29.5" style="stroke-linejoin:round;stroke:#fff" id="p1135" /> <path d="m 12.5,30 c 5.5,-3 14.5,-3 20,0 m -20,3.5 c 5.5,-3 14.5,-3 20,0 m -20,3.5 c 5.5,-3 14.5,-3 20,0" style="stroke:#fff;stroke-linejoin:round" id="p1137" /> </g>""",
    "bn": """<g style="opacity:1;fill:none;fill-opacity:1;fill-rule:evenodd;stroke:#000;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" transform="matrix(2.22,0,0,2.22,%.2f,%.2f)" id="bn"> <path d="m 22,10 c 10.5,1 16.5,8 16,29 H 15 c 0,-9 10,-6.5 8,-21" style="fill:#000" id="p1202" /> <path d="m 24,18 c 0.38,2.91 -5.55,7.37 -8,9 -3,2 -2.82,4.34 -5,4 -1.042,-0.94 1.41,-3.04 0,-3 -1,0 0.19,1.23 -1,2 -1,0 -4.003,1 -4,-4 0,-2 6,-12 6,-12 0,0 1.89,-1.9 2,-3.5 -0.73,-0.994 -0.5,-2 -0.5,-3 1,-1 3,2.5 3,2.5 h 2 c 0,0 0.78,-1.992 2.5,-3 1,0 1,3 1,3" style="fill:#000" id="p1204" /> <path d="m 9.5,25.5 a 0.5,0.5 0 1 1 -1,0 0.5,0.5 0 1 1 1,0 z" style="fill:#fff;stroke:#fff" id="p1206" /> <path d="m 15,15.5 a 0.5,1.5 0 1 1 -1,0 0.5,1.5 0 1 1 1,0 z" transform="matrix(0.866,0.5,-0.5,0.866,9.693,-5.173)" style="fill:#fff;stroke:#fff" id="p1208" /> <path d="M 24.55,10.4 24.1,11.85 24.6,12 c 3.15,1 5.65,2.49 7.9,6.75 2.25,4.26 3.25,10.31 2.75,20.25 l -0.05,0.5 h 2.25 L 37.5,39 C 38,28.94 36.62,22.15 34.25,17.66 31.88,13.17 28.46,11.02 25.06,10.5 Z" style="fill:#fff;stroke:none" id="p1210" /> </g>""",
    "bp": """<path d="m %.2f,%.2f c -4.91,0 -8.89,3.98 -8.89,8.89 0,1.98 0.64,3.8 1.73,5.29 -4.33,2.49 -7.29,7.13 -7.29,12.49 0,4.51 2.09,8.53 5.36,11.18 -6.67,2.36 -16.47,12.33 -16.47,29.93 h 51.11 c 0,-17.6 -9.8,-27.58 -16.47,-29.93 3.27,-2.64 5.36,-6.67 5.36,-11.18 0,-5.36 -2.96,-10 -7.29,-12.49 1.09,-1.49 1.73,-3.31 1.73,-5.29 0,-4.91 -3.98,-8.89 -8.89,-8.89 z" style="fill:#000;fill-rule:nonzero;stroke:#000;stroke-width:3.33;stroke-linecap:round;stroke-linejoin:miter" id="bp" />""",
    "bq": """<g style="fill:#000;stroke:#000;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round" id="bq" transform="matrix(2.22,0,0,2.22,%.2f,%.2f)"> <path d="m 9,26 c 8.5,-1.5 21,-1.5 27,0 L 38.5,13.5 31,25 30.7,10.9 25.5,24.5 22.5,10 19.5,24.5 14.3,10.9 14,25 6.5,13.5 Z" style="fill:#000;stroke-linecap:butt" id="p1341" /> <path d="m 9,26 c 0,2 1.5,2 2.5,4 1,1.5 1,1 0.5,3.5 -1.5,1 -1,2.5 -1,2.5 -1.5,1.5 0,2.5 0,2.5 6.5,1 16.5,1 23,0 0,0 1.5,-1 0,-2.5 0,0 0.5,-1.5 -1,-2.5 -0.5,-2.5 -0.5,-2 0.5,-3.5 1,-2 2.5,-2 2.5,-4 -8.5,-1.5 -18.5,-1.5 -27,0 z" id="p1343" /> <path d="M 11.5,30 C 15,29 30,29 33.5,30" id="p1345" /> <path d="m 12,33.5 c 6,-1 15,-1 21,0" id="p1347" /> <circle cx="6" cy="12" r="2" id="c1349" /> <circle cx="14" cy="9" r="2" id="c1351" /> <circle cx="22.5" cy="8" r="2" id="c1353" /> <circle cx="31" cy="9" r="2" id="c1355" /> <circle cx="39" cy="12" r="2" id="c1357" /> <path d="m 11,38.5 a 35,35 1 0 0 23,0" style="fill:none;stroke:#000;stroke-linecap:butt" id="p1359" /> <g style="fill:none;stroke:#fff" id="g1369"> <path d="m 11,29 a 35,35 1 0 1 23,0" id="p1361" /> <path d="m 12.5,31.5 h 20" id="p1363" /> <path d="m 11.5,34.5 a 35,35 1 0 0 22,0" id="p1365" /> <path d="m 10.5,37.5 a 35,35 1 0 0 24,0" id="p1367" /> </g> </g>""",
    "br": """<g style="fill:#000;fill-rule:evenodd;stroke:#000;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4" transform="matrix(2.22,0,0,2.22,%.2f,%.2f)" id="br"> <path d="M 9,39 H 36 V 36 H 9 Z" style="stroke-linecap:butt" id="p1455" /> <path d="M 12.5,32 14,29.5 h 17 l 1.5,2.5 z" style="stroke-linecap:butt" id="p1457" /> <path d="m 12,36 v -4 h 21 v 4 z" style="stroke-linecap:butt" id="p1459" /> <path d="m 14,29.5 v -13 h 17 v 13 z" style="stroke-linecap:butt;stroke-linejoin:miter" id="p1461" /> <path d="M 14,16.5 11,14 h 23 l -3,2.5 z" style="stroke-linecap:butt" id="p1463" /> <path d="M 11,14 V 9 h 4 v 2 h 5 V 9 h 5 v 2 h 5 V 9 h 4 v 5 z" style="stroke-linecap:butt" id="p1465" /> <path d="m 12,35.5 h 21 v 0" style="fill:none;stroke:#fff;stroke-width:1" id="p1467" /> <path d="M 13,31.5 H 32" style="fill:none;stroke:#fff;stroke-width:1;stroke-linejoin:miter" id="p1469" /> <path d="M 14,29.5 H 31" style="fill:none;stroke:#fff;stroke-width:1;stroke-linejoin:miter" id="p1471" /> <path d="M 14,16.5 H 31" style="fill:none;stroke:#fff;stroke-width:1;stroke-linejoin:miter" id="p1473" /> <path d="M 11,14 H 34" style="fill:none;stroke:#fff;stroke-width:1;stroke-linejoin:miter" id="p1475" /> </g>""",
    "wb": """<g style="fill:none;fill-rule:evenodd;stroke:#000;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:4" transform="matrix(2.22,0,0,2.22,%.2f,%.2f)" id="wb"> <g style="fill:#fff;stroke-linecap:butt" id="g1551"> <path d="m 9,36 c 3.39,-0.97 10.11,0.43 13.5,-2 3.39,2.43 10.11,1.03 13.5,2 0,0 1.65,0.54 3,2 -0.68,0.97 -1.65,0.99 -3,0.5 -3.39,-0.97 -10.11,0.46 -13.5,-1 C 19.11,38.96 12.39,37.53 9,38.5 7.65,38.99 6.68,38.97 6,38 7.35,36.54 9,36 9,36 Z" id="p1545" /> <path d="m 15,32 c 2.5,2.5 12.5,2.5 15,0 0.5,-1.5 0,-2 0,-2 0,-2.5 -2.5,-4 -2.5,-4 5.5,-1.5 6,-11.5 -5,-15.5 -11,4 -10.5,14 -5,15.5 0,0 -2.5,1.5 -2.5,4 0,0 -0.5,0.5 0,2 z" id="p1547" /> <path d="m 25,8 a 2.5,2.5 0 1 1 -5,0 2.5,2.5 0 1 1 5,0 z" id="p1549" /> </g> <path d="m 17.5,26 h 10 M 15,30 H 30 M 22.5,15.5 v 5 M 20,18 h 5" style="fill:none;stroke-linejoin:miter" id="p1553" /> </g>""",
    "wk": """<g style="fill:none;fill-rule:evenodd;stroke:#000;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round" id="wk" transform="matrix(2.22,0,0,2.22,%.2f,%.2f)"> <path d="M 22.5,11.63 V 6" style="stroke-linejoin:miter" id="p1621" /> <path d="m 20,8 h 5" style="stroke-linejoin:miter" id="p1623" /> <path d="m 22.5,25 c 0,0 4.5,-7.5 3,-10.5 0,0 -1,-2.5 -3,-2.5 -2,0 -3,2.5 -3,2.5 -1.5,3 3,10.5 3,10.5" style="fill:#fff;stroke-linecap:butt;stroke-linejoin:miter" id="p1625" /> <path d="m 12.5,37 c 5.5,3.5 14.5,3.5 20,0 v -7 c 0,0 9,-4.5 6,-10.5 -4,-6.5 -13.5,-3.5 -16,4 V 27 23.5 C 20,16 10.5,13 6.5,19.5 c -3,6 6,10.5 6,10.5 v 7" style="fill:#fff" id="p1627" /> <path d="M 12.5,30 C 18,27 27,27 32.5,30" id="p1629" /> <path d="m 12.5,33.5 c 5.5,-3 14.5,-3 20,0" id="p1631" /> <path d="M 12.5,37 C 18,34 27,34 32.5,37" id="p1633" /> </g>""",
    "wn": """<g style="fill:none;fill-rule:evenodd;stroke:#000;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round" transform="matrix(2.22,0,0,2.22,%.2f,%.2f)" id="wn"> <path d="m 22,10 c 10.5,1 16.5,8 16,29 H 15 c 0,-9 10,-6.5 8,-21" style="fill:#fff" id="p1697" /> <path d="m 24,18 c 0.38,2.91 -5.55,7.37 -8,9 -3,2 -2.82,4.34 -5,4 -1.042,-0.94 1.41,-3.04 0,-3 -1,0 0.19,1.23 -1,2 -1,0 -4.003,1 -4,-4 0,-2 6,-12 6,-12 0,0 1.89,-1.9 2,-3.5 -0.73,-0.994 -0.5,-2 -0.5,-3 1,-1 3,2.5 3,2.5 h 2 c 0,0 0.78,-1.992 2.5,-3 1,0 1,3 1,3" style="fill:#fff" id="p1699" /> <path d="m 9.5,25.5 a 0.5,0.5 0 1 1 -1,0 0.5,0.5 0 1 1 1,0 z" style="fill:#000" id="p1701" /> <path d="m 15,15.5 a 0.5,1.5 0 1 1 -1,0 0.5,1.5 0 1 1 1,0 z" transform="matrix(0.87,0.5,-0.5,0.87,9.69,-5.17)" style="fill:#000" id="p1703" /> </g>""",
    "wp": """<path d="m %.2f,%.2f c -4.91,0 -8.89,3.98 -8.89,8.89 0,1.98 0.65,3.8 1.73,5.29 -4.33,2.49 -7.29,7.13 -7.29,12.49 0,4.51 2.09,8.53 5.36,11.18 -6.67,2.36 -16.47,12.33 -16.47,29.93 h 51.11 c 0,-17.6 -9.8,-27.58 -16.47,-29.93 3.27,-2.64 5.36,-6.67 5.36,-11.18 0,-5.36 -2.96,-10 -7.29,-12.49 1.09,-1.49 1.73,-3.31 1.73,-5.29 0,-4.91 -3.98,-8.89 -8.89,-8.89 z" style="fill:#fff;fill-rule:nonzero;stroke:#000;stroke-width:3.33;stroke-linecap:round;stroke-linejoin:miter" id="wp" />""",
    "wq": """<g style="fill:#fff;stroke:#000;stroke-width:1.5;stroke-linejoin:round" id="wq" transform="matrix(2.22,0,0,2.22,%.2f,%.2f)"> <path d="m 9,26 c 8.5,-1.5 21,-1.5 27,0 L 38.5,13.5 31,25 30.7,10.9 25.5,24.5 22.5,10 19.5,24.5 14.3,10.9 14,25 6.5,13.5 Z" id="p1821" /> <path d="m 9,26 c 0,2 1.5,2 2.5,4 1,1.5 1,1 0.5,3.5 -1.5,1 -1,2.5 -1,2.5 -1.5,1.5 0,2.5 0,2.5 6.5,1 16.5,1 23,0 0,0 1.5,-1 0,-2.5 0,0 0.5,-1.5 -1,-2.5 -0.5,-2.5 -0.5,-2 0.5,-3.5 1,-2 2.5,-2 2.5,-4 -8.5,-1.5 -18.5,-1.5 -27,0 z" id="p1823" /> <path d="M 11.5,30 C 15,29 30,29 33.5,30" style="fill:none" id="p1825" /> <path d="m 12,33.5 c 6,-1 15,-1 21,0" style="fill:none" id="p1827" /> <circle cx="6" cy="12" r="2" id="c1829" /> <circle cx="14" cy="9" r="2" id="c1831" /> <circle cx="22.5" cy="8" r="2" id="c1833" /> <circle cx="31" cy="9" r="2" id="c1835" /> <circle cx="39" cy="12" r="2" id="c1837" /> </g>""",
    "wr": """<g style="opacity:1;fill:#fff;fill-opacity:1;fill-rule:evenodd;stroke:#000;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round" transform="matrix(2.22,0,0,2.22,%.2f,%.2f)" id="wr"> <path d="M 9,39 H 36 V 36 H 9 Z" style="stroke-linecap:butt" id="p1909" /> <path d="m 12,36 v -4 h 21 v 4 z" style="stroke-linecap:butt" id="p1911" /> <path d="M 11,14 V 9 h 4 v 2 h 5 V 9 h 5 v 2 h 5 V 9 h 4 v 5" style="stroke-linecap:butt" id="p1913" /> <path d="m 34,14 -3,3 H 14 l -3,-3" id="p1915" /> <path d="M 31,17 V 29.5 H 14 V 17" style="stroke-linecap:butt;stroke-linejoin:miter" id="p1917" /> <path d="m 31,29.5 1.5,2.5 h -20 L 14,29.5" id="p1919" /> <path d="M 11,14 H 34" style="fill:none;stroke:#000;stroke-linejoin:miter" id="p1921" /> </g>""",
}

fen2long = {
    "k": "bk",
    "q": "bq",
    "r": "br",
    "b": "bb",
    "n": "bn",
    "p": "bp",
    "K": "wk",
    "Q": "wq",
    "R": "wr",
    "B": "wb",
    "N": "wn",
    "P": "wp",
}

# Do the actual conversion
def fen2svg(fen, light_color="#fff", dark_color="#bbb"):
    x = 0
    y = 0
    pieces = []
    for c in fen:
        if c == "/":
            continue

        if c.isdigit():
            x = x + int(c)
        else:
            lu = fen2long[c]
            templ = pieceTemplates[lu]
            offsets = pieceOffsets[lu]
            if lu not in pieceAnchors:
                pieces.append(templ%(offsets[0]+100*x, offsets[1]+100*y))
                pieceAnchors[lu] = (x,y)
            else:
                pieces.append('<use xlink:href="#%s" id="u%d_%d" transform="translate(%d,%d)" />'%(lu, x, y, (x-pieceAnchors[lu][0])*100, (y-pieceAnchors[lu][1])*100))
            x = x + 1
        if x>7:
            y = y +1
            x=0
        if y>7:
            break
    return svgTemplate.format(pieces="\n".join(pieces), dark_color=args.dark_color, light_color=args.light_color)

if __name__ == "__main__":
    if not args.output:
        outfile = sys.stdout
    else:
        outfile = open(args.output, "x" if not args.force else "w")

    print(fen2svg(args.fen, light_color=args.light_color, dark_color=args.dark_color), file=outfile)
    print(args.fen)
