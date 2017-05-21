package nxt;

import lejos.nxt.LCD;
import lejos.nxt.Motor;
import lejos.util.Delay;

/**
 * Simple test for arm motor: lift up and put down
 */

public class ArmMotorTest {

	private static void slowRotate(int angle){
		for(int i = 0; i < Math.abs(angle); i++){
			Motor.A.rotate(1 * (angle) / Math.abs(angle));
			Delay.msDelay(5);
		}
	}
	private static void liftObject(){
		slowRotate(70);
	}
	private static void releaseObject(){
		slowRotate(-70);
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		LCD.drawString("Program test arm", 0, 0);
		LCD.drawInt(Motor.A.getTachoCount(), 0, 1);
//		slowRotate(80);
		liftObject();
		LCD.drawInt(Motor.A.getTachoCount(), 0, 2);
//		slowRotate(-80);
		releaseObject();
		LCD.drawInt(Motor.A.getTachoCount(), 0, 3);
		System.exit(0);
		
	}

}
