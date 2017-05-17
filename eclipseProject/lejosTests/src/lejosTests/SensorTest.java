package lejosTests;

import lejos.hardware.ev3.LocalEV3;
import lejos.hardware.lcd.LCD;
import lejos.hardware.port.Port;
import lejos.hardware.port.SensorPort;
import lejos.hardware.sensor.EV3ColorSensor;
import lejos.hardware.sensor.EV3UltrasonicSensor;
import lejos.hardware.sensor.SensorMode;
import lejos.hardware.sensor.SensorModes;
import lejos.robotics.SampleProvider;
import lejos.utility.Delay;

public class SensorTest {
	
	//Port ultraSonicPort = LocalEV3.get().getPort("S2");
	//Port colorPort = LocalEV3.get().getPort("S1");
	
	EV3ColorSensor colorSensor = new EV3ColorSensor(SensorPort.S1);
	static EV3UltrasonicSensor ultraSonicSensor = new EV3UltrasonicSensor(SensorPort.S4);
	
	 //SensorModes ultraSonicSensor = new EV3UltrasonicSensor(SensorPort.S2);
	//SensorMode color = colorSensor.getRGBMode();
	
	
	static SampleProvider distance = ultraSonicSensor.getMode("Distance");
	//SampleProvider colorSample ;

	float[] sample = new float[distance.sampleSize()];
	
	public float getUltrasonicDistance(){	
		
	 distance.fetchSample(sample, 0);
		return sample[0];
	}
	/*
	public void setUpUltrasonicDistance(){
		
		
	}
	*/
	
/*   from https://sourceforge.net/p/lejos/wiki/Sensor%20Framework/
	// get a port instance
	Port port = LocalEV3.get().getPort("S2");

	// Get an instance of the Ultrasonic EV3 sensor
	SensorModes sensor = new EV3UltrasonicSensor(port);

	// get an instance of this sensor in measurement mode
	SampleProvider distance= sensor.getMode("Distance");

	// initialize an array of floats for fetching samples. 
	// Ask the SampleProvider how long the array should be
	float[] sample = new float[distance.sampleSize()];

	// fetch a sample
	while(true) 
	  distance.fetchSample(sample, 0);
	*/
	/*
	public static void main(String[] args){
		
		SensorTest sensT = new SensorTest();
		
		
		LCD.drawInt(distance.sampleSize(), 4, 0);
		for(int i = 0; i < 3; i++){
			
			float test = sensT.getUltrasonicDistance();		
			String t = Float.toString(test);
			
			LCD.drawString(t, 4 , i+1);
			Delay.msDelay(2000);
		}
	
		
	}
	*/
	
}
