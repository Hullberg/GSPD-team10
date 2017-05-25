package lejosTests;

import lejos.robotics.subsumption.Behavior;
import lejos.utility.Delay;

public class Movement implements Behavior {
	private TravelTest traveler;
	
	private boolean suppressed;
	
	public Movement(TravelTest traveler){
		
		this.traveler = traveler;
	}

	@Override
	public boolean takeControl() {
		return true;
	}

	@Override
	public void action() {
		suppressed = false;
		
		traveler.getChassis().setVelocity(50d, 0d);
		
		
		while(!suppressed){
			traveler.followLine();
			if(traveler.sensors.getColID() == 0){
				Delay.msDelay(500);
				traveler.getChassis().rotate(90);
			}
			Thread.yield();
		}
		traveler.getChassis().stop();
	}

	@Override
	public void suppress() {
		suppressed = true;		
	} 
	
}
