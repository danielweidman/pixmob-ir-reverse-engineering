colors = {
    "RED":[1,1,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,1,1,0,1,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "RED_2":[1,1,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,0,1,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "RED_3":[1,1,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "RED_4":[1,1,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "RED_5":[1,1,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,0,1,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "DIM_RED":[1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,1,0,1,0,0,1,0,1,0,1,1,0,0,0,0,1],
    "DIM_RED_2":[1,0,1,0,0,0,1,1,0,0,1,0,0,0,1,0,0,1,0,1,0,0,1,1,0,1,0,0,1,0,1,0,1,1,0,0,0,0,1],
    "GREEN":[1,1,0,0,1,0,1,0,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "GREEN_2":[1,1,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "GREEN_3":[1,1,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "GREEN_4":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,1,1,0,0,0,1,1,0,0,0,0,1],
    "GREEN_5":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,1,0,0,0,0,1],
    "GREEN_6":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,0,1,1,0,0,0,0,1],
    "GREEN_7":[1,0,1,0,0,0,1,0,1,0,1,0,0,1,1,0,1,0,0,1,0,1,1,0,0,1,0,1,0,0,0,0,1,1,0,0,0,0,1],
    "GREEN_8":[1,1,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1],
    "GREEN_9":[1,1,0,0,1,0,1,0,0,1,0,1,0,1,1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1],
    "GREEN_10":[1,1,0,0,1,0,1,0,0,1,0,1,0,1,1,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1],
    "GREEN_11":[1,1,0,0,0,0,1,0,1,1,0,1,0,1,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,1,0,0,0,0,1],
    "GREEN_12":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,1,1,0,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "GREEN_13":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1],
    "GREEN_14":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,1,0,0,0,0,1,0,0,1,0,0,1],
    "GREEN_15":[1,1,0,0,0,0,1,0,1,1,0,1,0,1,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,1,0,0,0,0,1],
    "GREEN_DIM":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1],
    "LIGHT_GREEN":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,0,1,0,0,1,0,0,1],
    "LIGHT_GREEN_2":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1],
    "YELLOWGREEN":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,0,1,1,0,0,0,0,1],
    "YELLOWGREEN_2":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,1,1,0,0,1,0,1,0,1,0,0,0,0,1,1,0,0,0,0,1],
    "YELLOWGREEN_3":[1,1,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,1,0,1,0,1,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "BLUE":[1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,1,0,1,0,0,1,0,1,0,1,0,1,0,0,0,1],
    "BLUE_2":[1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,1,0,1,0,0,1,0,1,0,1,0,1,0,0,0,1],
    "BLUE_3":[1,0,1,0,0,0,1,1,0,0,1,0,0,0,1,0,0,1,0,1,0,0,1,1,0,1,0,0,1,0,1,0,1,0,1,0,0,0,1],
    "LIGHT_BLUE":[1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,1,0,1,0,1,1,0,0,1,0,0,0,1],
    "LIGHT_BLUE_2":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,1,0,0,0,0,1,0,1,1,0,0,1],
    "LIGHT_BLUE_3":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,1,0,0,0,0,1,1,0,1,0,0,1],
    "DIM_BLUE":[1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,1,0,1,0,0,1,0,1,0,1,0,0,1,0,0,1],
    "MAGENTA":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,1,0,1,1,0,0,0,1,0,1,0,0,0,1],
    "MAGENTA_2":[1,0,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,1,0,1,0,0,1,1,0,1,0,0,1,0,0,0,1,0,0,1,1,0,1],
    "MAGENTA_3":[1,0,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,1,0,1,0,0,1,1,0,1,0,0,1,0,0,0,1,1,0,1,1,0,1],
    "MAGENTA_4":[1,0,1,0,0,0,1,1,0,1,0,1,0,1,1,0,0,1,0,1,0,0,1,1,0,1,0,0,1,0,0,0,1,1,0,1,1,0,1],
    "YELLOW":[1,1,0,0,1,0,1,0,1,1,0,0,0,0,1,0,0,0,1,0,1,0,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "YELLOW_2":[1,1,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "YELLOW_3":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,1,1,0,0,0,1,1,0,0,0,0,1],
    "YELLOW_4":[1,0,1,0,0,0,1,1,0,0,1,0,0,0,1,0,0,1,0,1,0,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,0,0,1],
    "YELLOW_5":[1,0,1,0,0,0,1,1,0,0,1,0,0,0,1,0,0,1,0,1,0,0,1,0,1,1,0,0,1,0,1,1,0,1,0,0,0,0,1],
    "YELLOW_6":[1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,1,0,0,1,0,1,1,0,1,0,0,0,0,1],
    "YELLOW_7":[1,1,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,0,1,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1],
    "YELLOW_8":[1,1,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,1,0,1,0,1,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "YELLOW_9":[1,1,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,1,1,0,1,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1],
    "PINK":[1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,1,0,0,1,0,0,0,1,0,1,0,0,0,1],
    "PINK_2":[1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,0,1,1,0,0,0,0,1,1,0,0,1,0,0,0,1,0,1,0,0,0,1],
    "PINK_3":[1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,1,0,0,1,0,0,0,1,0,1,0,0,0,1],
    "PINK_4":[1,0,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,1,0,1,0,0,1,0,1,1,0,0,1,0,0,1,0,0,0,1,1,0,1],
    "PINK_5":[1,0,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,1,0,1,0,0,1,0,1,1,0,0,1,0,0,1,0,1,0,1,1,0,1],
    "ORANGE":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,0,1,1,0,0,0,0,1],
    "ORANGE_2":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "ORANGE_3":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,1,1,0,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "REDORANGE":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0,1,0,0,1,0,0,0,1,1,0,0,0,0,1],
    "REDORANGE_2":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,1,0,1,1,0,0,0,1,1,0,0,0,0,1],
    "REDORANGE_3":[1,1,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,0,1,0,1,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1],
    "YELLOWORANGE_1":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,0,1,1,0,0,0,1,1,0,0,0,0,1],
    "YELLOWORANGE_2":[1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,1,0,0,1,0,0,0,1,1,0,0,0,0,1],
    "WHITISH":[1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,1,0,0,1,0,0,0,1,0,0,1,0,0,1],
    "WHITISH_LONG":[1,0,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,1,0,1,0,0,0,0,1,1,0,0,1,0,1,1,0,0,0,1,1,0,1],
    "WHITISH_2":[1,0,1,0,0,0,1,1,0,0,1,0,0,0,1,0,0,1,0,1,0,0,0,0,1,1,0,0,1,0,0,0,1,0,1,0,0,0,1],
    "WHITISH_LONG_2":[1,0,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,1,0,1,0,0,0,0,1,1,0,0,1,0,1,1,0,1,0,1,1,0,1],
    "WHITISH_3":[1,1,0,0,1,0,1,0,1,1,0,0,0,0,1,0,0,0,1,0,1,0,0,1,0,0,1,1,0,0,0,0,1,0,1,0,0,0,1],
    "WHITISH_4":[1,0,1,0,0,0,1,1,0,0,1,0,0,0,1,0,0,1,0,1,0,0,1,0,1,1,0,0,1,0,1,1,0,0,1,0,0,0,1],
    "WHITISH_5":[1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,1,0,0,1,0,1,1,0,0,1,0,0,0,1],
    "WHITISH_6":[1,0,1,0,0,0,1,1,0,1,0,1,0,1,1,0,0,1,0,1,0,0,0,0,1,1,0,0,1,0,1,1,0,1,0,1,1,0,1],
    "WHITISH_7":[1,0,1,0,0,0,1,1,0,1,0,1,0,1,1,0,0,1,0,1,0,0,1,0,1,1,0,0,1,0,0,1,0,1,0,1,1,0,1],
    "TURQUOISE":[1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,0,0,1,0,1,1,0,0,1,0,0,1,1,0,0,0,0,1,0,1,0,0,0,1],
    "TURQUOISE_2":[1,0,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,1,1,0,1],
    "TURQUOISE_3":[1,0,1,0,0,0,1,1,0,1,0,1,0,1,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,1,0,1,1,0,1,1,0,1],
    "TURQUOISE_4":[1,0,1,0,0,0,1,1,0,0,1,1,0,1,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,1,0,1,1,0,1,1,0,1]
}