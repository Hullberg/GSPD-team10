package lejosTests;

import lejos.hardware.port.SensorPort;
import lejos.hardware.sensor.EV3ColorSensor;
import lejos.hardware.sensor.EV3UltrasonicSensor;
import lejos.robotics.SampleProvider;

/**
*  from https://sourceforge.net/p/lejos/wiki/Sensor%20Framework/
**/

public class Sensors{
	
	private EV3ColorSensor colorSensor; 
	private EV3UltrasonicSensor ultraSonicSensor; 
	
	private SampleProvider distance; 
	private SampleProvider color;  
	
	
	float[] distanceSample; 
	float[] colorSample;
	
	public Sensors(){
		this.ultraSonicSensor =  new EV3UltrasonicSensor(SensorPort.S3);
		this.distance = ultraSonicSensor.getMode("Distance");
		this.distanceSample = new float[distance.sampleSize()];
		
		this.colorSensor = new EV3ColorSensor(SensorPort.S1);
		this.color = colorSensor.getMode("RGB");
		this.colorSample = new float[color.sampleSize()];
	}
	
	public float getDistance(){	
	 distance.fetchSample(distanceSample, 0);
		return distanceSample[0];
	}
	
	public float getColor(){
		color.fetchSample(colorSample, 0);
		return colorSample[0];
	}
	
	public int getColID(){
		return colorSensor.getColorID();
	}
}
