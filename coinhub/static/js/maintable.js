"use strict";
/*jslint browser: true, continue:true */
/*global $, jQuery, Chart, historical_table */

/**
  * Creates and populates a chartjs graph for a given coin and places it
  * in the provided canvas's context.
  *
  * Inputs:
  *     coin_name - the name of the coin to generate a graph for
  *     ctx - the context of the canvas to place the chart in
  * 
  * Outputs: (none)
  * 
  **/
var createMainTableGraph = function (coin_name, ctx) {
    var graph_data = [],
        historical_data = JSON.parse(historical_table),
        time_labels = [],
        data,
        point,
        chart;

    for (data in historical_data[coin_name]) {
        if (historical_data[coin_name].hasOwnProperty(data)) {
            point = {
                x : historical_data[coin_name][data].time_collected,
                y : historical_data[coin_name][data].historical_price,
            };

            graph_data.push(point);
            time_labels.push(historical_data[coin_name][data].time_collected);
        }
    }

    chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: time_labels,
            datasets: [{
                radius: 0,
                fill: false,
                borderColor: 'rgb(255, 99, 132)',
                data: graph_data,
            }]
        },

        // Configuration options go here
        options: {
            responsive: false,
            animation: false,
            legend: {
                display: false,
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    display: false,
                    ticks: {
                        source: 'data',
                        autoSkip: false,
                    },
                }],
                yAxes: [{
                    display: false,
                }],
            },
            tooltips: {
                enabled: false,
            },
            hover: {
                mode: null,
            }
        }
    });
};