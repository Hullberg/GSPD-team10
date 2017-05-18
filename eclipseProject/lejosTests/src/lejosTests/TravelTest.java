package lejosTests;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

import lejos.hardware.lcd.LCD;
import lejos.hardware.motor.EV3LargeRegulatedMotor;
import lejos.hardware.motor.EV3MediumRegulatedMotor;
import lejos.hardware.motor.Motor;
import lejos.hardware.port.MotorPort;
import lejos.hardware.port.SensorPort;
import lejos.hardware.sensor.EV3IRSensor;
import lejos.remote.nxt.BTConnection;
import lejos.remote.nxt.BTConnector;
import lejos.robotics.RegulatedMotor;
import lejos.robotics.SampleProvider;
import lejos.robotics.chassis.Chassis;
import lejos.robotics.chassis.Wheel;
import lejos.robotics.chassis.WheeledChassis;
import lejos.robotics.navigation.MoveController;
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
  RotateMoveController pilot;
  
  RegulatedMotor arm;
 // EV3IRSensor ir = new EV3IRSensor(SensorPort.S4);
  //SampleProvider bump = ir.getDistanceMode();	
  //float[] sample = new float[1];
  
  static Wheel leftWheel = WheeledChassis.modelWheel(new EV3MediumRegulatedMotor(MotorPort.B), WHEEL_SIZE_EV3).offset(-59).gearRatio(1);
  static Wheel rightWheel = WheeledChassis.modelWheel(new EV3MediumRegulatedMotor(MotorPort.C), WHEEL_SIZE_EV3).offset(59).gearRatio(1);
  static Chassis myChassis = new WheeledChassis( new Wheel[]{leftWheel, rightWheel}, WheeledChassis.TYPE_DIFFERENTIAL);
  
  public TravelTest(){
	  
	  this.pilot = new MovePilot(myChassis);
	  this.arm = new EV3MediumRegulatedMotor(MotorPort.D);
  }
  
  
  public void go(SensorTest sensor) {
    
    //checks if an object is closer than 20 cm, if it is: stop
    
    boolean objectInTheWay = false;
    
    while(!objectInTheWay){
    	
    	if( sensor.getDistance() < 0.2){
    		pilot.stop();
    		objectInTheWay = true;
    	}
    	
    }
    
    Delay.msDelay(3000);
  }
 
  
  public void moveForward(int slots){
	  
	  pilot.travel(50 * slots);
	  pilot.stop();
	  
  }
  
  public void turnRight(){
	  
	  pilot.rotate(90);
	  
  }
  
  
  public void turnLeft(){
	  
	  pilot.rotate(-90);
	  
  }
  public void moveCoordinates(int x, int y){
	  
	  moveForward(x);	  
	  turnLeft();	
	  moveForward(y);	  
  }
  
  
  public static void main(String[] args) throws IOException {
    TravelTest traveler = new TravelTest();
 
    //SensorTest sensor = new SensorTest();
    LCD.drawString("Connecting", 1,1 );
    BTConnector bt = new BTConnector();
	BTConnection conn = bt.waitForConnection(10000, 2);
	
    DataInputStream dis = conn.openDataInputStream();
    DataOutputStream dos = conn.openDataOutputStream();
    
    byte[] buf = new byte[24];
    
    dis.read(buf, 0, 1024);
    
    int[] coords = new int[3];
    
    traveler.pilot.setLinearAcceleration(traveler.pilot.getLinearAcceleration()/3); //trying to get smoother start and stop
    
    for(int i = 0; i < 3; i++ ){
    	
    	coords[i] = ByteBuffer.wrap(buf).getInt((4*i)); //read one int at a time from the bytebuffer
    	
    	//LCD.drawInt(coords[i], 4, i+2); //print them (debug)
    	
    }
    
    
    traveler.moveCoordinates(coords[0], coords[1]);
    
    
    dos.writeInt(42); //respond 
    dos.flush(); // to be sure the message is sent
    
    Delay.msDelay(5000);
    
   
    
    
    
    
    
  } 
  
}