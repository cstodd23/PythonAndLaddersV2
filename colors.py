from enum import Enum


class GameColors(Enum):
    PRUSSIAN_BLUE = (29, 45, 68)        # BACKGROUND
    WHITE_SMOKE = (246, 246, 245)       # SQUARE_0
    SILVER = (200, 200, 200)            # SQUARE_1
    HOOKER_GREEN = (78, 110, 88)        # LADDER
    REDWOOD = (159, 74, 84)             # SNAKE
    BLACK = (0, 0, 0)                   # NUMBERS
    INDIGO_DYE = (21, 59, 80)           # DEFAULT_PLAYER
    MAIZE = (253, 231, 108)             # BUTTON_1
    TEA_GREEN = (196, 214, 176)         # BUTTON_2
    ENGLISH_VIOLET = (89, 62, 106)      # DUNNO YET
    GUNMETAL = (16, 37, 43)             # ALSO DUNNO
    EBONY = (62, 75, 52)                # WE WILL FIND OUT

    @classmethod
    def rgb(cls, color_name):
        return cls[color_name].value

def lighten_color(color: GameColors, amount: float = 0.3) -> tuple:
    r, g, b = color.value
    return (
        min(int(r + (255 - r) * amount), 255),
        min(int(g + (255 - g) * amount), 255),
        min(int(b + (255 - b) * amount), 255)
    )

def darken_color(color: GameColors, amount: float = 0.3) -> tuple:
    r, g, b = color.value
    return (
        max(int(r * (1 - amount)), 0),
        max(int(g * (1 - amount)), 0),
        max(int(b * (1 - amount)), 0)
    )
