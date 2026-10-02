package horserace;

/** One independently running horse. It never touches Swing components. */
final class Horse implements Runnable {
    interface Events {
        void onHorseFinished(Horse horse);
        void onHorseFailed(Horse horse, Throwable failure);
    }

    static final double BOOST_MULTIPLIER = 1.20;

    private final int id;
    private final double baseSpeed;
    private final int initialStamina;
    private final double finishDistance;
    private final long tickMillis;
    private final long boostDurationNanos;
    private final Events events;

    private volatile double position;
    private volatile int staminaRemaining;
    private volatile boolean boosting;
    private volatile boolean finished;
    private volatile boolean stopRequested;
    private volatile boolean boostModeEnabled;
    private volatile long boostEndsAtNanos;
    private volatile String threadName = "尚未啟動";

    Horse(int id, double baseSpeed, int stamina, RaceParameters parameters, Events events) {
        if (id <= 0 || baseSpeed <= 0.0 || stamina < 1 || stamina > 3) {
            throw new IllegalArgumentException("Invalid horse configuration");
        }
        this.id = id;
        this.baseSpeed = baseSpeed;
        this.initialStamina = stamina;
        this.staminaRemaining = stamina;
        this.finishDistance = parameters.finishDistance;
        this.tickMillis = parameters.tickMillis;
        this.boostDurationNanos = parameters.boostDurationMillis * 1_000_000L;
        this.events = events;
    }

    @Override
    public void run() {
        threadName = Thread.currentThread().getName();
        long previousNanos = System.nanoTime();
        try {
            while (!stopRequested && !finished) {
                Thread.sleep(tickMillis);
                long nowNanos = System.nanoTime();
                updateBoostAt(nowNanos);

                double elapsedSeconds = Math.min(0.25,
                        (nowNanos - previousNanos) / 1_000_000_000.0);
                previousNanos = nowNanos;
                double nextPosition = position + baseSpeed * currentSpeedMultiplier() * elapsedSeconds;
                position = Math.min(finishDistance, nextPosition);

                if (position >= finishDistance) {
                    finished = true;
                    boosting = false;
                    events.onHorseFinished(this);
                }
            }
        } catch (InterruptedException interrupted) {
            Thread.currentThread().interrupt();
        } catch (Throwable failure) {
            events.onHorseFailed(this, failure);
        }
    }

    void requestStop() {
        stopRequested = true;
    }

    synchronized void enableBoostMode() {
        enableBoostAt(System.nanoTime());
    }

    synchronized void enableBoostAt(long nowNanos) {
        if (boostModeEnabled || finished || stopRequested) {
            return;
        }
        boostModeEnabled = true;
        startNextBoostAt(nowNanos);
    }

    synchronized void updateBoostAt(long nowNanos) {
        while (boosting && nowNanos >= boostEndsAtNanos) {
            boosting = false;
            if (boostModeEnabled && staminaRemaining > 0 && !finished && !stopRequested) {
                startNextBoostAt(boostEndsAtNanos);
            }
        }
    }

    private void startNextBoostAt(long startNanos) {
        if (staminaRemaining <= 0 || finished || stopRequested) {
            boosting = false;
            return;
        }
        staminaRemaining--;
        boosting = true;
        boostEndsAtNanos = startNanos + boostDurationNanos;
    }

    double currentSpeedMultiplier() {
        return boosting ? BOOST_MULTIPLIER : 1.0;
    }

    int getId() {
        return id;
    }

    HorseSnapshot snapshot() {
        return new HorseSnapshot(
                id,
                Math.max(0.0, Math.min(1.0, position / finishDistance)),
                staminaRemaining,
                initialStamina,
                boosting,
                finished,
                baseSpeed,
                threadName
        );
    }
}

