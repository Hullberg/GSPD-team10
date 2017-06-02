package lejosTests;

import lejos.hardware.lcd.LCD;
import lejos.robotics.subsumption.Behavior;
import lejos.utility.Delay;

public class Movement implements Behavior {
	private Traveler traveler;
	private Connection conn; 

	private boolean suppressed;
	
	int[] taskCoordinates = new int[6];

	private int targetX;
	private int targetY;

	private int currentX;
	private int currentY;
	
	private int fromX;
	private int fromY;
	
	private int toX;
	private int toY;
	
	private int xMax = 2;
	private int yMax = 3;
	
	

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

	private boolean returning = false;
	
	private boolean decrementY = false;

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
				
				// if robot sees red
				if(traveler.sensors.getColID() == 0){
					updatePosition();		//update position
					
					traveler.getChassis().setVelocity(0d,0d);
					
					if(shouldRobotTurnLeft()){ //then check if we should turn left but not yet at target
						traveler.turnLeft();
						LCD.drawString("turned left at 83", 0, 6);

						movingInX = !movingInX; // make sure we now that we are traveling in another direction
						LCD.drawString(String.valueOf(movingInX), 0, 7);
					}
					
					
					
					else if(atTarget()){ // if we are at target position after seeing red and position is updated
						
						if(atTo()){
							
							traveler.turnLeft();
							
							LCD.drawString("atTo", 0, 4);
							
							//Delay.msDelay(3000)
							traveler.turnRight();
						//	movingInX = !movingInX;
							targetX = currentX;
							targetY = yMax;
							
							returning = true;
						}
						
						if(atFrom()){
							traveler.turnLeft();
							
							LCD.drawString("atFrom", 0, 4);
							
							//Delay.msDelay(3000)
							traveler.turnRight();
						//	movingInX = !movingInX;
							targetX = currentX;
							targetY = yMax;
							
							returning = true;
						}
						if(atBase()){
							traveler.turnLeft();
							taskActive = false;
							decrementY = false;
							conn.sendInt(1);
							LCD.clear();
							LCD.drawString("Done!", 0, 4);
							traveler.getChassis().setVelocity(0d,0d);
							
						}
						
						if(atTopRow()){
							LCD.drawString("At top row", 0, 5);
							traveler.turnLeft();
							LCD.drawString("turned left at 114", 0, 6);
							movingInX = !movingInX;
							LCD.drawString(String.valueOf(movingInX), 0, 7);
							targetX = 0;
							targetY = yMax;
							
						}
						
						if(atTopLeftCorner()){
							LCD.drawString("At top left corner", 0, 5);
							traveler.turnLeft();
							movingInX = !movingInX;
							LCD.drawString(String.valueOf(movingInX), 0, 7);
							targetX = 0;
							targetY = 0;
							decrementY = true;
						}
						
					}
					else{
						traveler.getChassis().setVelocity(30d, 0d); //make sure we are past the red before counting again
						Delay.msDelay(1000);
						
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

	private boolean atTopLeftCorner() {
		return currentX == 0 && currentY == yMax;
	}

	private boolean atTo(){
		return currentX == toX && currentY == toY && !returning;
	}

	private boolean atFrom(){
		return currentX == fromX && currentY == fromY;
	}

	private boolean atBase(){
		return currentX == 0 && currentY == 0;
	}

	private boolean atTopRow(){
		return currentY == yMax;
	}

	private boolean atTarget() {

		return currentX == targetX && currentY == targetY;
	}

	@Override
	public void suppress() {
		suppressed = true;		
	} 


	public void getTask(){
		LCD.drawString("getting task", 0, 3);
		taskCoordinates = conn.readCoordinates();
		LCD.drawString("got task", 0, 4);  
		
		currentX = 0;
		currentY = 0;
		
		fromX = taskCoordinates[0];
		fromY = taskCoordinates[1];
		
		toX = taskCoordinates[3];
		toY = taskCoordinates[4];
		
		if(fromX == 0 && fromY == 0){  // if from is base, set target to to-coordinates 
			setTargetX(toX);
			setTargetY(toY);
		}
		else { // else target is the from-coordinates
			setTargetX(taskCoordinates[0]);
			setTargetY(taskCoordinates[1]);
		}
		taskActive = true;
	}

	public boolean shouldRobotTurnLeft(){

		if(!atTarget() && movingInX && currentX == targetX ){
			return true; 
		}
//		else if( !atTarget() && !movingInX && currentY == targetY){
//			return true;
//		}

		return false;
	}

	public void updatePosition(){		
		if(movingInX && !returning){
			LCD.clear();
			currentX++;
			LCD.drawInt(currentX, 0, 3);
			LCD.drawInt(currentY, 3, 3);
			conn.sendCoordinates(new int[]{currentX, currentY,0});
		}
		else if(decrementY){
			currentY--;
			LCD.drawInt(currentX, 0, 3);
			LCD.drawInt(currentY, 3, 3);
			conn.sendCoordinates(new int[]{currentX, currentY,0});
		}
		else if(!movingInX){
			currentY++;
			LCD.drawInt(currentX, 0, 3);
			LCD.drawInt(currentY, 3, 3);
			conn.sendCoordinates(new int[]{currentX, currentY,0});
		}
		
		else if(movingInX && returning){
			currentX--;
			LCD.drawInt(currentX, 0, 3);
			LCD.drawInt(currentY, 3, 3);
			conn.sendCoordinates(new int[]{currentX, currentY,0});
		}
		

	}

	private boolean targetIsBase() {
		return targetX == 0 && targetY == 0;
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
