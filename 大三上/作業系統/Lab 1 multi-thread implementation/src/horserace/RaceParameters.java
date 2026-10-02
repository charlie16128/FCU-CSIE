package horserace;

/** Timing and distance values kept injectable for fast deterministic tests. */
final class RaceParameters {
    final double finishDistance;
    final long tickMillis;
    final long boostDurationMillis;
    final int minimumSpeed;
    final int maximumSpeed;

    RaceParameters(double finishDistance, long tickMillis, long boostDurationMillis,
                   int minimumSpeed, int maximumSpeed) {
        if (finishDistance <= 0.0 || tickMillis <= 0L || boostDurationMillis <= 0L
                || minimumSpeed <= 0 || maximumSpeed < minimumSpeed) {
            throw new IllegalArgumentException("Invalid race parameters");
        }
        this.finishDistance = finishDistance;
        this.tickMillis = tickMillis;
        this.boostDurationMillis = boostDurationMillis;
        this.minimumSpeed = minimumSpeed;
        this.maximumSpeed = maximumSpeed;
    }

    static RaceParameters defaults() {
        return new RaceParameters(1000.0, 25L, 1000L, 118, 190);
    }
}

