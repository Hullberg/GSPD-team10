package lejosTests;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

import lejos.hardware.lcd.LCD;
import lejos.remote.nxt.BTConnection;
import lejos.remote.nxt.BTConnector;



public class Connection {
	
	DataInputStream dis;	
	DataOutputStream dos;
	
	byte[] buf = new byte[64];

	public Connection(){
		
	    LCD.drawString("Connecting", 1,1 );
	    BTConnector bt = new BTConnector();
		BTConnection conn = bt.waitForConnection(10000, 2);
		LCD.clear();
		LCD.drawString("Connected", 1, 1);
		
	    this.dis = conn.openDataInputStream();
	    this.dos = conn.openDataOutputStream();
		
	}
	
	// reads one set of coordinates (x,y,z), can be extended to read two sets, or take an int as input for offset
	public int[] readCoordinates(){
		int[] coords = new int[3];
		
		try {
			dis.read(buf, 0, 64);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		for(int i = 0; i < 3; i++ ){
	    	coords[i] = ByteBuffer.wrap(buf).getInt((4*i)); //read one int at a time from the bytebuffer   	
	    	LCD.drawInt(coords[i], 4, i+2); //print them (debug)
		}
		return coords;
	}

	public int readInt(){
		int i;
		try {
			dis.read(buf, 0, 64);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		i = ByteBuffer.wrap(buf).getInt();
		return i;
	}
   public void sendInt(int i){
	   try {
		dos.writeInt(i);
		 dos.flush();
	} catch (IOException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	  
	   
   }
   public void closeConnection(){
	   try {
		dis.close();
		dos.close();
	} catch (IOException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
	}
	   
	   
	   
   }
	
}
