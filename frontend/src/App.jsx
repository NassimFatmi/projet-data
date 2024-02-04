import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import {
	Container,
	Typography,
	Button,
	Box,
	Grid,
	Paper,
	LinearProgress,
	TextField,
} from "@mui/material";
import { useState } from "react";
import {
	ActionPriceEvolution,
	DisplayIndicators,
	LineGraph,
	SearchIndicator,
	Summary,
} from "./components";
import { API_URL } from "./constants/api";
import axios from "axios";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";

const App = () => {
	// list of indicators
	const [indicators, setIndicators] = useState([]);
	const addIndicator = (indicator) => {
		if (indicators.includes(indicator)) return;
		setIndicators([...indicators, indicator]);
	};
	const deleteIndicator = (indicator) => {
		setIndicators(indicators.filter((e) => e !== indicator));
	};

	// Money input
	const [money, setMoney] = useState({
		initial: 10000,
		recurrent: 500,
	});

	// Generate the report
	const [loading, setLoading] = useState(false);
	const [data, setData] = useState(null);
	const generateReport = async () => {
		// loading state
		setLoading(true);

		try {
			// create the body
			const body = {
				indicator: indicators.map((e) => e),
				startDate: "2010-01-01",
				endDate: "2023-01-25",
				montantInitial: money.initial.toString(),
				montantRecurant: money.recurrent.toString(),
			};

			const response = await axios.post(`${API_URL}`, body, {
				headers: {
					"Content-Type": "application/json",
					Accept: "application/json",
				},
			});

			console.log(response.data);

			setData(response.data);
		} catch (err) {
			console.error(err);
		} finally {
			setLoading(false);
		}
	};

	// Generate the regression
	const [url, setUrl] = useState({
		file: "",
	});
	const generateRegression = async () => {
		// loading state
		setLoading(true);

		try {
			// create the body
			const body = {
				indicator: indicators[0],
				startDate: "2010-01-01",
				endDate: "2023-01-25",
			};

			const response = await axios.post(`${API_URL}/reg`, body, {
				headers: {
					"Content-Type": "application/json",
					Accept: "application/json",
				},
			});

			console.log(response.data);
			setUrl(response.data);
		} catch (err) {
			console.error(err);
		} finally {
			setLoading(false);
		}
	};

	return (
		<LocalizationProvider dateAdapter={AdapterDayjs}>
			{loading && <LinearProgress />}
			<Container>
				<Typography marginTop={2} variant="h5">
					Projet Data
				</Typography>
				{/* Search for indicators */}
				<Box sx={{ marginTop: 2 }}>
					<SearchIndicator addIndicator={addIndicator} />
				</Box>
				{/* Display the selected indicators */}
				<Grid container marginTop={1} spacing={2} alignItems={"center"}>
					<Grid item>
						<TextField
							label="Montant initial"
							variant="outlined"
							size="small"
							type="number"
							fullWidth
							value={money.initial}
							onChange={(e) => setMoney({ ...money, initial: e.target.value })}
							sx={{ marginRight: 2 }}
						/>
					</Grid>
					<Grid item>
						<TextField
							label="Montant récurrent"
							variant="outlined"
							size="small"
							type="number"
							value={money.recurrent}
							fullWidth
							sx={{ marginRight: 2 }}
							onChange={(e) =>
								setMoney({ ...money, recurrent: e.target.value })
							}
						/>
					</Grid>
					<Grid item>
						<DisplayIndicators
							indicators={indicators}
							deleteIndicator={deleteIndicator}
						/>
					</Grid>
					<Grid item>
						<Button
							variant="outlined"
							onClick={generateReport}
							disabled={indicators.length === 0}
						>
							Générer le rapport
						</Button>
					</Grid>
				</Grid>
				{/* Start report */}
				<Paper
					variant="outlined"
					sx={{
						marginTop: 6,
						padding: 2,
					}}
				>
					<Typography variant="h5" marginBottom={2}>
						Évolution
					</Typography>
					{!data ? (
						<Typography variant="body2">
							Génerez le rapport pour visualiser l&apos;évolution de votre
							portefeuille
						</Typography>
					) : (
						<LineGraph data={data.variations} />
					)}
				</Paper>

				{/* Summary of the results */}
				{data && <Summary money={money} data={data} />}

				{/* Evolution de cours de l'action */}
				{data && <ActionPriceEvolution data={data.evolution} />}

				{/* Display regression */}
				<Paper
					variant="outlined"
					sx={{
						marginTop: 6,
						padding: 2,
						marginBottom: 6,
					}}
				>
					<Typography variant="h5" marginBottom={2}>
						Régression linéaire
					</Typography>

					<Grid item>
						<Button
							variant="outlined"
							onClick={generateRegression}
							disabled={indicators.length === 0}
						>
							{indicators.length === 0 ? 'Générer la régression': `Régression de ${indicators[0]}`}
						</Button>
					</Grid>
					{url.file && <img width={"100%"} src={`${API_URL}/${url.file}`} />}
				</Paper>
				{/* Button to generate regression */}
			</Container>
		</LocalizationProvider>
	);
};

export default App;
