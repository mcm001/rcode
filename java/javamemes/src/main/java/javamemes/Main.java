package javamemes;

import javamemes.Main;

public class Main{
  
  public static void main(String[] args) {
    Logger.log("hi");

    Point point1 = new Point();

    Point point2 = new Point(3,4);

    Logger.log("Distance: " + Point.distance(point1, point2));


  }
}