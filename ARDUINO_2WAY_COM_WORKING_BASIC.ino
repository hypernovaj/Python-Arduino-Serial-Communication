/*
############################################################################
##TESTFILE FOR 2 WAY COMMUNICATION BETWEEN PYTHON AND ARDUINO             ##
##ARDUINO PART                                                            ##
##                                                                        ##
##created by Jan Meyne                                                    ##
##22.03.2022                                                              ##
############################################################################

 Python sends:
 start,indexcom+1,int_data+1,float_data+1,string_data,end\n
 Arduino sends:
 start,indexcom+2,int_data+2,float_data+2,zyx+ard,end\n
 

Teststring for the Serial Monitor of Arduino IDE:
    start,0,123,123.456,abcde,end\n

only seen as valid if full block arrives
start,transmission_index,DATA,end \n
readstring=Serial.readStringUntil("\n");
*/



//Markers for the string assembly that gets send
String starter = "start";
String ender = "end";
String commata = ",";

//initial values for teststring to return
int    Transmission_index = 0;
int    DATA_1_int = 987;
float  DATA_2_float = 789.123; 
String DATA_3_string= "zyx";
 
 
 
 void setup(){

//Begin serial Communication
  Serial.begin(9600);
//Serial communiciation listens for this amount of time for new data
  Serial.setTimeout(80);   
}

void loop(){

  //check if new data is available
  if(Serial.available() > 0 ){
    String raw_string = Serial.readString();
    
    //check if start is contained
    if(raw_string.indexOf("start") > -1)
    
    {
          //check if end is contained
         if(raw_string.indexOf("end") > -1)
        {

            //discard everything before first start
            String front_cut_raw_string = raw_string.substring(raw_string.indexOf("start"));
            
            // discard everything after first end of new substring
            String cut_string = front_cut_raw_string.substring(5,front_cut_raw_string.indexOf("end"));

            //read variables out of the cut_string
                //determine commata positions
                int first_comma   = cut_string.indexOf(",");
                int second_comma  = cut_string.indexOf(",", first_comma + 1);
                int third_comma   = cut_string.indexOf(",", second_comma + 1);
                int fourth_comma   = cut_string.indexOf(",", third_comma + 1);
                int fivth_comma   = cut_string.indexOf(",", fourth_comma + 1);
            
            //build the substrings of the variables and convert them to int and float and etc...
            //FYI: if nothing is sent in the string with start and end the variables are zero, as .toInt and .toFloat fall to zero if not convertible
            Transmission_index = cut_string.substring(first_comma+1, second_comma ).toInt();
            DATA_1_int = cut_string.substring(second_comma+1, third_comma ).toInt();
            DATA_2_float = cut_string.substring(third_comma+1, fourth_comma ).toInt();
            DATA_3_string= cut_string.substring(fourth_comma+1, fivth_comma );
                
                


            //RETURN DATA
            // add 2 to every number 
            Transmission_index=Transmission_index+2;
            DATA_1_int =DATA_1_int+2;
            DATA_2_float=DATA_2_float+2;
            DATA_3_string=DATA_3_string+"ard";
            // Send the String of data to be returned 
            // 3 times so first and last strings can be cut off and middle is still intact  
              Serial.println(starter + commata + Transmission_index + commata + DATA_1_int + commata + DATA_2_float + commata + DATA_3_string + commata + ender);
              Serial.println(starter + commata + Transmission_index + commata + DATA_1_int + commata + DATA_2_float + commata + DATA_3_string + commata + ender);
              Serial.println(starter + commata + Transmission_index + commata + DATA_1_int + commata + DATA_2_float + commata + DATA_3_string + commata + ender);

        }
        else
        {
          //end not received  
        }
    } 
    
    else
    {
      //start not received
    }
  }

  delay(100);
  //wait 100ms for new data to arrive
}
