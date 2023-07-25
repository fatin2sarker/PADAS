/*
 * BSD.h
 *
 *  Created on: Jul 24, 2023
 *      Author: fatin
 */

#ifndef BSD_H_
#define BSD_H_

#include "DAVE.h"                 //Declarations from DAVE Code Generation (includes SFR declaration)
#include <stdio.h>
#include <stdbool.h>

// Function declarations
void checkBlindSpot();
void radarDataProcessing(float distance, float speed);
void leftSensorDataProcessing(float distance);
void rightSensorDataProcessing(float distance);
void delay(uint32_t microseconds);

float getRadarDistance();

// NOTE: Average length of the car is 5 meters
// Blind spot detection measurement 7 meters
// The radar sensors are placed on the side mirror of the car for BSD, Parking assist.

// Thresholds for blind spot detection
#define DISTANCE_THRESHOLD 7.0 // Distance threshold in meters
#define SPEED_THRESHOLD 5.0    // Speed threshold in meters per second


#endif /* BSD_H_ */
