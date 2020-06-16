from . import main


@main.app_template_filter()
def rubles(value: float):
    return f"{value:.2f} &#8381;"
