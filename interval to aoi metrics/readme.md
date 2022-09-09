# Interval to AOI metrics

This script transforms an interval-based metrics format in Pro Lab (each AOI as a separate column) into an AOI-based metrics format (each AOI is on a separate row and identified by a single AOI column). This longer format makes more sense when you are comparing AOIs against other AOIs, whereas the interval-based format is better for comparing trials against other trials.

## Example
**META1**    **METRIC.AOI_1**    **METRIC.AOI_2**
jane         5               10

...becomes...

|**META1** | **AOI** | **METRIC** |
|jane | AOI_1 | 5 |
|jane | AOI_2 | 10 |