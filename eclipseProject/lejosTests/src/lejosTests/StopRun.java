package lejosTests;

import lejos.hardware.Button;
import lejos.robotics.subsumption.Behavior;

public class StopRun implements Behavior {
	@SuppressWarnings("unused")
	private boolean suppressed;
	
	@Override
	public boolean takeControl() {
		return Button.getButtons() != 0;
	}

	@Override
	public void action() {
		suppressed = false;
		System.exit(0);	
	}

	@Override
	public void suppress() {
		suppressed = true;
	}

}
