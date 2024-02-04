import {
	Table,
	TableBody,
	TableCell,
	TableContainer,
	TableHead,
	TableRow,
} from "@mui/material";
import PropTypes from "prop-types";

const metrics = [
	{
		name: "Montant Investi (€)",
		key: "montantInvest",
	},
	{
		name: "Revenue (€)",
		key: "revenue",
	},
	{
		name: "CAGR",
		key: "cagr",
	},

	{
		name: "Ecart Interquartille",
		key: "ecartInterquartille",
	},
	{
		name: "Ecart Type",
		key: "ecartType",
	},
	{
		name: "Moyenne",
		key: "moyenne",
	},
	{
		name: "Ratio Sharp",
		key: "ratioSharp",
	},
	{
		name: "Rendement Moyen",
		key: "rendementMoyen",
	},
	{
		name: "Volatilité",
		key: "volatilite",
	},
];

const IndicatorValues = ({ data }) => {
	return (
		<TableContainer sx={{marginTop: 2}} >
			<Table sx={{ minWidth: 650 }} aria-label="simple table">
				<TableHead>
					<TableRow>
						<TableCell>Métrique</TableCell>
						{data.map((indicator, index) => (
							<TableCell key={index} align="right">
								{indicator.name}
							</TableCell>
						))}
					</TableRow>
				</TableHead>
				<TableBody>
					{metrics.map((metric, index) => (
						<TableRow key={index}>
							<TableCell component="th" scope="row">
								{metric.name}
							</TableCell>
							{data.map((indicator, index) => (
								<TableCell key={index} align="right">
									{indicator[metric.key].toFixed(2)}
								</TableCell>
							))}
						</TableRow>
					))}
				</TableBody>
			</Table>
		</TableContainer>
	);
};

IndicatorValues.propTypes = {
	data: PropTypes.array.isRequired,
};

export default IndicatorValues;
