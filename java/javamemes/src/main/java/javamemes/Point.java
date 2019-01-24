package javamemes;

public class Point {

    private int x_, y_;

    public Point(int x, int y) {
        x_ = x;
        y_ = y;
    }

    public Point() {
        this(0,0);
    }

    public double getX() {
        return x_;
    }

    public double getY() {
        return y_;
    }
    
    public static double distance(Point point1, Point point2) {
        double dX = point2.getX() - point1.getX();
        double dY = point2.getY() - point1.getY();
        return Math.sqrt(dX * dX + dY * dY);
    }

    public double distance(Point other) {
        return Point.distance(this, other);
    }

}