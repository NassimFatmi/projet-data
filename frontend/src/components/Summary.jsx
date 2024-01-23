import { Typography, Grid, Paper } from "@mui/material";
import PropTypes from "prop-types";

const Summary = ({ data }) => {
	return (
		<>
			<Paper
				variant="outlined"
				sx={{
					marginTop: 6,
					padding: 2,
				}}
			>
				<Typography variant="h5">Résumé</Typography>
				<Grid
					sx={{ marginTop: 2 }}
					container
					justifyContent={"space-around"}
				></Grid>
			</Paper>
		</>
	);
};

// props validation
Summary.propTypes = {
	data: PropTypes.array.isRequired,
};

export default Summary;
