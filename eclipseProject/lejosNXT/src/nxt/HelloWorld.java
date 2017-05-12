package nxt;

/**
 * @author gsduong
 * @date 4/24/2017
 */

import lejos.nxt.Button;

public class HelloWorld {
  public static void main (String[] args) {
    System.out.println("Hello World");
    Button.waitForAnyPress();
  }
}