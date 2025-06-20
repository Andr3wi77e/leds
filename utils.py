import config

def color_diff(c1, c2):
    return sum(abs(a - b) for a, b in zip(c1, c2))

def apply_black_cutoff(color, threshold=30):
    if sum(color) < threshold:
        return (0, 0, 0)
    return color

def suppress_low_values(r, g, b, threshold=40):
    if r < threshold and g < threshold and b < threshold:
        return (0, 0, 0)
    return (r, g, b)

def apply_warming(r, g, b, strength=config.WARMTH_STRENGTH):
    r = int(min(255, r + 50 * strength))
    g = int(min(255, g + 20 * strength))
    b = int(max(0, b - 80 * strength))
    return r, g, b

def apply_gamma(r, g, b, gamma=config.GAMMA):
    def correct(channel):
        normalized = channel / 255.0
        corrected = pow(normalized, gamma)
        return int(min(255, max(0, corrected * 255)))
    return correct(r), correct(g), correct(b)

def apply_config_color_settings(*avg):
    if config.ENABLE_WARMING:
        avg = apply_warming(*avg)
    if config.ENABLE_GAMMA:
        avg = apply_gamma(*avg)
    return avg