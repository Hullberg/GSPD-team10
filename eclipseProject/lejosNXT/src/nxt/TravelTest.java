package nxt;

import lejos.nxt.Button;
import lejos.nxt.Motor;
import lejos.nxt.SensorPort;
import lejos.nxt.TouchSensor;
import lejos.robotics.navigation.DifferentialPilot;

/**
 * @author gsduong
 * @date 5/8/2017
 */

public class TravelTest {

	DifferentialPilot pilot;
	TouchSensor bump = new TouchSensor(SensorPort.S1);
	
	public void go(){
		float distance = 0;
	    pilot.travel(100, true);
	    while (pilot.isMoving()) {
	      if (bump.isPressed()) {
	    	  distance = pilot.getMovement().getDistanceTraveled();
	    	  pilot.stop();
	    	  pilot.rotate(180);
	      }
	    }
	    pilot.travel((float)(distance), true);
	    System.out.println("Distance moved: " + distance);
	    Button.waitForAnyPress();
	}
	
	public static void main(String[] args) {
	    TravelTest traveler = new TravelTest();
	    traveler.pilot = new DifferentialPilot(2.25f, 5.5f, Motor.B, Motor.C);
	    traveler.go();
	}
}
