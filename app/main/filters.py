from . import main


@main.app_template_filter('rubles')
def _jinja2_filter_rubles(value: float):
    return f"{value:.2f} &#8381;"


@main.app_template_filter('dt')
def _jinja2_filter_dt(date, fmt=None):
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime('%d/%m/%Y')


@main.app_template_filter('tm')
def _jinja2_filter_tt(time, fmt=None):
    if fmt:
        return time.strftime(fmt)
    else:
        return time.strftime('%H:%M')
