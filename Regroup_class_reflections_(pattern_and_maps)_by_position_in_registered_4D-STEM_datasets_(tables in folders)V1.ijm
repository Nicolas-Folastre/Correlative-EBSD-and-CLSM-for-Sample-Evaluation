/* Draw a projection of all reflections in table

Find classes as patterns repaeating and map them

ISSUE : a spot belong to maximum 1 class
Strategy : 	classes with too few reflections or too few positions in scan 
			should be merged with the most similar class

 */



// to select reflections to delete
#@ File[] inputDir (label="Select folders", style="both")
#@ int Mean_treshold
#@ int Prominence_treshold
umax=lengthOf(inputDir);
setBatchMode("hide");
for (u = 0; u < umax; u++) {
			directory = inputDir[u];
			print(u+"  "+inputDir[u]);
			print("Waiting for interaction with projection...");

				
			//directory=getDir("");
		filelist = getFileList(directory);	    
			if(File.exists(directory+"/"+"Results_All_Al[].csv")==1){
				Table.open(directory+"/"+"Results_All_Al[].csv");
	
	X_scan_	=Table.getColumn("X_scan"); 
	Y_scan_	=Table.getColumn("Y_scan"); 
	X_acc_	=Table.getColumn("X_acc"); 
	Y_acc_	=Table.getColumn("Y_acc");
	R_		=Table.getColumn("Radius");
	M_		=Table.getColumn("Mean");
	P_		=Table.getColumn("Prominence_pseudo");
	
	X_scan_denoised_ 	=newArray(X_acc_.length);
	Y_scan_denoised_ 	=newArray(X_acc_.length);
	X_acc_denoised_ 	=newArray(X_acc_.length);
	Y_acc_denoised_		=newArray(X_acc_.length);
	R_denoised_ 		=newArray(X_acc_.length);
	M_denoised_ 		=newArray(X_acc_.length);
	P_denoised_ 		=newArray(X_acc_.length);
	
	Table_size=Table.size;
	close("Results_All_Al[].csv");
	
	Amorphous_=newArray(X_acc_.length);
	newImage("Projection", "32-bit black", 512, 512, 1);
	Nspots=0;
	for (i = 0; i < Table_size; i++) {
		if (M_[i]>=Mean_treshold && P_[i]>=Prominence_treshold) {
			setPixel(X_acc_[i], Y_acc_[i], getPixel(X_acc_[i], Y_acc_[i])+1);
			Nspots++;}
	}
	setMinAndMax(0, 0);
	//run("Enhance Contrast", "saturated=0.35");
	run("Gaussian Blur...", "sigma=2");
	run("Find Maxima...", "prominence=0 strict exclude output=[Point Selection]");
	getSelectionCoordinates(xpoints, ypoints);
	close("Projection");
	//loop on all references
	tol_col_spots = 8; //radius to group reflections
	for (p = 0; p < xpoints.length; p++) {
		newImage("VDF_"+IJ.pad(p, 4)+"_"+xpoints[p]+"_"+ypoints[p], "32-bit black", X_scan_[Table_size-1], Y_scan_[Table_size-1], 1);
		for (i = 0; i < Table_size; i++) {
			//check distance of reflection to reference
			if (sqrt(Math.sqr(X_acc_[i]-xpoints[p])+Math.sqr(Y_acc_[i]-ypoints[p])) < tol_col_spots) { 
				setPixel(X_scan_[i]-1, Y_scan_[i]-1, 1);}
		}
		showProgress(p/xpoints.length);
	}
	run("Images to Stack", "name=Reflections_VDF  title=VDF use");
	// until here each spot has a column of reflections to belong to
	// it also belongs to several known places (1 reflection is one slice in this stack)
	
	//compare VDF similarities by XM YM of VDF
		XM_=newArray(xpoints.length);
		YM_=newArray(xpoints.length);
		M2_=newArray(xpoints.length);
		Slice_=newArray(xpoints.length);
		for (i = 1; i <= xpoints.length; i++) {
    		setSlice(i); Slice_[i-1]=i;
    		 List.setMeasurements;
    		 XM_[i-1]=List.getValue("XM");
    		 YM_[i-1]=List.getValue("YM");
    		 M2_[i-1]=List.getValue("Mean");
		}
			//close("Reflections_VDF");
		Array.sort(M2_, XM_, YM_, xpoints, ypoints,Slice_);
		Array.sort(XM_, YM_, M2_, xpoints, ypoints,Slice_);
		Array.sort(YM_, M2_, XM_, xpoints, ypoints,Slice_);
			//Array.show("title", XM_, YM_, M2_, xpoints, ypoints);
			
	//Find and draw class diffraction pattern
	tol_class = 2; // move max of radius of XM,YM to keep same class
		class_=newArray(xpoints.length); class_[0]=0;
		class=0; i=0;
		newImage("Class_"+IJ.pad(class, 4), "32-bit black", 512, 512, 1);
		setPixel(xpoints[i], ypoints[i], 1);
		for (i = 1; i < xpoints.length; i++) {			
    		 if(abs(XM_[i]-XM_[i-1]) > tol_class || abs(YM_[i]-YM_[i-1]) > tol_class){
    		 	class++;
    		    newImage("Class_"+IJ.pad(class, 4), "32-bit black", 512, 512, 1);
    		 	}
    		 class_[i]=class;
    		 setPixel(xpoints[i], ypoints[i], 1);
    	}
    	run("Images to Stack", "name=Reflections_Class  title=Class use"); 

	
	//Draw class maps
	newImage("Map_classes", "32-bit black", X_scan_[Table_size-1], Y_scan_[Table_size-1], class+1);
	selectWindow("Reflections_VDF"); N=nSlices; setPasteMode("Add");
		for (i = 1; i <= N; i++) {
	   		 selectWindow("Reflections_VDF");
	   		 setSlice(Slice_[i-1]);
	   		 run("Select All");run("Copy");
	   		 
	   		 selectWindow("Map_classes");
	   		 setSlice(class_[i-1]+1);
	   		 run("Paste");
		}
	//Compare the classes again to merge patterns of superposed dark field
	
		
	/*selectWindow("Reflections_Class");
	for (i = 1; i <= nSlices; i++) {
    	setSlice(i);
		run("Find Maxima...", "prominence=0 strict exclude output=[Point Selection]");
		run("Enlarge...", "enlarge="+5);
		Roi.setPosition(i);
		roiManager("Add");
	}
	
	n = roiManager('count');
	for (r = 0; r < n; r++) {
    	newImage("Map_class_"+IJ.pad(r, 4), "32-bit black", X_scan_[Table_size-1], Y_scan_[Table_size-1], 1);
    	for (i = 0; i < Table_size; i++) {
    		//selectWindow("Reflections_Class");
    		roiManager('select', r);
    		if(Roi.contains(X_acc_[i], Y_acc_[i]) == 1){
    			//selectWindow("Map_class_"+IJ.pad(r, 4));
    			setPixel(X_scan_[i]-1, Y_scan_[i]-1, getPixel(X_scan_[i], Y_scan_[i])+1);
    		}
    	}
	}
	run("Images to Stack", "name=Map_Classes  title=Map_class use");*/
	}
}
setBatchMode("exit and display");