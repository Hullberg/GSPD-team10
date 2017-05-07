package lejosTests;

import lejos.hardware.lcd.LCD;
import lejos.utility.Delay;

public class Main {
	public static void main(String [ ] args){
	
	LCD.drawString("Test String", 2, 4); 
	Delay.msDelay(5000);
	
	
	}
}
