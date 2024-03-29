"""

. # ┤ ┴ ┬ ├ ┼ ┌ ┐ ┘ └ ─ │
┤ ┴ ┬ ├
FLOOR WALL LEFT-
"""


WALL_CHARS = {0:".",

2: "#", 10: "#", 32: "#", 34: "#", 40: "#", 42: "#", 128: "#", 130: "#", 136: "#", 138: "#", 142: "#", 154: "#", 162: "#", 168: "#", 160: "#", 170: "#", 174: "#",

84: "┤", 86: "┤", 92: "┤", 94: "┤", 116: "┤", 118: "┤", 212: "┤", 214: "┤", 215: "┤", 220: "┤", 222: "┤", 244: "┤", 246: "┤",

81: "┴", 83: "┴", 89: "┴", 91: "┴", 95: "┴", 121: "┴", 113: "┴", 123: "┴", 217: "┴", 115: "┴", 209: "┴", 211: "┴", 219: "┴",

21: "┬", 23: "┬", 61: "┬", 149: "┬", 245: "┬", 53: "┬", 181: "┬", 55: "┬", 29: "┬", 189: "┬", 157: "┬", 151: "┬", 183: "┬",

69: "├", 77: "├", 101: "├", 111: "├", 109: "├", 125: "├", 229: "├", 237: "├", 71: "├", 197: "├", 103: "├", 79: "├", 205: "├",

85: "┼", 87: "┼", 117: "┼", 119: "┼", 221: "┼", 213: "┼", 93: "┼",

5: "┌", 7: "┌", 37: "┌", 253: "┌", 141: "┌", 135: "┌", 133: "┌", 165: "┌", 143: "┌", 167: "┌", 15: "┌", 13: "┌", 39: "┌", 47: "┌", 173: "┌", 175: "┌", 45: "┌",

20: "┐", 22: "┐",54: "┐",60: "┐",62: "┐",148: "┐", 247: "┐", 188: "┐",28: "┐",30: "┐",190: "┐",156: "┐",52: "┐",158: "┐",182: "┐",150: "┐",180: "┐",

65: "└", 127: "└", 225: "└", 233: "└", 67: "└", 73: "└", 75: "└", 227: "└", 193: "└", 97: "└", 105: "└", 107: "└", 195: "└", 99: "└", 203: "└", 201: "└", 235: "└",

80: "┘", 90: "┘", 120: "┘", 122: "┘", 223: "┘", 240: "┘", 242: "┘", 248: "┘", 208: "┘", 112: "┘", 216: "┘", 88: "┘", 250: "┘", 114: "┘", 218: "┘", 82: "┘", 210: "┘",

1: "─", 3: "─", 9: "─", 16: "─", 17: "─", 18: "─", 19: "─", 24: "─", 25: "─", 26: "─", 27: "─", 31: "─",
33: "─", 35: "─", 43: "─", 48: "─", 49: "─", 50: "─", 51: "─", 56: "─", 57: "─", 58: "─", 59: "─", 63: "─", 129: "─", 161: "─",
144: "─", 145: "─", 146: "─", 147: "─", 153: "─", 155: "─", 159: "─", 176: "─", 177: "─", 179: "─", 184: "─", 185: "─", 186: "─", 187: "─", 191: "─", 241: "─", 243: "─", 152: "─",
249: "─", 251: "─", 137: "─", 131: "─", 41: "─", 169: "─", 139: "─", 163: "─", 171: "─", 11: "─", 178: "─",


4: "│", 6: "│", 8: "│", 12: "│", 36: "│", 38: "│", 44: "│", 46: "│", 64: "│", 66: "│", 68: "│", 70: "│", 72: "│", 74: "│", 76: "│", 78: "│", 96: "│", 98: "│", 100: "│", 102: "│", 104: "│", 108: "│", 110: "│", 124: "│", 126: "│",
132: "│", 164: "│", 192: "│", 194: "│", 196: "│", 198: "│", 199: "│", 202: "│", 204: "│", 206: "│", 207: "│", 224: "│", 226: "│", 228: "│", 230: "│", 232: "│", 236: "│", 238: "│", 239: "│", 252: "│", 254: "│", 200: "│",
231: "│", 134: "│", 172: "│", 14: "│", 166: "│", 106: "│", 234: "│", 140: "│",

}


DOUBLE_WALL_CHARS = {0:".",

2: "#", 10: "#", 32: "#", 34: "#", 40: "#", 42: "#", 128: "#", 130: "#", 136: "#", 138: "#", 142: "#", 154: "#", 162: "#", 168: "#", 160: "#", 170: "#", 174: "#",

84: "╣", 86: "╣", 92: "╣", 94: "╣", 116: "╣", 118: "╣", 212: "╣", 214: "╣", 215: "╣", 220: "╣", 222: "╣", 244: "╣", 246: "╣",

81: "╩", 83: "╩", 89: "╩", 91: "╩", 95: "╩", 121: "╩", 113: "╩", 123: "╩", 217: "╩", 115: "╩", 209: "╩", 211: "╩", 219: "╩",

21: "╦", 23: "╦", 61: "╦", 149: "╦", 245: "╦", 53: "╦", 181: "╦", 55: "╦", 29: "╦", 189: "╦", 157: "╦", 151: "╦", 183: "╦",

69: "╠", 77: "╠", 101: "╠", 111: "╠", 109: "╠", 125: "╠", 229: "╠", 237: "╠", 71: "╠", 197: "╠", 103: "╠", 79: "╠", 205: "╠",

85: "┼", 87: "┼", 117: "┼", 119: "┼", 221: "┼", 213: "┼", 93: "┼",

5: "╔", 7: "╔", 37: "╔", 253: "╔", 141: "╔", 135: "╔", 133: "╔", 165: "╔", 143: "╔", 167: "╔", 15: "╔", 13: "╔", 39: "╔", 47: "╔", 173: "╔", 175: "╔", 45: "╔",

20: "╗", 22: "╗",54: "╗",60: "╗",62: "╗",148: "╗", 247: "╗", 188: "╗",28: "╗",30: "╗",190: "╗",156: "╗",52: "╗",158: "╗",182: "╗",150: "╗",180: "╗",

65: "╚", 127: "╚", 225: "╚", 233: "╚", 67: "╚", 73: "╚", 75: "╚", 227: "╚", 193: "╚", 97: "╚", 105: "╚", 107: "╚", 195: "╚", 99: "╚", 203: "╚", 201: "╚", 235: "╚",

80: "╝", 90: "╝", 120: "╝", 122: "╝", 223: "╝", 240: "╝", 242: "╝", 248: "╝", 208: "╝", 112: "╝", 216: "╝", 88: "╝", 250: "╝", 114: "╝", 218: "╝", 82: "╝", 210: "╝",

1: "═", 3: "═", 9: "═", 16: "═", 17: "═", 18: "═", 19: "═", 24: "═", 25: "═", 26: "═", 27: "═", 31: "═",
33: "═", 35: "═", 43: "═", 48: "═", 49: "═", 50: "═", 51: "═", 56: "═", 57: "═", 58: "═", 59: "═", 63: "═", 129: "═", 161: "═",
144: "═", 145: "═", 146: "═", 147: "═", 153: "═", 155: "═", 159: "═", 176: "═", 177: "═", 179: "═", 184: "═", 185: "═", 186: "═", 187: "═", 191: "═", 241: "═", 243: "═", 152: "═",
249: "═", 251: "═", 137: "═", 131: "═", 41: "═", 169: "═", 139: "═", 163: "═", 171: "═", 11: "═", 178: "═",


4: "║", 6: "║", 8: "║", 12: "║", 36: "║", 38: "║", 44: "║", 46: "║", 64: "║", 66: "║", 68: "║", 70: "║", 72: "║", 74: "║", 76: "║", 78: "║", 96: "║", 98: "║", 100: "║", 102: "║", 104: "║", 108: "║", 110: "║", 124: "║", 126: "║",
132: "║", 164: "║", 192: "║", 194: "║", 196: "║", 198: "║", 199: "║", 202: "║", 204: "║", 206: "║", 207: "║", 224: "║", 226: "║", 228: "║", 230: "║", 232: "║", 236: "║", 238: "║", 239: "║", 252: "║", 254: "║", 200: "║",
231: "║", 134: "║", 172: "║", 14: "║", 166: "║", 106: "║", 234: "║", 140: "║",

}