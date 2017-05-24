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
public class TravelTest {

	private static final double WHEEL_SIZE_EV3 = 56;
	private RotateMoveController pilot;

	private RegulatedMotor arm;
	// EV3IRSensor ir = new EV3IRSensor(SensorPort.S4);
	//SampleProvider bump = ir.getDistanceMode();	
	//float[] sample = new float[1];

	static Wheel leftWheel = WheeledChassis.modelWheel(new EV3LargeRegulatedMotor(MotorPort.B), WHEEL_SIZE_EV3).offset(-59).gearRatio(1);
	static Wheel rightWheel = WheeledChassis.modelWheel(new EV3LargeRegulatedMotor(MotorPort.C), WHEEL_SIZE_EV3).offset(59).gearRatio(1);
	static Chassis myChassis = new WheeledChassis( new Wheel[]{leftWheel, rightWheel}, WheeledChassis.TYPE_DIFFERENTIAL);


	Sensors sensors = new Sensors();
	
	public TravelTest(){

		this.setPilot(new MovePilot(myChassis));
		this.arm = new EV3MediumRegulatedMotor(MotorPort.D);
	}



	public void go(Sensors sensor) {

		//checks if an object is closer than 20 cm, if it is: stop

		boolean objectInTheWay = false;

		while(!objectInTheWay){

			if( sensor.getDistance() < 0.2){
				getPilot().stop();
				objectInTheWay = true;
			}

		}

		Delay.msDelay(3000);
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
		
		getPilot().forward();
/*		
		if(sensors.getColID() == 2){
			pilot.rotate(10);
		}
		else if (sensors.getColID() == 1){
			pilot.rotate(-10);		
		}
	*/	
		
		
	}



	public RotateMoveController getPilot() {
		return pilot;
	}



	public void setPilot(RotateMoveController pilot) {
		this.pilot = pilot;
	}
	
	/*
	public static void main(String[] args){
		TravelTest traveler = new TravelTest();
		//Connection conn = new Connection();
		

		
		String col = Float.toString(traveler.sensors.getColor());
		LCD.drawString(col, 4, 2);
		
		String colID = Integer.toString(traveler.sensors.getColID());
		LCD.drawString(colID, 4, 4);
	//	traveler.takeThreeCommands(conn);
		/*
    int[] coords = new int[3];

    traveler.pilot.setLinearAcceleration(traveler.pilot.getLinearAcceleration()/3); //trying to get smoother start and stop

    traveler.moveToCoordinates(coords[0], coords[1]);
    traveler.returnFromCoordinates(coords[0], coords[1]);
		 
	//	int[] co =	conn.readCoordinates();
		
		//conn.sendInt(42);
		//int[] tr = {1,2,3}; 
		//conn.sendCoordinates(tr);
		//conn.closeConnection();
		Delay.msDelay(4000);


	} 
*/
}
