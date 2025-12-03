X=285.01;
Y=84.01;

R = Find_radius_V1(X, Y, 3, 0.8, 20);
print(R);

function Find_radius_V1(X, Y, r_default, part, r_max) { 
	//X, Y 			position of spot center
	//r_default		default radius
	//part			fraction of intensity representing the spot (compared to intensity in r_max)
	//r_max			area containing at least all the spot
		r=r_default;
		run("Specify...", "width=r_max height=r_max x="+X+" y="+Y+" oval constrain centered");
		List.setMeasurements; zone_max = part*(List.getValue("IntDen"));		
		found=0; 
	for (i = r_max; i > 0; i-=2) {if(found==0){
		run("Specify...", "width=i height=i x="+X+" y="+Y+" oval constrain centered");
		List.setMeasurements; if((List.getValue("IntDen")) <= zone_max){r=i/2; found=1;}}}
return r;
}
