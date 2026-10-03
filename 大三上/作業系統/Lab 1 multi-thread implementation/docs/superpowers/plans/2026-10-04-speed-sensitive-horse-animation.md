# Speed-Sensitive Horse Animation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make each Java2D horse visibly animate at a cadence derived from its current speed, including a faster gait during the existing 20% boost.

**Architecture:** Keep the single-file Swing application and existing worker-thread model. Add pure timing helpers for deterministic tests, carry effective speed in the immutable GUI snapshot, and select one of three procedural poses using one timestamp per repaint. Do not add animation threads or external image assets.

**Tech Stack:** Java 21, Swing, Java2D, plain Java test runner

---

### Task 1: Define and test speed-to-animation timing

**Files:**
- Create: `HorseRaceAnimationTest.java`
- Modify: `HorseRace.java:35-40`

- [ ] **Step 1: Write the failing test**

Create `HorseRaceAnimationTest.java`:

```java
public final class HorseRaceAnimationTest {
    private HorseRaceAnimationTest() { }

    public static void main(String[] args) {
        assertEquals(200L, HorseRace.animationFrameDurationMillis(118.0),
                "slow horse frame duration");
        assertEquals(85L, HorseRace.animationFrameDurationMillis(228.0),
                "fast horse frame duration");
        assertTrue(HorseRace.animationFrameDurationMillis(180.0)
                        < HorseRace.animationFrameDurationMillis(150.0),
                "higher speed must shorten frame duration");
        assertEquals(0, HorseRace.animationFrame(150.0, 400L, false),
                "stationary horse uses neutral frame");
        assertTrue(HorseRace.animationFrame(118.0, 200L, true)
                        != HorseRace.animationFrame(228.0, 200L, true),
                "slow and fast horses can show different poses");
        assertDoubleEquals(150.0, HorseRace.currentSpeed(150.0, false, false),
                "normal speed");
        assertDoubleEquals(180.0, HorseRace.currentSpeed(150.0, true, false),
                "boosted speed");
        assertDoubleEquals(0.0, HorseRace.currentSpeed(150.0, true, true),
                "finished speed");
        System.out.println("HorseRaceAnimationTest: PASS");
    }

    private static void assertEquals(long expected, long actual, String message) {
        if (expected != actual) {
            throw new AssertionError(message + ": expected " + expected + ", got " + actual);
        }
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }

    private static void assertDoubleEquals(double expected, double actual, String message) {
        if (Math.abs(expected - actual) > 0.000001) {
            throw new AssertionError(message + ": expected " + expected + ", got " + actual);
        }
    }
}
```

- [ ] **Step 2: Verify the test fails before implementation**

Run `javac -encoding UTF-8 HorseRace.java HorseRaceAnimationTest.java`.

Expected: `cannot find symbol` for `animationFrameDurationMillis`, `animationFrame`, and `currentSpeed`.

- [ ] **Step 3: Add the pure timing helpers**

Add these members to outer class `HorseRace`:

```java
private static final double BOOST_MULTIPLIER = 1.20;
private static final double SLOW_ANIMATION_SPEED = 118.0;
private static final double FAST_ANIMATION_SPEED = 228.0;
private static final long SLOW_FRAME_MILLIS = 200L;
private static final long FAST_FRAME_MILLIS = 85L;
private static final int RUNNING_FRAME_COUNT = 3;

static double currentSpeed(double baseSpeed, boolean boosting, boolean finished) {
    return finished ? 0.0 : baseSpeed * (boosting ? BOOST_MULTIPLIER : 1.0);
}

static long animationFrameDurationMillis(double speed) {
    double clamped = Math.max(SLOW_ANIMATION_SPEED,
            Math.min(FAST_ANIMATION_SPEED, speed));
    double ratio = (clamped - SLOW_ANIMATION_SPEED)
            / (FAST_ANIMATION_SPEED - SLOW_ANIMATION_SPEED);
    return Math.round(SLOW_FRAME_MILLIS
            - ratio * (SLOW_FRAME_MILLIS - FAST_FRAME_MILLIS));
}

static int animationFrame(double speed, long nowMillis, boolean moving) {
    if (!moving || speed <= 0.0) {
        return 0;
    }
    return (int) ((nowMillis / animationFrameDurationMillis(speed))
            % RUNNING_FRAME_COUNT);
}
```

Replace `boosting ? 1.20 : 1.0` in `Horse.run()` with `boosting ? BOOST_MULTIPLIER : 1.0`.

- [ ] **Step 4: Compile and run the test**

Run:

```powershell
javac -encoding UTF-8 HorseRace.java HorseRaceAnimationTest.java
java HorseRaceAnimationTest
```

Expected: `HorseRaceAnimationTest: PASS`.

### Task 2: Carry effective speed in immutable snapshots

**Files:**
- Modify: `HorseRace.java:76-94`
- Modify: `HorseRace.java:181-190`

- [ ] **Step 1: Add the snapshot value**

Add `final double currentSpeed;` to `HorseSnapshot`, add a `double currentSpeed` constructor parameter before the two boolean flags, and assign it with `this.currentSpeed = currentSpeed;`.

- [ ] **Step 2: Populate it from a consistent state read**

Replace `Horse.snapshot()` with:

```java
HorseSnapshot snapshot() {
    boolean isBoosting = boosting;
    boolean isFinished = finished;
    return new HorseSnapshot(
            id,
            Math.max(0.0, Math.min(1.0, position / FINISH_DISTANCE)),
            staminaRemaining,
            initialStamina,
            currentSpeed(baseSpeed, isBoosting, isFinished),
            isBoosting,
            isFinished
    );
}
```

- [ ] **Step 3: Compile and run the test**

Run `javac -encoding UTF-8 HorseRace.java HorseRaceAnimationTest.java`, then `java HorseRaceAnimationTest`.

Expected: `HorseRaceAnimationTest: PASS`.

### Task 3: Render three distinct running poses

**Files:**
- Modify: `HorseRace.java:403-536`

- [ ] **Step 1: Use one timestamp for every horse in a repaint**

In `drawTrack`, set `long animationTimeMillis = System.currentTimeMillis();` before the lane loop. Pass it as the final argument to `drawHorse` and add the matching `long animationTimeMillis` parameter to that method.

- [ ] **Step 2: Select pose offsets from effective speed**

At the start of `drawHorse`, after calculating `scale`, add:

```java
int frame = horse == null ? 0 : animationFrame(
        horse.currentSpeed, animationTimeMillis, !horse.finished);
int[] bodyBounce = {0, 1, -1};
int[] headBob = {0, 1, -1};
int[] tailLift = {-2, 2, -5};
int poseCenterY = centerY + (int) Math.round(bodyBounce[frame] * scale);
```

Use `poseCenterY` for body and badge placement. Apply `headBob[frame]` to neck/head Y coordinates and `tailLift[frame]` to the tail endpoint.

- [ ] **Step 3: Replace fixed legs with articulated pose tables**

Add this helper inside `RacePanel`:

```java
private void drawLeg(Graphics2D g2, int hipX, int hipY,
                     int kneeDx, int hoofDx, double scale) {
    int kneeX = hipX + (int) Math.round(kneeDx * scale);
    int kneeY = hipY + (int) Math.round(7 * scale);
    int hoofX = hipX + (int) Math.round(hoofDx * scale);
    int hoofY = hipY + (int) Math.round(14 * scale);
    g2.drawLine(hipX, hipY, kneeX, kneeY);
    g2.drawLine(kneeX, kneeY, hoofX, hoofY);
}
```

Replace the two fixed leg lines with:

```java
int[][] hindLegs = {{-3, -8}, {2, 0}, {4, 8}};
int[][] rearLegs = {{3, 7}, {-2, -1}, {-4, -8}};
int[][] foreLegs = {{4, 9}, {-2, 0}, {-4, -8}};
int[][] frontLegs = {{-3, -7}, {2, 1}, {4, 8}};
int legTop = bodyY + bodyH - (int) Math.round(2 * scale);

g2.setColor(color.darker().darker());
drawLeg(g2, bodyX + (int) Math.round(9 * scale), legTop,
        rearLegs[frame][0], rearLegs[frame][1], scale);
drawLeg(g2, bodyX + bodyW - (int) Math.round(9 * scale), legTop,
        foreLegs[frame][0], foreLegs[frame][1], scale);
g2.setColor(color.darker());
drawLeg(g2, bodyX + (int) Math.round(4 * scale), legTop,
        hindLegs[frame][0], hindLegs[frame][1], scale);
drawLeg(g2, bodyX + bodyW - (int) Math.round(4 * scale), legTop,
        frontLegs[frame][0], frontLegs[frame][1], scale);
```

Preview and finished horses select frame zero. Running horses cycle through all frames, and boosted speed shortens the frame duration while the existing glow, lightning, and `x1.2` remain.

- [ ] **Step 4: Compile and verify**

Run:

```powershell
javac -encoding UTF-8 HorseRace.java HorseRaceAnimationTest.java
java HorseRaceAnimationTest
git diff --check
```

Expected: compilation succeeds, the test prints `HorseRaceAnimationTest: PASS`, and the diff check has no output.

- [ ] **Step 5: Review the diff**

Run `git diff -- HorseRace.java HorseRaceAnimationTest.java`. Confirm distance, random speed range, stamina, ranking, thread lifecycle, and EDT handling are unchanged.

### Task 4: Commit and final verification

**Files:**
- Verify: `HorseRace.java`
- Verify: `HorseRaceAnimationTest.java`
- Verify: `docs/superpowers/specs/2026-10-03-speed-sensitive-horse-animation-design.md`

- [ ] **Step 1: Commit the implementation**

Run:

```powershell
git add -- HorseRace.java HorseRaceAnimationTest.java
git commit -m "feat: animate horses according to current speed"
```

- [ ] **Step 2: Run fresh verification**

Run:

```powershell
javac -encoding UTF-8 HorseRace.java HorseRaceAnimationTest.java
java HorseRaceAnimationTest
git diff --check HEAD~1..HEAD
git status --short -- HorseRace.java HorseRaceAnimationTest.java docs/superpowers
```

Expected: compile and test exit 0, test prints `HorseRaceAnimationTest: PASS`, diff check has no output, and relevant status is clean.

- [ ] **Step 3: Check every completion criterion**

Confirm: faster speed means shorter frame duration; a 20% boost produces a faster gait and retains indicators; preview/finished horses remain fixed; existing race rules and concurrency structure remain unchanged.

- [ ] **Step 4: Perform final self-review**

Inspect the committed diff for correctness, concurrency safety, visual bounds at 2 and 10 horses, and agreement with the design. Fix every Critical or Important issue before reporting completion.
