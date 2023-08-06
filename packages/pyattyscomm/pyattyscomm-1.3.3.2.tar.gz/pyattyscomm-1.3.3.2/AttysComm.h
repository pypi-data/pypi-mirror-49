class AttysComm;

#ifndef __ATTYS_COMM_H
#define __ATTYS_COMM_H


/**
 * AttysComm contains all the neccessary comms to talk to
 * the Attys on both Linux and Windows.
 *
 * 1) Instantiate the class AttyScan and do a scan
 *    It finds all paired Attys and creates separate AttysComm classes
 * 2) These classes are in in the array attysComm in AttysScan and
 *    the number of them in nAttysDevices.
 * 3) All attysComm are Threads so just start the data acquisition
 *    with start(), for example attysComm[0]->start() for the 1st Attys
 * 4) Get the data either via the RingBuffer functions or register a
 *    callback to get the data as it arrives.
 **/


#ifdef __linux__ 
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>
#include <bluetooth/rfcomm.h>
#include <sys/socket.h>
#include<sys/ioctl.h>
#include<stdio.h>
#include<fcntl.h>
#include<unistd.h>
#include<stdlib.h>
#include<termios.h>
#include <string>
#define SOCKET int
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#define Sleep(u) usleep((u*1000))
#if (defined(NDEBUG) || defined(QT_NO_DEBUG))
#define _RPT0(u,v)
#define _RPT1(u,v,w)
#else
#define _RPT0(u,v) fprintf(stderr,v)
#define _RPT1(u,v,w) fprintf(stderr,v,w)
#endif
#define OutputDebugStringW(s)
#elif _WIN32
#define _CRT_SECURE_NO_WARNINGS
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include <winsock2.h>
#include <ws2tcpip.h>
#include <winsock2.h>
#include <ws2bth.h>
#include <BluetoothAPIs.h>
#include <string>
#else
#endif

#include "attyscomm/AttysThread.h"
#include "attyscomm/base64.h"

#pragma once

// callback when a sample has arrived
struct AttysCommListener {
	// empty destructor in case of a delete
	virtual ~AttysCommListener() {};
	// provides timestamp,array of all channels
	virtual void hasSample(float,float *) = 0;
};

// type which represents the samples
typedef float* sample_p;

// callback when an error has occurred
struct AttysCommError {
	// provides error number and a text message about the error
	virtual void hasError(int,const char*) = 0;
};


///////////////////////////////////////////////////////////////////
// AttysComm takes a socket as an argument (Linux or Windows)
// and then connects to the Attys


class AttysComm : public AttysThread
{
public:
	/////////////////////////////////////////////////
	// Constructor: takes the bluetooth device as an argument
	// it then tries to connect to the Attys
	AttysComm(SOCKET _btsocket);

	~AttysComm();

public:

	static const int NCHANNELS = 8;

	// index numbers of the channels returned in the data array
	static const int INDEX_Acceleration_X = 0;
	static const int INDEX_Acceleration_Y = 1;
	static const int INDEX_Acceleration_Z = 2;
	static const int INDEX_Magnetic_field_X = 3;
	static const int INDEX_Magnetic_field_Y = 4;
	static const int INDEX_Magnetic_field_Z = 5;
	static const int INDEX_Analogue_channel_1 = 6;
	static const int INDEX_Analogue_channel_2 = 7;

	// descriptions the channels in text form
	const std::string CHANNEL_DESCRIPTION[NCHANNELS] = {
		"Acceleration X",
		"Acceleration Y",
		"Acceleration Z",
		"Magnetic field X",
		"Magnetic field Y",
		"Magnetic field Z",
		"Analogue channel 1",
		"Analogue channel 2"
	};

	// descriptions of the channels in text form
	const std::string CHANNEL_SHORT_DESCRIPTION[NCHANNELS] = {
		"Acc X",
		"Acc Y",
		"Acc Z",
		"Mag X",
		"Mag Y",
		"Mag Z",
		"ADC 1",
		"ADC 2"
	};

	// units of the channels
	std::string const CHANNEL_UNITS[NCHANNELS] = {
		"m/s^2",
		"m/s^2",
		"m/s^2",
		"T",
		"T",
		"T",
		"V",
		"V"
	};

	///////////////////////////////////////////////////////////////////
	// ADC sampling rate and for the whole system
	static const int ADC_RATE_125HZ = 0;
	static const int ADC_RATE_250HZ = 1;
	static const int ADC_RATE_500Hz = 2;
	static const int ADC_DEFAULT_RATE = ADC_RATE_250HZ;
	// array of the sampling rates converting the index
	// to the actual sampling rate
	const int ADC_SAMPLINGRATE[4] = { 125, 250, 500, 1000 };
	// the actual sampling rate in terms of the sampling rate index
	int adc_rate_index;

	void setAdc_samplingrate_index(int idx) {
		adc_rate_index = idx;
	}

	// get the sampling rate in Hz (not index number)
	int getSamplingRateInHz() {
		return ADC_SAMPLINGRATE[adc_rate_index];
	}

	int getAdc_samplingrate_index() {
		return adc_rate_index;
	}


	////////////////////////////////////////////////////////////////////////////
	// ADC gain
	// the strange numbering scheme comes from the ADC's numbering
	// scheme. Index=0 is really a gain factor of 6
	// On the ATttys we refer to channel 1 and 2 which are 0 and 1 here for
	// indexing.
	static const int ADC_GAIN_6 = 0;
	static const int ADC_GAIN_1 = 1;
	static const int ADC_GAIN_2 = 2;
	static const int ADC_GAIN_3 = 3;
	static const int ADC_GAIN_4 = 4;
	static const int ADC_GAIN_8 = 5;
	static const int ADC_GAIN_12 = 6;
	// mapping between index and actual gain
	const int ADC_GAIN_FACTOR[7] = { 6, 1, 2, 3, 4, 8, 12 };
	// the voltage reference of the ADC in volts
	const float ADC_REF = 2.42F;

	float getADCFullScaleRange(int channel) {
		switch (channel) {
		case 0:
			return ADC_REF / ADC_GAIN_FACTOR[adc0_gain_index];
		case 1:
			return ADC_REF / ADC_GAIN_FACTOR[adc1_gain_index];
		default:
			fprintf(stderr, "getADCFullScaleRange wrong index\n");
			exit(1);
		}
		return 0;
	}

	void setAdc0_gain_index(int idx) {
		adc0_gain_index = idx;
	}

	void setAdc1_gain_index(int idx) {
		adc1_gain_index = idx;
	}

	// initial gain factor is 1 for both channels
	int adc0_gain_index = ADC_GAIN_1;
	int adc1_gain_index = ADC_GAIN_1;


	/////////////////////////////////////////////////////////////////////
	// Bias currents for resistance measurement
	// selectable bias current index numbers for the ADC inputs
	// used to measure resistance
	static const int ADC_CURRENT_6NA = 0;
	static const int ADC_CURRENT_22NA = 1;
	static const int ADC_CURRENT_6UA = 2;
	static const int ADC_CURRENT_22UA = 3;
	int current_index = 0;
	int current_mask = 0;

	// sets the bias current which can be switched on
	void setBiasCurrent(int currIndex) {
		current_index = currIndex;
	}

	// gets the bias current as in index
	int getBiasCurrent() {
		return current_index;
	}

	// switches the currents on
	void enableCurrents(int pos_ch1, int neg_ch1, int pos_ch2) {
		current_mask = 0;
		if (pos_ch1) {
			current_mask = (int)(current_mask | (int)0b00000001);
		}
		if (neg_ch1) {
			current_mask = (int)(current_mask | (int)0b00000010);
		}
		if (pos_ch2) {
			current_mask = (int)(current_mask | (int)0b00000100);
		}
	}


	//////////////////////////////////////////////////////////////////////////////
	// selectable different input mux settings
	// for the ADC channels
	static const int ADC_MUX_NORMAL = 0;
	static const int ADC_MUX_SHORT = 1;
	static const int ADC_MUX_SUPPLY = 3;
	static const int ADC_MUX_TEMPERATURE = 4;
	static const int ADC_MUX_TEST_SIGNAL = 5;
	static const int ADC_MUX_ECG_EINTHOVEN = 6;
	int adc0_mux_index;
	int adc1_mux_index;

	void setAdc0_mux_index(int idx) {
		adc0_mux_index = idx;
	}

	void setAdc1_mux_index(int idx) {
		adc1_mux_index = idx;
	}


	///////////////////////////////////////////////////////////////////////////////
	// Temperature
	static float phys2temperature(float volt) {
		return (float)((volt - 145300E-6) / 490E-6 + 25);
	}


	///////////////////////////////////////////////////////////////////////////////
	// accelerometer
	static const int ACCEL_2G = 0;
	static const int ACCEL_4G = 1;
	static const int ACCEL_8G = 2;
	static const int ACCEL_16G = 3;
	const float oneG = 9.80665F; // m/s^2
	const float ACCEL_FULL_SCALE[4] = { 2 * oneG, 4 * oneG, 8 * oneG, 16 * oneG }; // m/s^2
	int accel_full_scale_index;

	float getAccelFullScaleRange() {
		return ACCEL_FULL_SCALE[accel_full_scale_index];
	}

	void setAccel_full_scale_index(int idx) {
		accel_full_scale_index = idx;
	}


	///////////////////////////////////////////////////
	// magnetometer
	//
	const float MAG_FULL_SCALE = 4800.0E-6F; // TESLA

	float getMagFullScaleRange() {
		return MAG_FULL_SCALE;
	}


	////////////////////////////////////////////////
	// timestamp stuff as double
	// note this might drift in the long run
	void setTimestamp(double ts) {
		timestamp = ts;
	}

	double getTimestamp() {
		return timestamp;
	}


	////////////////////////////////////////////////
	// sample counter
	long sampleNumber = 0;

	long getSampleNumber() {
		return sampleNumber;
	}

	void setSampleNumber(long sn) {
		sampleNumber = sn;
	}


	///////////////////////////////////////////////////////////////////////
	// message listener
	// sends error/success messages back
	// for MessageListener
	// here are the messages:
	static const int MESSAGE_CONNECTED = 0;
	static const int MESSAGE_ERROR = 1;
	static const int MESSAGE_RETRY = 2;
	static const int MESSAGE_CONFIGURE = 3;
	static const int MESSAGE_STARTED_RECORDING = 4;
	static const int MESSAGE_STOPPED_RECORDING = 5;
	static const int MESSAGE_CONNECTING = 6;

	////////////////////////////////////////////
	// connection info
	int hasActiveConnection() {
		return isConnected;
	}

	int hasFatalError() {
		return fatalError;
	}


	/////////////////////////////////////////////////
	// ringbuffer keeping data for chunk-wise plotting
	sample_p getSampleFromBuffer();

	int hasSampleAvailable() {
		return (inPtr != outPtr);
	}

	// spelling mishtake in previous versions
	int hasSampleAvilabale() { return hasSampleAvailable(); }

public:
	////////////////////////////////////////////////
	// Realtime callback function which is called
	// whenever a sample has arrived.
        // Implemented as an interface
	
	// Register a callback
	void registerCallback(AttysCommListener* f) {
		callbackInterface = f;
	}

	// Unregister the callback
	void unregisterCallback() {
		callbackInterface = NULL;
	}

private:
	AttysCommListener* callbackInterface = NULL;

	
public:
	////////////////////////////////////////////////
	// Callback function which is called
	// whenever an error has occurred
        // Implemented as an interface
	
	// Register a callback
	void registerErrorCallback(AttysCommError* f) {
		attysCommError = f;
	}

	// Unregister the callback
	void unregisterErrorCallback() {
		attysCommError = NULL;
	}

private:
	AttysCommError* attysCommError = NULL;

	
private:
	///////////////////////////////////////////////////////
	// from here it's private
	SOCKET btsocket;
	int doRun = 0;
	// ringbuffer
	float** ringBuffer;
	// number of entries in the ringbuffer
	const int nMem = 10000;
	int inPtr = 0;
	int outPtr = 0;
	int isConnected = 0;
	int fatalError = 0;
	int* adcMuxRegister;
	int* adcGainRegister;
	int* adcCurrNegOn;
	int* adcCurrPosOn;
	int expectedTimestamp = 0;
	int correctTimestampDifference = 0;
	double timestamp = 0.0; // in secs
	int connectionEstablished;
	long* data;
	char* raw;
	float* sample;
	char* inbuffer;

	void sendSyncCommand(const char *message, int checkOK);

	void sendSamplingRate();

	void sendFullscaleAccelRange();

	void sendCurrentMask();

	void sendBiasCurrent();

	void sendGainMux(int channel, int gain, int mux);

	void setADCGain(int channel, int gain) {
		sendGainMux(channel, gain, adcMuxRegister[channel]);
	}

	void setADCMux(int channel, int mux) {
		sendGainMux(channel, adcGainRegister[channel], mux);
	}

	void sendInit();

	void run();

	public:
	/* Call this from the main activity to shutdown the connection */
	void quit() {
		doRun = false;
	}
};


#endif
