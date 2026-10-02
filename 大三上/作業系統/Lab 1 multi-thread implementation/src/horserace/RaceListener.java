package horserace;

import java.util.List;

/** Receives race events. Callbacks may originate from horse worker threads. */
public interface RaceListener {
    void onRaceStarted(List<HorseSnapshot> horses);
    void onFirstHorseFinished(int horseId);
    void onHorseFinished(int horseId, int place, List<Integer> ranking);
    void onRaceFinished(List<Integer> ranking);
    void onRaceFailed(String message);
}

