package nxt;

import lejos.nxt.Button;
import lejos.nxt.LCD;
import lejos.nxt.LightSensor;
import lejos.nxt.Motor;
import lejos.nxt.SensorPort;

/**
 * @author XPS
 * @date 22 thg 5, 2017
 */

public class SimpleLineFollower {

	public static void main(String[] args) {
		int light = 29;

		LightSensor ls = new LightSensor(SensorPort.S3);

		while (Button.readButtons() == 0) {
			Motor.C.forward();
			Motor.B.forward();
			Motor.B.setSpeed(100);
			Motor.C.setSpeed(100);
			int dist = ls.readValue();
			LCD.clear();
			LCD.drawInt(dist, 0, 0);
			if (dist > light) {
				// Slightly turn left
				Motor.C.forward();
				Motor.B.backward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(100);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("1", 10, 0);
			}
			if (dist > light) {
				Motor.C.backward();
				Motor.B.forward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(150);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("2", 10, 0);
			}
			if (dist > light) {
				Motor.C.forward();
				Motor.B.backward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(200);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("3", 10, 0);
			}
			if (dist > light) {
				Motor.C.backward();
				Motor.B.forward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(250);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("4", 10, 0);
			}
			if (dist > light) {
				Motor.C.forward();
				Motor.B.backward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(300);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("5", 10, 0);
			}
			if (dist > light) {
				Motor.C.backward();
				Motor.B.forward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(350);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("6", 10, 0);
			}
			if (dist > light) {
				Motor.C.forward();
				Motor.B.backward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(400);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("7", 10, 0);
			}
			if (dist > light) {
				Motor.C.backward();
				Motor.B.forward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(450);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("8", 10, 0);
			}
			if (dist > light) {
				Motor.C.forward();
				Motor.B.backward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(500);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("9", 10, 0);
			}
			if (dist > light) {
				Motor.C.backward();
				Motor.B.forward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(550);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("10", 10, 0);
			}
			if (dist > light) {
				Motor.C.forward();
				Motor.B.backward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(600);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("11", 10, 0);
			}
			if (dist > light) {
				Motor.C.backward();
				Motor.B.forward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(650);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("12", 10, 0);
			}
			if (dist > light) {
				Motor.C.forward();
				Motor.B.backward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(700);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("13", 10, 0);
			}
			if (dist > light) {
				Motor.C.backward();
				Motor.B.forward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(750);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("14", 10, 0);
			}
			if (dist > light) {
				Motor.C.forward();
				Motor.B.backward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(800);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("15", 10, 0);
			}
			if (dist > light) {
				Motor.C.backward();
				Motor.B.forward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(850);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("16", 10, 0);
			}
			if (dist > light) {
				Motor.C.forward();
				Motor.B.backward();
				Motor.B.setSpeed(50);
				Motor.C.setSpeed(50);
				try {
					Thread.sleep(900);
				}
				catch (InterruptedException e) {
				}
				dist = ls.readValue();
				LCD.clear();
				LCD.drawInt(dist, 0, 0);
				LCD.drawString("17", 10, 0);
			}

			try {
				Thread.sleep(30);
			}
			catch (InterruptedException e) {
			}
		}
		Motor.C.stop();
		Motor.B.stop();
		System.exit(0);
	}
}