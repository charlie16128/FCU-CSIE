package horserace;

import javax.swing.JPanel;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Polygon;
import java.awt.RenderingHints;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Paints the track and horses from immutable snapshots. */
public final class RacePanel extends JPanel {
    private static final Color TRACK_LIGHT = new Color(232, 244, 233);
    private static final Color TRACK_DARK = new Color(220, 237, 222);
    private static final Color TRACK_LINE = new Color(188, 210, 190);
    private static final Color[] HORSE_COLORS = {
            new Color(43, 108, 176), new Color(197, 48, 48), new Color(47, 133, 90),
            new Color(128, 90, 213), new Color(221, 107, 32), new Color(49, 130, 206),
            new Color(183, 121, 31), new Color(56, 161, 105), new Color(184, 50, 128),
            new Color(74, 85, 104)
    };

    private volatile List<HorseSnapshot> snapshots = Collections.emptyList();
    private volatile int previewHorseCount = 5;

    public RacePanel() {
        setBackground(new Color(248, 250, 252));
        setPreferredSize(new Dimension(1040, 520));
        setMinimumSize(new Dimension(720, 400));
    }

    public void setSnapshots(List<HorseSnapshot> snapshots) {
        this.snapshots = Collections.unmodifiableList(new ArrayList<HorseSnapshot>(snapshots));
        repaint();
    }

    public void showPreview(int horseCount) {
        previewHorseCount = horseCount;
        snapshots = Collections.emptyList();
        repaint();
    }

    @Override
    protected void paintComponent(Graphics graphics) {
        super.paintComponent(graphics);
        Graphics2D g2 = (Graphics2D) graphics.create();
        try {
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
            g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
            List<HorseSnapshot> current = snapshots;
            int horseCount = current.isEmpty() ? previewHorseCount : current.size();
            paintTrack(g2, current, horseCount);
        } finally {
            g2.dispose();
        }
    }

    private void paintTrack(Graphics2D g2, List<HorseSnapshot> current, int horseCount) {
        int width = getWidth();
        int height = getHeight();
        int top = 18;
        int bottom = 18;
        int startX = 105;
        int finishX = width - 66;
        int laneHeight = Math.max(38, (height - top - bottom) / horseCount);
        int trackHeight = laneHeight * horseCount;
        int trackTop = Math.max(top, (height - trackHeight) / 2);

        g2.setFont(uiFont(Font.BOLD, 14));
        for (int index = 0; index < horseCount; index++) {
            int laneY = trackTop + index * laneHeight;
            g2.setColor(index % 2 == 0 ? TRACK_LIGHT : TRACK_DARK);
            g2.fillRoundRect(10, laneY, width - 20, laneHeight - 3, 12, 12);

            g2.setColor(TRACK_LINE);
            g2.setStroke(new BasicStroke(1f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_BEVEL,
                    1f, new float[]{7f, 7f}, 0f));
            g2.drawLine(startX, laneY + laneHeight - 4, finishX, laneY + laneHeight - 4);

            HorseSnapshot horse = current.isEmpty() ? null : current.get(index);
            drawLaneLabel(g2, horse, index + 1, laneY, laneHeight);
            double progress = horse == null ? 0.0 : horse.getProgress();
            int horseWidth = Math.min(52, Math.max(40, laneHeight - 2));
            int x = startX + (int) Math.round((finishX - startX - horseWidth + 9) * progress);
            int centerY = laneY + (laneHeight - 3) / 2;
            drawHorse(g2, x, centerY, horseWidth, index, horse);
        }
        drawFinishLine(g2, finishX, trackTop, trackHeight - 3);
    }

    private void drawLaneLabel(Graphics2D g2, HorseSnapshot horse, int id, int laneY, int laneHeight) {
        g2.setFont(uiFont(Font.BOLD, laneHeight < 46 ? 13 : 15));
        g2.setColor(new Color(39, 53, 76));
        g2.drawString(id + " 號馬", 20, laneY + Math.max(17, laneHeight / 2));

        if (laneHeight >= 46) {
            g2.setFont(uiFont(Font.PLAIN, 11));
            g2.setColor(new Color(88, 102, 126));
            String detail;
            if (horse == null) {
                detail = "等待起跑";
            } else if (horse.isFinished()) {
                detail = "已完賽";
            } else {
                detail = "體力 " + horse.getStaminaRemaining() + "/" + horse.getInitialStamina();
            }
            g2.drawString(detail, 20, laneY + laneHeight - 9);
        }
    }

    private void drawFinishLine(Graphics2D g2, int x, int y, int height) {
        int tile = 7;
        for (int row = 0; row < (height + tile - 1) / tile; row++) {
            for (int column = 0; column < 2; column++) {
                g2.setColor((row + column) % 2 == 0 ? new Color(31, 41, 55) : Color.WHITE);
                g2.fillRect(x + column * tile, y + row * tile, tile, Math.min(tile, y + height - (y + row * tile)));
            }
        }
        g2.setColor(new Color(185, 28, 28));
        g2.setStroke(new BasicStroke(2f));
        g2.drawLine(x - 1, y, x - 1, y + height);
        g2.setFont(uiFont(Font.BOLD, 11));
        g2.drawString("終點", x - 5, Math.max(12, y - 4));
    }

    private void drawHorse(Graphics2D g2, int x, int centerY, int width, int colorIndex, HorseSnapshot horse) {
        double scale = width / 52.0;
        int bodyW = (int) Math.round(29 * scale);
        int bodyH = (int) Math.round(15 * scale);
        int bodyX = x + (int) Math.round(7 * scale);
        int bodyY = centerY - bodyH / 2;
        Color bodyColor = HORSE_COLORS[colorIndex % HORSE_COLORS.length];

        if (horse != null && horse.isBoosting()) {
            g2.setColor(new Color(245, 158, 11, 80));
            g2.fillOval(x - 5, centerY - bodyH, width + 8, bodyH * 2);
            g2.setFont(uiFont(Font.BOLD, 11));
            g2.setColor(new Color(180, 83, 9));
            g2.drawString("x1.2", x + width - 5, centerY - bodyH / 2 - 3);
            drawLightning(g2, x + 1, centerY - bodyH);
        }

        g2.setColor(bodyColor.darker());
        g2.setStroke(new BasicStroke(Math.max(1f, (float) scale * 1.6f), BasicStroke.CAP_ROUND,
                BasicStroke.JOIN_ROUND));
        g2.drawLine(bodyX + 3, bodyY + bodyH - 1, bodyX, centerY + (int) (12 * scale));
        g2.drawLine(bodyX + bodyW - 6, bodyY + bodyH - 1,
                bodyX + bodyW - 2, centerY + (int) (12 * scale));
        g2.drawLine(bodyX + bodyW - 1, bodyY + 3, bodyX + bodyW + (int) (8 * scale),
                bodyY - (int) (6 * scale));
        g2.drawLine(bodyX + 2, bodyY + 4, x, bodyY - (int) (2 * scale));

        g2.setColor(bodyColor);
        g2.fillOval(bodyX, bodyY, bodyW, bodyH);
        int headSize = (int) Math.round(11 * scale);
        g2.fillOval(bodyX + bodyW + (int) (5 * scale), bodyY - (int) (9 * scale), headSize, headSize);

        g2.setColor(new Color(255, 255, 255, 225));
        int badge = Math.max(12, (int) Math.round(14 * scale));
        int badgeX = bodyX + bodyW / 2 - badge / 2;
        int badgeY = centerY - badge / 2;
        g2.fillOval(badgeX, badgeY, badge, badge);
        g2.setColor(new Color(31, 41, 55));
        g2.setFont(uiFont(Font.BOLD, Math.max(9, (int) Math.round(10 * scale))));
        String number = Integer.toString(colorIndex + 1);
        FontMetrics metrics = g2.getFontMetrics();
        g2.drawString(number, badgeX + (badge - metrics.stringWidth(number)) / 2,
                badgeY + (badge + metrics.getAscent() - metrics.getDescent()) / 2);
    }

    private void drawLightning(Graphics2D g2, int x, int y) {
        Polygon bolt = new Polygon();
        bolt.addPoint(x + 6, y);
        bolt.addPoint(x, y + 9);
        bolt.addPoint(x + 5, y + 9);
        bolt.addPoint(x + 2, y + 18);
        bolt.addPoint(x + 13, y + 6);
        bolt.addPoint(x + 8, y + 6);
        g2.setColor(new Color(245, 158, 11));
        g2.fillPolygon(bolt);
    }

    private static Font uiFont(int style, int size) {
        return new Font("Microsoft JhengHei", style, size);
    }
}

