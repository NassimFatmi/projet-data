import { Paper, Typography } from "@mui/material";
import LineGraph from "./LineGraph";
import PropTypes from "prop-types";

const ActionPriceEvolution = ({ data }) => {
	return (
		<Paper
			variant="outlined"
			sx={{
				marginTop: 6,
				padding: 2,
			}}
		>
			<Typography variant="h5" marginBottom={2}>
				Évolution de cours de l&apos;action
			</Typography>
			<LineGraph data={data} />
		</Paper>
	);
};

ActionPriceEvolution.propTypes = {
  data: PropTypes.array.isRequired,
};

export default ActionPriceEvolution;
