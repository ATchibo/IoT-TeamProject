# IoT Team Project


 
![schema_2_bb](https://github.com/ATchibo/IoT-TeamProject/assets/44547421/6f6ec03d-491c-4ed3-b87b-5f2fc80b30e3)

# Setup and Build Plan

1. We use two male-female cables to link a 5V pin and a ground pin from the Raspberry to the breadboard
2. We take the ADC and place it on the breadboard like in the schema above
3. We use the appropiate cables (4 male-male, 4 male-female) to connect the Raspberry to the ADC
4. We take the moisture sensor and connect its pins to 5V, ground and the pin of the ADC corresponding to channel 1 (the second one on the left)
5. We link the ground pin of the Mosfet to the ground of the Raspberry and we link the Signal pin to the corresponding GPIO pin from the Raspberry
6. We connect the water pump and the battery to the Mosfet, then attach the hoses to the pump
7. We connect the ultrasonic sensor using the appropriate cables (3 male-female,  1 female-female) and also use a male-female cable to connect it to our rezistors
8. In the end, to complete the hardware setup, we also connect the touchscreen to the Raspberry
9. We need to put Raspberry Pi OS on our MicroSD card, which will be inserted in our Raspberry Pi
10. After we boot in Raspberry Pi OS, we need to clone this repository on our Raspberry Pi (make sure you have Python3, git setup is not mandatory but recommended)
11. We enter the project folder and run "python3 main.py", then the app should launch shortly
12. Place one tube in a water tank and in the flower pot put the other tube and the moisture sensor
13. Make sure you have the PlantBuddy app installed on your mobile phone
14. Run the app on your phone and follow the instructions
15. Enjoy!
