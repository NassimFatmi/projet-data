import { Typography, Grid, Paper } from "@mui/material";
import { IndicatorValues } from "../components";
import PropTypes from "prop-types";

const Summary = ({ data, money }) => {
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
				>
					<Grid item>
						<Typography variant="h6">
							Montant initial: {money.initial} $
						</Typography>
					</Grid>
					<Grid item>
						<Typography variant="h6">
							Montant récurrent: {money.recurrent} $
						</Typography>
					</Grid>
				</Grid>

				{/* Table with the important values */}
				<IndicatorValues data={data.indicators} />
			</Paper>
		</>
	);
};

// props validation
Summary.propTypes = {
	data: PropTypes.object.isRequired,
	money: PropTypes.object.isRequired,
};

export default Summary;
