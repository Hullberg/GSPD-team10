package lejosTests;

import lejos.robotics.subsumption.Arbitrator;
import lejos.robotics.subsumption.Behavior;

public class CanDetect {

	
	public static void main(String[] args){
		TravelTest traveler = new TravelTest();
		Behavior move = new Movement(traveler);
		Behavior detect = new CollisionDetector(traveler.sensors);	
		Behavior stop = new StopRun();
		Behavior[] bArray = {move, detect, stop};
	    Arbitrator arby = new Arbitrator(bArray);
	    arby.go();
	    
	
	}
	
}
