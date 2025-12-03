setBatchMode("hide");
LUT = getList("LUTs");
ID=getImageID();
name=getTitle();
run("Surface Plot...", "polygon=200 shade draw_axis fill smooth"); ID2=getImageID();
run("Duplicate...", "SP"); ID3=getImageID();
selectImage(ID2);
makePolygon(80,269,241,499,590,408,592,20,80,20);
run("Make Inverse"); run("Clear", "slice"); run("Select None");
selectImage(ID3);
makePolygon(80,269,241,499,590,408,592,20,80,20);
run("Clear", "slice"); run("Make Inverse"); run("Copy"); run("Select None");
for (i = 1; i < lengthOf(LUT); i++) {
	selectImage(ID2);
	run("Duplicate...", "title="+"LUT_"+IJ.pad(i, 2));
	run(LUT[i]);
	run("Apply LUT");
	run("RGB Color");
	makePolygon(80,269,241,499,590,408,592,20,80,20);
	run("Paste");
	run("Select None");
	//doWand(90, 30);
	//run("Clear", "slice");
}
run("Images to Stack", "name="+name+"_LUT title=LUT_ use");
selectImage(ID3);
close();
selectImage(ID2);
close();
//run("Tile");
setBatchMode("exit and display");




