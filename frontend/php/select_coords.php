<?php
	
	$keyword = strval($_POST['query']);
	$conn = new mysqli('localhost', 'at354323_sci', '?m^(R@14,O9C:2W' , 'at354323_scientometrics');

	$return_arr = array();

	// $sql="SELECT * FROM name_coords WHERE id = ".$keyword;
	$sql="SELECT * FROM dcore_mag2 WHERE id = ".$keyword;

	$result = mysqli_query($conn,$sql);

	while($row = mysqli_fetch_array($result)) {
		// $return_arr['h_index_n'] = $row["h_index_n"];
		// $return_arr['name'] = $row["name"];
		// $return_arr['coords'] = $row["coords"];
		// $return_arr['surname'] = $row["surname"];

		$return_arr['name'] = $row["name"];
		$return_arr['coords'] = $row["frontier"];
		$return_arr['surname'] = $row["last"];
		$return_arr['type'] = $row["type"];

		// array_push( $return_arr, $row_array );
	}
		
	echo json_encode($return_arr);

	$conn->close();

?>
