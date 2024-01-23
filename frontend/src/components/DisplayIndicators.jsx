import { Chip, Typography } from "@mui/material";
import { grey } from "@mui/material/colors";
import PropTypes from "prop-types";

const DisplayIndicators = ({ indicators, deleteIndicator }) => {
	return (
		<>
			{/* Display chip with option to delete with the name of the indicator */}
			{indicators.length === 0 && (
				<Typography variant="body2" color={grey[500]}>
					Aucun indicateur
				</Typography>
			)}

			{indicators.map((indicator, index) => (
				<Chip
					key={index}
					label={indicator}
					onDelete={() => deleteIndicator(indicator)}
					sx={{ margin: 0.5 }}
					color="primary"
				/>
			))}
		</>
	);
};

DisplayIndicators.propTypes = {
	indicators: PropTypes.array.isRequired,
	deleteIndicator: PropTypes.func.isRequired,
};

export default DisplayIndicators;
