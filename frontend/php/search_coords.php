<?php
	
	$keyword = strval($_POST['query']);
	// $search_param = "{$keyword}%";
	$conn = new mysqli('localhost', 'at354323_sci', '?m^(R@14,O9C:2W' , 'at354323_scientometrics');


	$return_arr = array();

	//$sql="SELECT * FROM name_coords WHERE surname = '".$keyword."'";
	$sql="SELECT * FROM dcore_mag2 WHERE last = '".$keyword."'";

	$result = mysqli_query($conn,$sql);

	if ($result->num_rows > 0) {
		while($row = $result->fetch_assoc()) {
			$row_array['name'] = $row["name"];
			$row_array['id'] = $row["id"];
			array_push( $return_arr, $row_array );
		}
		
		echo json_encode($return_arr);
	} else {
		echo '0';
	}
	$conn->close();

?>
