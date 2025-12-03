/* Check files in function of size
 *  size of scan is auto from path
 *  missing files are written as dark image with name of missing image in same folder.
 *  
 *  show if there is extra images
 *  
 *  TO DO : determine what is the extra image if there is (ok) and 
 *  		move it in brother_folder "waste or extra"+same name of folder
 *  
 *  /genreally acting on registred table before reconstruction would be better !
 * 
 * 
 */


images_size = 512; // px
type = ".bmp";

// input folders
#@ File[] inputDir (label="Select folders", style="both")
umax=inputDir.length;

setBatchMode("hide");
line_length_ = newArray(umax);
column_length_ = newArray(umax);
missing_count_ = newArray(umax);

for (u = 0; u < umax; u++) {
	print("------------------------------------------------------------------------------------");
	Size = Find_X_Y_in_path(inputDir[u]);
	line_length_[u] = Size[0];
	column_length_[u] = Size[1];
	filelist = getFileList(inputDir[u]);
	missing_count_[u] = line_length_[u]*column_length_[u]-filelist.length; 

	//if missing != 0 look for missing numbers
	if(missing_count_[u] == 0){print("No missing bmp images");}
	
	if(missing_count_[u] < 0){print(missing_count_[u] + " excess bmp images");
		extra_images = newArray(abs(missing_count_[u]));
		c=0; f=0;
			for (y = 1; y <= column_length_[u]; y++) {
			for (x = 1; x <= line_length_[u]; x++) {
				if(f < filelist.length){
					name=IJ.pad(y, 4)+"-"+IJ.pad(x, 4);
						if (filelist[f] != name+type) {
							extra_images[c]=filelist[f]; c++;
							if(x>1){x--;} else {y--; x=line_length_[u];}
						}
					f++;
				}			
			}
			}
		Array.print(extra_images);
		waitForUser("Remove extra files ?");
		for (extra = 0; extra < extra_images.length; extra++) {
			File.delete(inputDir[u] + File.separator + extra_images[extra]);
		}

		
	}
	if(missing_count_[u] > 0){print(missing_count_[u] + " missing bmp images");
		name = ""; 
		c = 0;
		missing_images = newArray(missing_count_[u]);
			for (x = 1; x <= line_length_[u]; x++) {
			for (y = 1; y <= column_length_[u]; y++) {
					name=IJ.pad(y, 4)+"-"+IJ.pad(x, 4);
					if (File.exists(inputDir[u] + File.separator + name + type) != 1) {
						missing_images[c] = name; c++;
						}
			}
			}
		Array.print(missing_images);
		//create missing images
		newImage("Missing_Images", "8-bit black", images_size, images_size, c);
		for (c = 1; c <= nSlices; c++) {setSlice(c); run("Set Label...", "label="+missing_images[c-1]);}
		run("Image Sequence... ", "select= dir="+inputDir[u]+" format=BMP name=[] use");
		close();
		filelist = getFileList(inputDir[u]);
		print(line_length_[u]*column_length_[u]-filelist.length + " missing images after treatment");
			
	}
}

print("End of file checking.");


	

setBatchMode("exit and display");




////// functions  //////////////////////////////

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


