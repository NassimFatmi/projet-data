import {
	Autocomplete,
	Button,
	Dialog,
	DialogActions,
	DialogTitle,
	Grid,
	TextField,
} from "@mui/material";

import PropTypes from "prop-types";
import { useState } from "react";

const AddDialog = ({ open, handleClose, addAction }) => {
	const [indicator, setIndicator] = useState({
		name: "",
		montantInitial: 0,
		montantRecurent: 0,
	});

	const handleAddClick = (e) => {
		e.preventDefault();
		addAction(indicator);
		handleClose();
	};

	return (
		<Dialog onClose={handleClose} open={open}>
			<DialogTitle>Ajouter un autre ETF</DialogTitle>
			<form onSubmit={handleAddClick}>
				<Grid container direction={"column"} spacing={2} padding={2}>
					<Grid item>
						<Autocomplete
							limitTags={1}
							options={[{ name: "AAPL" }, { name: "TSLA" }, { name: "HHH" }]}
							getOptionLabel={(option) => option.name}
							isOptionEqualToValue={(option, value) => option?.id === value?.id}
							onChange={(_, value) =>
								setIndicator({
									...indicator,
									name: value.name,
								})
							}
							renderInput={(params) => (
								<TextField
									{...params}
									label="Indicateur"
									placeholder="Nom de l'indicateur"
									required
								/>
							)}
						/>
					</Grid>

					<Grid item></Grid>
					<TextField
						required
						label="Montant Initial (€)"
						variant="outlined"
						onChange={(e) =>
							setIndicator({
								...indicator,
								montantInitial: e.target.value,
							})
						}
					/>

					<Grid item>
						<TextField
							required
							label="Montant Recurrent (€)"
							variant="outlined"
							onChange={(e) =>
								setIndicator({
									...indicator,
									montantRecurent: e.target.value,
								})
							}
						/>
					</Grid>
				</Grid>

				<DialogActions>
					<Button onClick={handleClose}>Cancel</Button>
					<Button type="submit">Ajouter</Button>
				</DialogActions>
			</form>
		</Dialog>
	);
};

// prop validation
AddDialog.propTypes = {
	handleClose: PropTypes.func.isRequired,
	addAction: PropTypes.func.isRequired,
	open: PropTypes.bool.isRequired,
};

export default AddDialog;
