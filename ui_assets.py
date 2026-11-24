"""ابزارهای سادهٔ رسم با Canvas؛ این فایل به کتابخانهٔ اضافی نیاز ندارد."""


def hex_to_rgb(color_code):
    """کد رنگی مثل #684363 را به سه عدد قرمز، سبز و آبی تبدیل می‌کند."""
    value = color_code.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def rgb_to_hex(rgb):
    """سه عدد قرمز، سبز و آبی را به کد رنگی #RRGGBB تبدیل می‌کند."""
    return "#%02x%02x%02x" % rgb


def draw_vertical_gradient(canvas, width, height, color_top, color_bottom, steps=120):
    """با چند مستطیل باریک، گرادیان عمودی را داخل Canvas می‌کشد."""
    top = hex_to_rgb(color_top)
    bottom = hex_to_rgb(color_bottom)
    steps = max(1, min(int(steps), int(height)))
    canvas.configure(bg=color_bottom)

    # هر مستطیل کمی با قبلی فرق رنگ دارد؛ کنار هم قرارگرفتنشان حس گرادیان می‌دهد.
    for index in range(steps):
        ratio = index / max(1, steps - 1)
        color = tuple(round(a + (b - a) * ratio) for a, b in zip(top, bottom))
        y1 = round(height * index / steps)
        y2 = round(height * (index + 1) / steps) + 1
        canvas.create_rectangle(0, y1, width, y2, fill=rgb_to_hex(color), outline="")
