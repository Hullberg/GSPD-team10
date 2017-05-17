package lejosTests;

import lejos.hardware.lcd.LCD;
import lejos.hardware.motor.EV3LargeRegulatedMotor;
import lejos.hardware.motor.EV3MediumRegulatedMotor;
import lejos.hardware.motor.Motor;
import lejos.hardware.port.MotorPort;
import lejos.hardware.port.SensorPort;
import lejos.hardware.sensor.EV3IRSensor;
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
  
  
  public void go() {
    pilot.travel(70);
    /*
    while (pilot.isMoving()) {
      bump.fetchSample(sample, 0);
      if (sample[0] < 20) pilot.stop();
    }
    */
    /*float dist = pilot.getMovement().getDistanceTraveled();
    LCD.drawString("Distance = " + dist, 2,4);
    
    */
    //pilot.travel(-50);
    
   // pilot.rotate(90, true);
    
    arm.rotate(-90); //lower the arm
    Delay.msDelay(3000);
  }
 
  
  /*
  
  public static void main(String[] args) {
    TravelTest traveler = new TravelTest();
    traveler.arm = new EV3MediumRegulatedMotor(MotorPort.D);
  //  traveler.arm = new EV3MediumRegulatedMotor(MotorPort.D);
    //traveler.arm.rotate(90);
    
    traveler.pilot = new MovePilot(myChassis);
    
    traveler.go();
  } 
  */
}