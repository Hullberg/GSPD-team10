package lejosTests;

import lejos.robotics.subsumption.Behavior;

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
		
		traveler.getPilot().forward();
		
		while(!suppressed){
			Thread.yield();
		}
		traveler.getPilot().stop();
	}

	@Override
	public void suppress() {
		suppressed = true;		
	} 
	
}
