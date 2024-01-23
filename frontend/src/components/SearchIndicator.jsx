import { Box, Button, TextField } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import { useState } from "react";
import PropTypes from "prop-types";

const SearchIndicator = ({ addIndicator }) => {
	const [name, setName] = useState("");

	const handleAddAction = () => {
		if (name === "") return;

		addIndicator(name.toUpperCase());
		setName("");
	};

	return (
		<>
			<Box
				sx={{
					display: "flex",
					gap: 1,
				}}
			>
				<TextField
					label="ex: AAPL, TSLA.."
					variant="outlined"
					fullWidth
					value={name}
					onChange={(e) => setName(e.target.value)}
					size="small"
				/>
				<Button
					variant="outlined"
					startIcon={<AddIcon />}
					onClick={handleAddAction}
				>
					Ajouter
				</Button>
			</Box>
		</>
	);
};

SearchIndicator.propTypes = {
	addIndicator: PropTypes.func.isRequired,
};

export default SearchIndicator;
