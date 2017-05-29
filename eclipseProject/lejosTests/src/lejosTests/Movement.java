package lejosTests;

import lejos.hardware.lcd.LCD;
import lejos.robotics.subsumption.Behavior;
import lejos.utility.Delay;

public class Movement implements Behavior {
	private Traveler traveler;
	private Connection conn; 

	private boolean suppressed;


	private int targetX;
	private int targetY;

	private int currentX;
	private int currentY;

	public int getCurrentX() {
		return currentX;
	}

	public void setCurrentX(int currentX) {
		this.currentX = currentX;
	}

	public int getCurrentY() {
		return currentY;
	}

	public void setCurrentY(int currentY) {
		this.currentY = currentY;
	}

	private boolean taskActive = false;

	private boolean movingInX  = true;

	private boolean returning;

	public Movement(Traveler traveler, Connection conn){

		this.traveler = traveler;
		this.conn = conn;
	}

	@Override
	public boolean takeControl() {
		return true;
	}

	@Override
	public void action() {
		suppressed = false;
		
		

		while(!suppressed){

			if(taskActive){
				traveler.followLine();
				if(traveler.sensors.getColID() == 0){
					incrementPosition();		

					if(shouldRobotTurn()){
						//Delay.msDelay(500);
						traveler.getChassis().setVelocity(0d, 90d);
						Delay.msDelay(1000);
						movingInX = !movingInX;
					}
				}

			}
			else{
				getTask();
				LCD.drawString("got coords",0, 6);
			}
			Thread.yield();
		}

		traveler.getChassis().stop();
	}

	@Override
	public void suppress() {
		suppressed = true;		
	} 


	public void getTask(){
		LCD.drawString("getting task", 0, 3);
		int[] coords = conn.readCoordinates();
		LCD.drawString("got task", 0, 4);  

		setTargetX(coords[0]);
		setTargetY(coords[1]);

		taskActive = true;
	}

	public boolean shouldRobotTurn(){

		if(movingInX && currentX == targetX ){
			return true; 
		}
		else if(!movingInX && currentY == targetY){
			return true;
		}

		return false;
	}

	public void incrementPosition(){		
		if(movingInX){
			currentX++;
			conn.sendCoordinates(new int[]{currentX, currentY,0});
		}
		else{
			currentY++;
			conn.sendCoordinates(new int[]{currentX, currentY,0});
		}

	}

	public int getTargetX() {
		return targetX;
	}

	public void setTargetX(int targetX) {
		this.targetX = targetX;
	}

	public int getTargetY() {
		return targetY;
	}

	public void setTargetY(int targetY) {
		this.targetY = targetY;
	}


}
