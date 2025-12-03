/*   
 *  Robot to use DifftoBlo on several folders containing 4D datasets
 *  Size of each dataset is automatically detected fro folder name
 *  
 *  !! Be sure that DifftoBlo "explorer" window is (size minimized) and fit to the right side of main window (dedicated background can help)
 * TO DO : 	- Check progression with several rectangles ?
 * 			- Slack message on progress (equivalent to print  wth get Log ?)
 *          - Better timers especially for "paste in field" function
 *          
 *          MAIN ISSUE : when number of images doesn't fit 
 *          should be a function before this macro to check if all files are present, 
 *          and generate an empty image with corresponding coordinates as name (order of sequence is important)
 *          
 */


//where is icon of DifftoBlo on Desktop
Icon_X = 3750; Icon_Y = 50;

#@ File[] inputDir (label="Select folders", style="both")
umax=inputDir.length;

line_length = 205; column_length = 200; 								// X, Y
delay = 1500; 															// (ms)
delay_double_click = 100;												// double click fixed timer (ms)
Calculation_Time = 3600;		//seconds to skip the actual step (blo) 										// (s) Estimated time of calculation + 20% at least
ddd="";

//choose input data folder(s)
line_length_ = newArray(umax);
column_length_ = newArray(umax);
for (u = 0; u < umax; u++) {
	Size = Find_X_Y_in_path(inputDir[u]);
	line_length_[u] = Size[0];
	column_length_[u] = Size[1];
}
	
Dialog.create("Stack size");
for (u = 0; u < umax; u++) {
	//Dialog.addMessage("--------------------------------------------------------------------------");
	Dialog.addMessage(File.getName(inputDir[u]));
	Dialog.addNumber("X", line_length_[u]);
	Dialog.addToSameRow();Dialog.addNumber("Y", column_length_[u]);
	ddd=ParseName(inputDir[u], "_[");
	Dialog.addToSameRow();Dialog.addMessage(ddd);
}
Dialog.show();
for (u = 0; u < umax; u++) {
	line_length_[u] = Dialog.getNumber();
	column_length_[u] = Dialog.getNumber();
}

setBatchMode("hide");
for (u = 0; u < umax; u++) {
	line_length = line_length_[u];
	column_length = column_length_[u];
	print("------------------");
	print(inputDir[u]);
	print(line_length_[u], column_length_[u], ParseName(inputDir[u], "abricots"););
t1=getTime();
//Double click on icon
	double_click(Icon_X, Icon_Y);						//Icon place
	wait(1000);
// Click "next"
	click(746, 415, delay);
// Click "Select 1st image"
	click(764, 93, delay);
	wait(500);
//paste in field "path" and cick "open"
	/*paste_in_field(1010, 435, inputDir[u], 200);
	wait(500);
	click(1310, 435, delay);
	paste_in_field(1010, 435, "0001-0001.bmp", 200);
	click(1310, 435, delay);*/
	ddd=inputDir[u]+File.separator+"0001-0001.bmp";
	paste_in_field(1010, 435, ddd, 200);
	wait(500);
	click(1310, 435, delay);
	
//db click 1st image
	//wait(10000);
	//double_click(950, 160);
//wait list to appear 20s
	wait(40000);
// Click "next"
	click(746, 415, delay);
//paste X and Y in field
	paste_in_field(255, 117, line_length, 200);
	paste_in_field(338, 117, column_length, 200);
// Click "next"
	click(746, 415, delay);
// Click "next"
	click(746, 415, delay);
// Click "..."
	click(764, 369, delay);
//Click on the icon to parent folder
	wait(4000);
	click(1200, 90, delay);
	wait(4000);
//paste "path" in field
	ddd= "BLO_"+ParseName(inputDir[u], "_EDX");
	paste_in_field(1010, 435, ddd, 1000);
	wait(4000);
//click "save"
	click(1475, 435, delay);
//click "Build Block"
	click(746, 415, delay);
//Monitor the Progress bar of software
	//Method based on observation of software display to catch the moment computation is finished
	wait(5000); // wait extract button to be grey, processing
	run("Capture Screen");
	M = Find_Mean_rectangle(580, 410, 8, 8);
	close();
	end=0;
	
	for (t = 0; t < Calculation_Time; t++) {
		if (end == 0) {
			run("Capture Screen");
				if (Find_Mean_rectangle(580, 410, 8, 8) == M) {close(); wait(1000); } 
				else {close(); end=1;} //around (584 414)
		}
		//print(end+" "+t); 
		print("\\Update:["+end+" "+t+"]");
	}
	print("[waiting 20 seconds]"); // extra time before starting nex file process
	wait(20000);

//click "Close"
	click(746, 415, delay);
	wait(1000);
//Finalize
	t2=getTime();
	print("\\Update:[end of "+inputDir[u]+" ("+((t2-t1)/1000)+" s)]");
		wait(3000);
}
setBatchMode("exit and display");

//---------------------------------------------------------------FUNCTIONS---------------------------------------------------------------//


function click(X, Y, delay) {
	run("IJ Robot", "order=Left_Click x_point="+X+" y_point="+Y+" delay="+delay+" keypress=[]");
}

function double_click(X, Y) {
	run("IJ Robot", "order=Left_Click x_point="+X+" y_point="+Y+" delay="+delay_double_click+" keypress=[]");
	run("IJ Robot", "order=Left_Click x_point="+X+" y_point="+Y+" delay="+delay_double_click+" keypress=[]");
}


function paste_in_field(X, Y, value, delay) { 
	String.copy(value);
// double click on a field and paste the value
	//double click
	run("IJ Robot", "order=Left_Click x_point="+X+" y_point="+Y+" delay="+delay_double_click+" keypress=[]");
	run("IJ Robot", "order=Left_Click x_point="+X+" y_point="+Y+" delay="+delay_double_click+" keypress=[]");
	wait(delay);
	//right click and paste
	run("IJ Robot", "order=Right_Click x_point="+X+" y_point="+Y+" delay="+delay+" keypress=[]");
	run("IJ Robot", "order=Left_Click x_point="+X+30+" y_point="+Y+90+" delay="+delay+" keypress=[]");
	wait(delay);
}

function Find_X_Y_in_path(path) { 
// function description

par1 = lastIndexOf(path, "(");
par2 = lastIndexOf(path, ")");
text_par = substring(path, par1+1, par2);
vir = lastIndexOf(text_par, ",");
tir1 = indexOf(text_par, "-");
tir2 = lastIndexOf(text_par, "-");
block1 = substring(text_par, tir1+1, vir);
block2 = substring(text_par, tir2+1, lengthOf(text_par));
//X = parseInt(block2)+1;
//Y = parseInt(block1)+1;
X = parseInt(block2);
Y = parseInt(block1);
print(path);
print(X+", "+Y);
SIZE=newArray(X, Y);
return SIZE;
}

function Find_Mean_rectangle(x0, y0, w, h){
	//take coordinates of central spot and determine its diameter
	makeRectangle(x0, y0, w, h); // = place of "extract" button, that become grey during process, then "Done"
	List.setMeasurements;
	M = List.getValue("Mean"); 
	run("Select None");
	return M;
}

function ParseName(path, endstring) {
	
	endstring_= newArray("_EDX", "_extract", "_(", "EDX", "extract", "(");		
	NAME = File.getName(path);
	
	if(lengthOf(NAME) > 50){
		x = indexOf(NAME, endstring);
		if(x==-1){x = lengthOf(NAME);
			for (i = 0; i < endstring_.length; i++) { 
				if(x>indexOf(NAME, endstring_[i]) && indexOf(NAME, endstring_[i])!=-1){x = indexOf(NAME, endstring_[i]);}
			}
		}
 		if (x != -1) {NAME_cut = substring(NAME, 0, x);} 
 		else {NAME_cut = substring(NAME, 0, lengthOf(NAME));} 
	}
	else {NAME_cut = substring(NAME, 0, lengthOf(NAME));}
	
return NAME_cut;
}