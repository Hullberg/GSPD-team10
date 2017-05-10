package lejosTests;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.util.Arrays;

import lejos.hardware.lcd.LCD;
import lejos.remote.nxt.BTConnection;
import lejos.remote.nxt.BTConnector;
import lejos.utility.Delay;




public class Main {
	public static void main(String [ ] args) throws IOException{
	
	LCD.drawString("Test String", 2, 4); 
	Delay.msDelay(2000);
	
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
   
    

    Delay.msDelay(10000);
    
    
	
	
	
	}
}
