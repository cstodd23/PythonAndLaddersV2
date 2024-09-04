from enum import Enum


class GameColors(Enum):
    PRUSSIAN_BLUE = (29, 45, 68, 255)           # BACKGROUND
    WHITE_SMOKE = (246, 246, 245, 255)          # SQUARE_0
    SILVER = (200, 200, 200, 255)               # SQUARE_1
    HOOKER_GREEN = (78, 110, 88, 255)           # LADDER
    REDWOOD = (159, 74, 84, 255)                # SNAKE
    BLACK = (0, 0, 0, 255)                      # NUMBERS
    INDIGO_DYE = (21, 59, 80, 255)              # DEFAULT_PLAYER
    MAIZE = (253, 231, 108, 255)                # BUTTON_1
    TEA_GREEN = (196, 214, 176, 255)            # BUTTON_2
    ENGLISH_VIOLET = (89, 62, 106, 255)         # DUNNO YET
    GUNMETAL = (16, 37, 43, 255)                # ALSO DUNNO
    EBONY = (62, 75, 52, 255)                   # WE WILL FIND OUT
    # OPAQUE COLORS
    OPAQUE_PRUSSIAN_BLUE = (29, 45, 68, 200)    # BACKGROUND
    OPAQUE_WHITE_SMOKE = (246, 246, 245, 200)   # SQUARE_0
    OPAQUE_SILVER = (200, 200, 200, 200)        # SQUARE_1
    OPAQUE_HOOKER_GREEN = (78, 110, 88, 200)    # LADDER
    OPAQUE_REDWOOD = (159, 74, 84, 200)         # SNAKE
    OPAQUE_BLACK = (0, 0, 0, 200)               # NUMBERS
    OPAQUE_INDIGO_DYE = (21, 59, 80, 200)       # DEFAULT_PLAYER
    OPAQUE_MAIZE = (253, 231, 108, 200)         # BUTTON_1
    OPAQUE_TEA_GREEN = (196, 214, 176, 200)     # BUTTON_2
    OPAQUE_ENGLISH_VIOLET = (89, 62, 200)       # DUNNO YET
    OPAQUE_GUNMETAL = (16, 37, 43, 200)         # ALSO DUNNO
    OPAQUE_EBONY = (62, 75, 52, 200)            # WE WILL FIND OUT

    @classmethod
    def rgb(cls, color_name):
        return cls[color_name].value

def lighten_color(color: GameColors, amount: float = 0.3) -> tuple:
    print(color.value)
    r, g, b, o = color.value
    return (
        min(int(r + (255 - r) * amount), 255),
        min(int(g + (255 - g) * amount), 255),
        min(int(b + (255 - b) * amount), 255),
        o
    )

def darken_color(color: GameColors, amount: float = 0.3) -> tuple:
    r, g, b, o = color.value
    return (
        max(int(r * (1 - amount)), 0),
        max(int(g * (1 - amount)), 0),
        max(int(b * (1 - amount)), 0),
        o
    )
