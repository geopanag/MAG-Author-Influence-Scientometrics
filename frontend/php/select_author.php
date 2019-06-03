<?php
	
	$keyword = strval($_POST['query']);
	$conn =new mysqli('localhost', 'at354323_sci', '?m^(R@14,O9C:2W' , 'at354323_scientometrics');

	$return_arr = array();

	$sql="SELECT * FROM hindex_mag WHERE id =".$keyword;
	$result = mysqli_query($conn,$sql);

	while($row = mysqli_fetch_array($result)) {
		// $return_arr['h_index_n'] = $row["h_index_n"];
		$return_arr['author'] = $row["author"];
		$return_arr['hindex_perc'] = $row["hindex_perc"];
		$return_arr['hindex'] = $row["hindex"];
		// array_push( $return_arr, $row_array );
	}
		
	echo json_encode($return_arr);

	$conn->close();

?>