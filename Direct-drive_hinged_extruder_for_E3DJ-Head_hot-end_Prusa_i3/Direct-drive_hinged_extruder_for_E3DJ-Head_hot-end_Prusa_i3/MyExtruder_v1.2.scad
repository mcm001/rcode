x_filament = 4.4;
z_filament = 9.5;

x_idler = 10;

module mk8() {
	translate([0,0,z_filament])
	rotate_extrude(convexity = 10, $fn = 100) 
	import (file = "MyExtruder_v1.2.dxf", layer = "mk8");
}

module base() {

difference() {

	union() {
		
		// Import the 2D design
		linear_extrude(height = 3, center = false, convexity = 10)
  			import (file = "MyExtruder_v1.2.dxf", layer = "base", $fn=64);
		linear_extrude(height = 14, center = false, convexity = 10)
   			import (file = "MyExtruder_v1.2.dxf", layer = "base_top", $fn=64);
		
		// Support for the idler hinge
		translate([15.5,-15.5,0]) {
			cylinder(r=5, h=5, $fn=64);
		}
	}

	union() {
		
		// Import the 2D design
		translate([0,0,-1]) linear_extrude(height = 16, center = false, convexity = 10)
  			import (file = "MyExtruder_v1.2.dxf", layer = "base_hole", $fn=64);

		translate([0,0,z_filament])
		rotate_extrude(convexity = 10, $fn = 100) 
		import (file = "MyExtruder_v1.2.dxf", layer = "mk8ext");
		
		// Hole for the motor screws
		translate([15.5,-15.5,-1]) cylinder(r=1.5, h=16, $fn=64);
		translate([-15.5,-15.5,-1]) cylinder(r=1.5, h=16, $fn=64);
		translate([15.5,15.5,-1]) cylinder(r=1.5, h=16, $fn=64);
		translate([-15.5,15.5,-1]) cylinder(r=1.5, h=16, $fn=64);

		// motor hole 
		translate([0,0,-1]) cylinder(r=11.1, h=3, $fn=64);

		// Hole for the filament
		translate([x_filament,35,z_filament]) rotate([90,0,0]) cylinder(r=1.2, h=70, $fn=64);

		// Hole for the spring nut
		translate([6,21,9.5]) rotate([0,90,0]) cylinder(r=2, h=12, $fn=64);			
		translate([7.8,17.4,15.5]) rotate([0,90,0]) cube([10,7.2,3.2]);	

		// Hole for the hot-end
		translate([x_filament,-21,z_filament]) rotate([90,0,0]) cylinder(r=8.05, h=4.1, $fn=64);
		translate([x_filament,-25,z_filament]) rotate([90,0,0]) cylinder(r=6.05, h=6, $fn=64);
		translate([x_filament-8.05,-21,z_filament]) rotate([90,0,0]) cube([16.1, 10, 4.1]);
		translate([x_filament-6.05,-25,z_filament]) rotate([90,0,0]) cube([12.1, 10, 6]);

		// Holes for the hod-end mount screws
		translate([15.5,-26,-1]) { 
				cylinder(r=1.5, h=16, $fn=64);
				cylinder(r=3.3, h=6, $fn=6);
		}
		translate([-15.5+8,-26,-1]) {
			cylinder(r=1.5, h=16, $fn=64);
			cylinder(r=3.3, h=6, $fn=6);
		}

		// Hole for the fan mount
		translate([-17.5,-28+3.6,10]) rotate([0,90,0]) cylinder(r=2, h=8, $fn=64);	
		translate([-13.5,-28,16]) rotate([0,90,0]) cube([10,7.2,3.2]);	

	}

}
	// Import the 2D design, Add some support
		translate([0,0,0]) linear_extrude(height = 2, center = false, convexity = 10)
  			import (file = "MyExtruder_v1.2.dxf", layer = "support", $fn=64);

}

module hot_end_mount() {
difference() {

	union() {
		// Import the 2D design
		translate([0,0,14]) linear_extrude(height = 5, center = false, convexity = 10)
  			import (file = "MyExtruder_v1.2.dxf", layer = "hot_mount", $fn=64);

	}

	union() {
		
		// Hole for the hot-end
		translate([4,-20.9,z_filament-0.1]) rotate([90,0,0]) cylinder(r=8.05, h=4.2, $fn=64);
		translate([4,-25,z_filament-0.1]) rotate([90,0,0]) cylinder(r=6.05, h=6.1, $fn=64);

		translate([-25,-50, 0]) cube([50,50,12]);

		// Holes for the hod-end mount screws
		translate([15.5,-26,10]) { 
				cylinder(r=1.5, h=16, $fn=64);
				//cylinder(r=3.3, h=4, $fn=6);
		}
		translate([-15.5+8,-26,10]) {
			cylinder(r=1.5, h=16, $fn=64);
			//cylinder(r=3.3, h=4, $fn=6);
		}

	}

}

}


module idler() {

difference() {

	union() {
		
		// Import the 2D design
		linear_extrude(height = 2, center = false, convexity = 10)
  			import (file = "MyExtruder_v1.2.dxf", layer = "idler_base", $fn=64);
		linear_extrude(height = 9, center = false, convexity = 10)
   			import (file = "MyExtruder_v1.2.dxf", layer = "idler", $fn=64);
		
		// Support for the bearing
		translate([x_idler,0,0]) {
			cylinder(r=2.32, h=9, $fn=64);
			cylinder(r=3.5, h=2.2, $fn=64);
		}
	}

	union() {
		
		// Hole for the bearing screw (to be taped M3)
		//translate([x_idler,0,-1]) cylinder(r=1.47, h=12, $fn=64);

		// Hole for the hinge screw
		translate([15.5,-15.5,-1]) cylinder(r=1.5, h=12, $fn=64);

		// Hole for the filament
		translate([15,22,z_filament-5]) rotate([0,90,0]) cylinder(r=2, h=12, $fn=64);	
		translate([15,20,z_filament-5]) rotate([0,90,0]) cylinder(r=2, h=12, $fn=64);	
		translate([15,20,z_filament-3]) rotate([0,90,0]) cube([4,2,12]);	

		// Hole for the spring 
		translate([5,12,4.5]) rotate([90,0,0]) cylinder(r=1.2, h=12, $fn=64);	
		translate([0,12,3.3]) rotate([90,0,0]) cube([5,2.4,12]);	
	}

}

}
//mk8();
//base();
//translate([0,0,1]) 
//rotate([0, 180, 0]) hot_end_mount();
//translate([0,0,5]) 
idler();
%translate([x_filament,35,z_filament]) rotate([90,0,0]) cylinder(r=1.75/2, h=70, $fn=64);
