package site.viosmash.ex2;

public class Pair {
    double x1;
    double x2;

    public Pair(double v, double v1) {
        this.x1 = v;
        this.x2 = v1;
    }

    @Override
    public String toString() {
        return "Pair{" +
                "x1=" + x1 +
                ", x2=" + x2 +
                '}';
    }
}
