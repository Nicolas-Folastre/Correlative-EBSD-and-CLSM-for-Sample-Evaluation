/* 
 *  Robot to use DifftoBlo on several folders containing 4D datasets
 *  Enter size of each dataset
 */


//where is icon of DifftoBlo on Desktop
Icon_X = 3750; Icon_Y = 50;

#@ File[] inputDir (label="Select folders", style="both")
umax=inputDir.length;

line_length = 205; column_length = 200; 								// X, Y
delay = 1500; 															// (ms)
delay_double_click = 100;												// double click fixed timer (ms)
Calculation_Time = 4000;												// (s) Estimated time of calculation + 20% at least
ddd="";
dddd="";
// Set max number  of folders to include
	/*Dialog.create("Maximum Number of Folders");
	Dialog.addNumber("MaxNumber of Folders", 1);
	Dialog.show();
	umax=Dialog.getNumber()+1;*/

//choose input data folder(s)
inputDir_ = Array.copy(inputDir);
//inputDir_ = newArray(umax);
line_length_ = newArray(umax);
column_length_ = newArray(umax);
for (u = 0; u < umax; u++) {
	//inputDir_[u]= getDirectory("Choose input directory "+u);
	Size = Find_X_Y_in_path(inputDir_[u]);
	line_length_[u] = Size[0];
	column_length_[u] = Size[1];
}
	
Dialog.create("Stack size");
for (u = 0; u < umax; u++) {
	//Dialog.addMessage("--------------------------------------------------------------------------");
	ddd=inputDir[u]+File.separator+"0001-0001.bmp";
	Dialog.addMessage(ddd);
	Dialog.addNumber("X", line_length_[u]);
	Dialog.addToSameRow();Dialog.addNumber("Y", column_length_[u]);
	ddd=ParseName(inputDir[u], "abricots");
	Dialog.addToSameRow();Dialog.addMessage(ddd);
}
Dialog.show();
for (u = 0; u < umax; u++) {
	line_length_[u] = Dialog.getNumber();
	column_length_[u] = Dialog.getNumber();
}

Array.show("title", inputDir_, line_length_, column_length_);

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
	
