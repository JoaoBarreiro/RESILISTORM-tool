import pygal

class GaugeChart:
    def __init__(self, value, min_value, max_value):
        self.value = value
        self.min_value = min_value
        self.max_value = max_value

    def plot(self):
        gauge = pygal.SolidGauge(
            half_pie=True, inner_radius=0.70,
            style=pygal.style.styles['default'](value_font_size=20))

        percent_formatter = lambda x: '{:.10g}%'.format(x)
        gauge.value_formatter = percent_formatter

        gauge.add('', [{'value': self.value, 'max_value': self.max_value}])
        gauge.render()

# Example usage
gauge = GaugeChart(value=75, min_value=0, max_value=100)
gauge.plot()
gauge.show()