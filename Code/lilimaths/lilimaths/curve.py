from dataclasses import dataclass, field

@dataclass
class Curve:
    """
    Defines a curve object including data point pairs, the curve's label and color.
    """
    values: list[tuple[float, float]] = field(default_factory=list)
    label: str = ''
    color: str = 'blue'
    kind: str  = 'line'   # supported: 'line', 'scatter'
    marker: str = '.'     # irrelevant if line

if __name__ == '__main__':
    curve = Curve()
    print(curve)
