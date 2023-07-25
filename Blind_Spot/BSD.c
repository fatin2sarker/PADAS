/*
 * BSD.c
 *
 *  Created on: Jul 24, 2023
 *      Author: fatin
 */

#include "BSD.h"
#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>


// Function to create a delay in microseconds using SysTick
void delay(uint32_t microseconds)
{
    // Calculate the number of ticks needed for the given delay
    uint32_t ticks = (microseconds * SystemCoreClock) / 1000000;

    // Disable SysTick during configuration
    SysTick->CTRL = 0;

    // Load the initial value to the SysTick Timer
    SysTick->LOAD = ticks - 1;

    // Set the current value to 0
    SysTick->VAL = 0;

    // Enable SysTick with the desired clock source (usually System Clock)
    SysTick->CTRL = SysTick_CTRL_ENABLE_Msk | SysTick_CTRL_CLKSOURCE_Msk;

    // Wait for the count flag to be set (indicating the delay has elapsed)
    while ((SysTick->CTRL & SysTick_CTRL_COUNTFLAG_Msk) == 0)
    {
        // Wait
    }

    // Disable SysTick after the delay has elapsed
    SysTick->CTRL = 0;
}

// Function for blind spot detection
void checkBlindSpot()
{
    // Get radar data
    float radarDistance = getRadarDistance(); // Replace with appropriate radar data retrieval function
    float radarSpeed = getRadarSpeed();       // Replace with appropriate radar data retrieval function

    // Process radar data
    radarDataProcessing(radarDistance, radarSpeed);

    // Get sensor data
    float leftSensorDistance = getLeftSensorDistance();   // Replace with appropriate left sensor data retrieval function
    float rightSensorDistance = getRightSensorDistance(); // Replace with appropriate right sensor data retrieval function

    // Process sensor data
    leftSensorDataProcessing(leftSensorDistance);
    rightSensorDataProcessing(rightSensorDistance);
}

// Process radar data for blind spot detection
void radarDataProcessing(float distance, float speed)
{
    // Check if the target is within the blind spot
    if (distance < DISTANCE_THRESHOLD && abs(speed) > SPEED_THRESHOLD)
    {
        printf("Blind spot detected!\n");
        // Perform action here, activating an alarm or sending a warning
    }
}

// Process left sensor data for blind spot detection
void leftSensorDataProcessing(float distance)
{
    if (distance < DISTANCE_THRESHOLD)
    {
        printf("Object detected in the left blind spot!\n");
        // Perform action here, sending a warning
    }
}

// Process right sensor data for blind spot detection
void rightSensorDataProcessing(float distance)
{
    if (distance < DISTANCE_THRESHOLD)
    {
        printf("Object detected in the right blind spot!\n");
        // Perform action here, sending a warning
    }
}


// Function to get radar distance
float getRadarDistance()
{
    // ... Code to start radar measurement ...

    // Wait for DISTANCE2GOL microseconds
    delayMicroseconds(DISTANCE2GOL);

    // ... Code to read radar distance ...

    // Return the radar distance
    return radar_distance;
}

float getRadarSpeed()
{
	float radar_distance = getRadarDistance();


	float radar_speed;
	return radar_speed;
}

