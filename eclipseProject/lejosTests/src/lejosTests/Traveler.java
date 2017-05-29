package lejosTests;


import lejos.hardware.lcd.LCD;
import lejos.hardware.motor.EV3LargeRegulatedMotor;
import lejos.hardware.motor.EV3MediumRegulatedMotor;
import lejos.hardware.port.MotorPort;
import lejos.robotics.RegulatedMotor;
import lejos.robotics.chassis.Chassis;
import lejos.robotics.chassis.Wheel;
import lejos.robotics.chassis.WheeledChassis;
import lejos.robotics.navigation.MovePilot;
import lejos.robotics.navigation.RotateMoveController;

/**
 * Robot travels to obstacle and back again -- original comment
 * Are used for more eperimentation and tuning of parameters
 * From https://lejosnews.wordpress.com/2015/01/17/lejos-navigation-pilots/
 *  Wheeled chassis from https://lejosnews.wordpress.com/2015/05/12/lejos-navigation-the-chassis/
 */
public class Traveler {

	private static final double WHEEL_SIZE_EV3 = 56;
	private RotateMoveController pilot;

	private RegulatedMotor arm;

	private Wheel leftWheel = WheeledChassis.modelWheel(new EV3LargeRegulatedMotor(MotorPort.B), WHEEL_SIZE_EV3).offset(-59).gearRatio(1);
	private Wheel rightWheel = WheeledChassis.modelWheel(new EV3LargeRegulatedMotor(MotorPort.C), WHEEL_SIZE_EV3).offset(59).gearRatio(1);
	private Chassis chassis = new WheeledChassis( new Wheel[]{leftWheel, rightWheel}, WheeledChassis.TYPE_DIFFERENTIAL);


	Sensors sensors = new Sensors();
	
	public Traveler(){

		this.pilot = new MovePilot(chassis);
		this.arm = new EV3MediumRegulatedMotor(MotorPort.D);
	}



	public Chassis getChassis() {
		return chassis;
	}


	public void moveForward(int slots){

		getPilot().travel(50 * slots);

		getPilot().stop();

	}

	public void turnRight(){

		getPilot().rotate(90);

	}


	public void turnLeft(){

		getPilot().rotate(-90);

	}
	public void moveToCoordinates(int x, int y){

		moveForward(x);	  
		turnLeft();	
		moveForward(y);	  
	}

	public void returnFromCoordinates(int x, int y){

		turnLeft();
		moveForward(x);
		turnLeft();
		moveForward(y);
		turnLeft();

	}

	public void takeThreeCommands(Connection conn){
		
		for(int i = 0; i<3; i++){

			int command = conn.readInt();

			switch (command) {
			case 1: moveForward(5);
			break;
			case 2: turnLeft();
			break;
			case 3: moveForward(-5);
			break;
			case 4: turnRight();
			break;
			default: LCD.drawInt(command, 4,6);
			break;
			}
		}

		
	}
	
	public void followLine(){
			
		// turn right if blue 
		if(sensors.getColID() == 2){
			LCD.drawInt(2, 4, 4);
			chassis.setVelocity(50d, 5d);
		}
		// turn left if green
		else if (sensors.getColID() == 1){
			LCD.drawInt(1, 4, 4);
			chassis.setVelocity(50d, -5d);
		}
		
	}



	public RotateMoveController getPilot() {
		return pilot;
	}	
	
  
	 
}
