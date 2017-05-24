package lejosTests;

import lejos.robotics.subsumption.Behavior;

public class CollisionDetector implements Behavior{
	
	private Sensors sensors;
	@SuppressWarnings("unused")
	private Boolean suppressed;
	
	public CollisionDetector(Sensors sensors){
		this.sensors = sensors;
		}

	@Override
	public boolean takeControl() {
		return sensors.getDistance() < 0.2;
	}

	@Override
	public void action() {
		suppressed = false;
		while(sensors.getDistance() <0.2){
		}
		
	}

	@Override
	public void suppress() {
		suppressed = true;
	}


}
