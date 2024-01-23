import { Chart } from "react-google-charts";
import PropTypes from "prop-types";

const LineGraph = ({ data }) => {
	for (let i = 1; i < data.length; i++) {
		data[i][0] = new Date(data[i][0]).toLocaleDateString();
	}

	const options = {
		legend: { position: "top" },
		explorer: {
			keepInBounds: false,
			maxZoomIn: 8.0,
		},
		chartArea: { width: "85%", height: "85%" },
		hAxis: {
			textStyle: {
				fontSize: 12,
				bold: false,
			},
			title: "Date",
			titleTextStyle: {
				fontSize: 12,
				bold: true,
			},
		},
		vAxis: {
			textStyle: {
				fontSize: 12,
				bold: false,
			},
			title: "Valeur",
		},
	};

	return (
		<Chart
			chartType="LineChart"
			width="100%"
			height="600px"
			data={data}
			options={options}
		/>
	);
};

// props validation
LineGraph.propTypes = {
	data: PropTypes.array.isRequired,
};

export default LineGraph;
