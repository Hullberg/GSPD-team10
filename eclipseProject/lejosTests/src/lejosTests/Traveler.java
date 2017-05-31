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
import lejos.utility.Delay;

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


	
	public void followLine(){
			
		// turn left if white 
		if(sensors.getColID() == 6){
			LCD.drawInt(2, 4, 4);
			chassis.setVelocity(30d, -10d);
		}
		// turn right if black
		else if (sensors.getColID() == 7){
			LCD.drawInt(1, 4, 4);
			chassis.setVelocity(30d, 10d);
		}
		
	}
	public void turnLeft(){
		
		
		chassis.setVelocity(0d, -30d);
		
		//chassis.rotate(-90);
		//turn until black
		while(sensors.getColID() != 7){
			
		}
		
		//keep turning until we see white after black
		while(sensors.getColID() != 6){
			
		}
		
		//change turning direction
		chassis.setVelocity(30d, 10d);
		Delay.msDelay(400);
		// turn back until white
		while(sensors.getColID() == 7){
			
		}
		
		

	}
	
	public void turnRight(){
		
		chassis.setVelocity(30d, -10d);
		Delay.msDelay(1000);

		chassis.setVelocity(0d, 0d);
		
		chassis.setVelocity(0d, 30d);
		Delay.msDelay(1000);
		//turn until red
				while(sensors.getColID() != 0){
					
				}
				
				//keep turning until we see white after black
			//	while(sensors.getColID() != 6){
					
				//}
				
				//change turning direction
				chassis.setVelocity(30d, -10d);
		
		
	}

	public RotateMoveController getPilot() {
		return pilot;
	}	
	/*
	public static void main(String[] args){
		
		Traveler traveler = new Traveler();
		traveler.chassis.setVelocity(50d,0d);
		
		while
		
		if(traveler.sensors.getColID() ==0){
			
		}
		
		
	}
  */
	 
}
