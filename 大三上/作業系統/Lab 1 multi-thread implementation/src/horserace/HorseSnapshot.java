package horserace;

/** Immutable state used by the Swing view. */
public final class HorseSnapshot {
    private final int id;
    private final double progress;
    private final int staminaRemaining;
    private final int initialStamina;
    private final boolean boosting;
    private final boolean finished;
    private final double baseSpeed;
    private final String threadName;

    public HorseSnapshot(int id, double progress, int staminaRemaining, int initialStamina,
                         boolean boosting, boolean finished, double baseSpeed, String threadName) {
        this.id = id;
        this.progress = progress;
        this.staminaRemaining = staminaRemaining;
        this.initialStamina = initialStamina;
        this.boosting = boosting;
        this.finished = finished;
        this.baseSpeed = baseSpeed;
        this.threadName = threadName;
    }

    public int getId() { return id; }
    public double getProgress() { return progress; }
    public int getStaminaRemaining() { return staminaRemaining; }
    public int getInitialStamina() { return initialStamina; }
    public boolean isBoosting() { return boosting; }
    public boolean isFinished() { return finished; }
    public double getBaseSpeed() { return baseSpeed; }
    public String getThreadName() { return threadName; }
}
