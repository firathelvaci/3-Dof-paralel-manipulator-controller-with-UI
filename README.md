# 3-Dof-paralel-manipulator-controller-with-UI

In our project we designed 3 serial manipulators with 2 degrees of freedom that work compatible. Also, these serial manipulators can grab from cornes of hexagonal platform, that was designed by us, and can carry our platform to the point that we want or can rotate the platform.

Thanks to image processing our end effector,which is laser engraving aparatus attached hexagonal platform With its most compact form 3 serial manipulators must be placed, in a circle which have radius is 400 mm. And the area where all functions can be fullfilled close to footprint. Designed manipulators with considering that constrain, carry at least 200 gr hexagonal platform that we design. 

Our system that controlled by position controllers, can go wanted positon with wanted velocity. Also, we used motor drivers that designed by us.

In the UI part user gives a parametric path function to the UI. And UI calcualtes points in given time period. For example if a circle path given by user, every predeterminated period the UI calculates end effector points and with these points UI calculates motor angles for every each motor and sends to the arduino. The arduino is used beacuse the arduino is used as a bridge between pic microcontrollers and PC. But we are planning to remove the arduino and use a raspberry pi instead. With this communication delay will be reduced and comminaciton can be done more reliably.

For test videos :
www.youtube.com/user/frathelvaci
