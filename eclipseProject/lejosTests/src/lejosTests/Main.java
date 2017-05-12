package lejosTests;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.util.Arrays;

import lejos.hardware.lcd.LCD;
import lejos.hardware.motor.EV3LargeRegulatedMotor;
import lejos.hardware.motor.EV3MediumRegulatedMotor;
import lejos.hardware.motor.Motor;
import lejos.hardware.port.MotorPort;
import lejos.hardware.port.SensorPort;
import lejos.hardware.sensor.EV3GyroSensor;
import lejos.remote.nxt.BTConnection;
import lejos.remote.nxt.BTConnector;
import lejos.robotics.RegulatedMotor;
import lejos.robotics.SampleProvider;
import lejos.robotics.chassis.Chassis;
import lejos.robotics.chassis.Wheel;
import lejos.robotics.chassis.WheeledChassis;
import lejos.utility.Delay;
/**
 * Used for experimentation with different functions of the robot
 * Will use code snippets from this class in the real implementation
 **/


public class Main {
	  private static final double WHEEL_SIZE_EV3 = 56;

	//static RegulatedMotor mLeft = new EV3LargeRegulatedMotor(MotorPort.B);
	//static RegulatedMotor mRight = new EV3LargeRegulatedMotor(MotorPort.C);
	static RegulatedMotor arm = new EV3MediumRegulatedMotor(MotorPort.D);
	
	static Wheel leftWheel = WheeledChassis.modelWheel(new EV3MediumRegulatedMotor(MotorPort.B), WHEEL_SIZE_EV3).offset(-59).gearRatio(1);
	static Wheel rightWheel = WheeledChassis.modelWheel(new EV3MediumRegulatedMotor(MotorPort.C), WHEEL_SIZE_EV3).offset(59).gearRatio(1);
	static Chassis myChassis = new WheeledChassis( new Wheel[]{leftWheel, rightWheel}, WheeledChassis.TYPE_DIFFERENTIAL);
	/*
	
	public static void main(String [ ] args) throws IOException{
	
	LCD.drawString("Test String", 2, 4); 
	Delay.msDelay(2000);
	/*
	LCD.drawString("Connecting", 2, 4);
	
	BTConnector bt = new BTConnector();
	BTConnection conn = bt.waitForConnection(10000, 2);
	

    DataInputStream dis = conn.openDataInputStream();
    DataOutputStream dos = conn.openDataOutputStream();
    
    byte[] buf = new byte[1024];
    
    dis.read(buf, 0, 1024);
    String str = new String(buf);
    	//int n = dis.readInt();
    	//LCD.clear();
    	//LCD.drawInt(buf[0], 2, 4);   
    LCD.clear();
    LCD.drawString(str, 4,4);
    LCD.drawString(Arrays.toString(buf), 3, 6);
    dos.writeInt(42);
    dos.flush();
   
    turnLeft();

    Delay.msDelay(10000);
    
    
	
	
	
	}
	*/
	/*
	public static void main(String[] args){
		
		arm.rotate(90);
		
	}
	*/

}

