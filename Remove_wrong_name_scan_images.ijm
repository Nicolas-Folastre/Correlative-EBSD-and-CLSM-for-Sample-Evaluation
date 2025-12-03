lines=250;

directory = getDir("");
path = directory + IJ.pad(0, 4) + "-" + IJ.pad(0, 4) + ".bmp";
print(path);
if(File.exists(path) == 1){
	print("delete");
	File.delete(path);
}
for (i = 0; i < lines; i++) {
	
	path = directory + IJ.pad(i, 4) + ".bmp";
	print(path);
if(File.exists(path) ==1){
	File.delete(path);
}
}


