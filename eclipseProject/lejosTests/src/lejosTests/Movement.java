package lejosTests;

import lejos.robotics.subsumption.Behavior;
import lejos.utility.Delay;

public class Movement implements Behavior {
	private Traveler traveler;
	
	private boolean suppressed;
	
	
	private int x;
	private int y;
	
	private boolean taskActive;
	
	public Movement(Traveler traveler){
		
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
				//Delay.msDelay(500);
				traveler.getChassis().setVelocity(0d, 90d);
				Delay.msDelay(1000);
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
