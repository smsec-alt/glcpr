
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAMx7cwEAAAAAGpt5INEcwcSdGiY9Rm4y98d9EpU%3DJkLAwRnJLoBqIllppv3lcxt1muXr7iKSDaqzjjPl2ItuvHcVYK'


styles = [
    dict(selector="th", props=[("color", "#005b65"),
                               ("border", "1px solid #FFFFFF"),
                               ("border-collapse", "collapse"),
                               ("background", "#FFFFFF"),
                               ("text-transform", "uppercase"),
                               ("font-size", "12px")
                               ]),
    dict(selector="td", props=[("color", "#000"),
                               ("padding", "15px 20px"),
                               ('text-align', 'center'),
                               ("font-size", "12px")
                               ])
]

for country in countries_list:
    new_key_drought, new_key_flooding, new_key_heat = f'drought_{country}', f'flooding_{country}', f'heatwave_{country}'
    vlookup_dict[new_key_drought] = f"{country} ({vlookup_dict['drought']})"
    vlookup_dict[new_key_flooding] = f"{country} ({vlookup_dict['flooding']})"
    vlookup_dict[new_key_heat] = f"{country} ({vlookup_dict['heat']})"


def style_negative(v, props=''):
    return props if v < 0 else None