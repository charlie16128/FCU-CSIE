# Candlestick Match Coverage Design

## Goal

Improve validation coverage so the locked candlestick model can produce meaningful out-of-sample matches without using 2026 data to tune any parameter.

## Scope

This first round changes only model discovery and validation selection:

- Set the assignment-defined minimum frequency parameter to `n = 5`.
- Keep the current minimum validation accuracy at `0.55`.
- Search similarity thresholds from `0.4` through `1.4` in increments of `0.1`.
- Search clustering distance thresholds `1.0`, `1.25`, `1.5`, and `2.0`.
- Keep the existing three interpretable weight presets.
- Select parameters by qualification and coverage before profit.
- Never fill the final Top 10 with patterns that fail the minimum frequency or accuracy requirement.

The full 1,024-combination group-weight grid and GUI changes are out of scope for this round.

## Data Boundaries

- 2018-2023: fit the scaler, identify bullish/bearish candidates, and form clusters.
- 2024-2025: compare cluster thresholds, weight presets, and similarity thresholds.
- 2026: final locked-model test only.

No 2026 result may influence the scaler, candidates, clusters, weights, similarity threshold, qualification rules, or Top 10 selection.

## Model Search

For each clustering threshold:

1. Cluster 2018-2023 bullish and bearish candidates separately.
2. Transform 2024-2025 validation rows with the discovery-only scaler.
3. For each existing weight preset, compute the pattern-to-row distance matrix once.
4. Reuse that matrix for all eleven similarity thresholds.
5. Compute validation metrics for every pattern.

Each pattern qualifies when:

```text
occurrence_count >= 5
accuracy >= 0.55
```

Parameter combinations are ranked lexicographically by:

1. whether both directions have at least ten qualified patterns;
2. the smaller of bullish and bearish qualified counts;
3. total qualified count;
4. total occurrence among the best ten qualified patterns per direction;
5. mean directional profit;
6. mean accuracy;
7. smaller similarity threshold;
8. smaller clustering threshold.

This ordering prevents a one-off high-profit match from defeating a configuration with adequate validation coverage.

## Final Pattern Selection

For each direction, only qualified patterns participate in ranking. They are ranked by average directional profit, accuracy, and occurrence count. The existing `0.30` weighted-distance duplicate check remains. If duplicate removal leaves fewer than ten, additional qualified patterns may fill the remaining slots; unqualified patterns may never fill them.

If the best configuration still has fewer than ten qualified bullish or bearish patterns, analysis stops with a message that reports the available counts. It does not overwrite the locked model with an invalid Top 10.

## Outputs

- `validation_results.csv` includes `cluster_distance_threshold` and coverage fields.
- `final_patterns.json` records the selected clustering distance threshold.
- The analysis summary reports the selected clustering threshold.
- Existing 2026 test files retain their schemas.

## Testing

Automated tests will verify:

- the threshold grids and `n = 5` configuration;
- coverage-first parameter ranking;
- rejection of unqualified Top 10 fillers;
- propagation of the clustering threshold through discovery and the locked model;
- existing feature, leakage, test-output, CLI, and GUI contracts.

