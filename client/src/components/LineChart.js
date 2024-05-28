// LineChart.js
import React, { useContext, useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    LineElement,
    PointElement,
    LinearScale,
    Title,
    Tooltip,
    Legend,
    CategoryScale,
} from 'chart.js';
import { graphData } from '../utils/api/stock-api';
import { useLocation } from 'react-router-dom';
import StockContext from '../context/StockContext';

ChartJS.register(
    LineElement,
    PointElement,
    LinearScale,
    Title,
    Tooltip,
    Legend,
    CategoryScale
);


const LineChart = () => {
    const [graph, setGraph] = useState(null);
    const location = useLocation();


    useEffect(() => {
        const getGraphData = async () => {
            const params = new URLSearchParams(location.search);
            const symbol = params.get('query');
            console.log("symbol", symbol);
            try {
                const searchResults = await graphData(symbol);
                const result = searchResults;
                setGraph(result);
            } catch (error) {
                setGraph(null);
                console.log(error);
            }
        };

        getGraphData();
    }, [location.search]);

    function extractTimeSeriesData(timeSeries) {
        const dates = [];
        const openValues = [];

        // Iterate over each date in the time series object
        for (const date in timeSeries) {
            // Check if the property is not inherited from prototype chain
            if (timeSeries.hasOwnProperty(date)) {
                // Extract open value for each date
                const open = timeSeries[date]["1. open"];
                dates.push(date);
                openValues.push(parseFloat(open)); // Convert open value to float if necessary
            }
        }

        return { dates, openValues };
    }

    console.log("graph32243",graph);
    console.log("graph data1234", graph["Time Series (Daily)"]);
    const { dates, openValues } = extractTimeSeriesData(graph["Time Series (Daily)"]);
    console.log("dates",dates);
    console.log("open values",openValues);
    const data = {
        labels: dates || [],
        datasets: [
            {
                label: 'Transactions(in USD)',
                data: openValues || [],
                fill: false,
                backgroundColor: 'rgba(75,192,192,0.2)',
                borderColor: 'rgba(75,192,192,1)',
                tension: 0.1,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top',
            },
            title: {
                display: true,
                text: 'Current Market Trends',
            },
        },
    };

    return <Line data={data} options={options} />;
};

export default LineChart;
