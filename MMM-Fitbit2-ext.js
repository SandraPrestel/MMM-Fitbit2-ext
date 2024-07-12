/* global Module */

/* Magic Mirror
 * Module: MMM-Fitbit2-ext
 *
 * Forked from MMM-fitbit by Sam Vendittelli
 * MMM-Fitbit2 modifications by Mike Roberts
 * Forked from MMM-Fitbit2
 * MMM-Fitbit2-ext modifications by Sandra Prestel
 * MIT Licensed.
 */

Module.register("MMM-Fitbit2-ext", {
	// Initial values
	userData: {
		steps: {
			day1: {
				weekday: 'Mo',
				value: 0,
				goal: 10000,
			},
			day2: {
				weekday: 'Tu',
				value: 0,
				goal: 10000,
			},
			day3: {
				weekday: 'We',
				value: 0,
				goal: 10000,
			},
			day4: {
				weekday: 'Th',
				value: 0,
				goal: 10000,
			},
			day5: {
				weekday: 'Fr',
				value: 0,
				goal: 10000,
			},
			day6: {
				weekday: 'Sa',
				value: 0,
				goal: 10000,
			},
			day7: {
				weekday: 'Su',
				value: 0,
				goal: 10000,
			},
			unit: "steps"
		},
		caloriesOut: {
			day1: {
				weekday: 'Mo',
				value: 0,
				goal: 2000,
			},
			day2: {
				weekday: 'Tu',
				value: 0,
				goal: 2000,
			},
			day3: {
				weekday: 'We',
				value: 0,
				goal: 2000,
			},
			day4: {
				weekday: 'Th',
				value: 0,
				goal: 2000,
			},
			day5: {
				weekday: 'Fr',
				value: 0,
				goal: 2000,
			},
			day6: {
				weekday: 'Sa',
				value: 0,
				goal: 2000,
			},
			day7: {
				weekday: 'Su',
				value: 0,
				goal: 2000,
			},
			unit: "cals"
		},
		distance: {
			day1: {
				weekday: 'Mo',
				value: 0,
				goal: 5,
			},
			day2: {
				weekday: 'Tu',
				value: 0,
				goal: 5,
			},
			day3: {
				weekday: 'We',
				value: 0,
				goal: 5,
			},
			day4: {
				weekday: 'Th',
				value: 0,
				goal: 5,
			},
			day5: {
				weekday: 'Fr',
				value: 0,
				goal: 5,
			},
			day6: {
				weekday: 'Sa',
				value: 0,
				goal: 5,
			},
			day7: {
				weekday: 'Su',
				value: 0,
				goal: 5,
			},
			unit: "km"
		},
		activeMinutes: {
			day1: {
				weekday: 'Mo',
				value: 0,
				goal: 30,
			},
			day2: {
				weekday: 'Tu',
				value: 0,
				goal: 30,
			},
			day3: {
				weekday: 'We',
				value: 0,
				goal: 30,
			},
			day4: {
				weekday: 'Th',
				value: 0,
				goal: 30,
			},
			day5: {
				weekday: 'Fr',
				value: 0,
				goal: 30,
			},
			day6: {
				weekday: 'Sa',
				value: 0,
				goal: 30,
			},
			day7: {
				weekday: 'Su',
				value: 0,
				goal: 30,
			},
			unit: "mins"
		},
		restingHeart: {
			day1: {
				weekday: 'Mo',
				value: 0,
				goal: 60,
			},
			day2: {
				weekday: 'Tu',
				value: 0,
				goal: 60,
			},
			day3: {
				weekday: 'We',
				value: 0,
				goal: 60,
			},
			day4: {
				weekday: 'Th',
				value: 0,
				goal: 60,
			},
			day5: {
				weekday: 'Fr',
				value: 0,
				goal: 60,
			},
			day6: {
				weekday: 'Sa',
				value: 0,
				goal: 60,
			},
			day7: {
				weekday: 'Su',
				value: 0,
				goal: 60,
			},
			unit: "bpm"
		},
		water: {
			day1: {
				weekday: 'Mo',
				value: 0,
				goal: 2000,
			},
			day2: {
				weekday: 'Tu',
				value: 0,
				goal: 2000,
			},
			day3: {
				weekday: 'We',
				value: 0,
				goal: 2000,
			},
			day4: {
				weekday: 'Th',
				value: 0,
				goal: 2000,
			},
			day5: {
				weekday: 'Fr',
				value: 0,
				goal: 2000,
			},
			day6: {
				weekday: 'Sa',
				value: 0,
				goal: 2000,
			},
			day7: {
				weekday: 'Su',
				value: 0,
				goal: 2000,
			},
			unit: "ml"
		},
		caloriesIn: {
			day1: {
				weekday: 'Mo',
				value: 0,
				goal: 2000,
			},
			day2: {
				weekday: 'Tu',
				value: 0,
				goal: 2000,
			},
			day3: {
				weekday: 'We',
				value: 0,
				goal: 2000,
			},
			day4: {
				weekday: 'Th',
				value: 0,
				goal: 2000,
			},
			day5: {
				weekday: 'Fr',
				value: 0,
				goal: 2000,
			},
			day6: {
				weekday: 'Sa',
				value: 0,
				goal: 2000,
			},
			day7: {
				weekday: 'Su',
				value: 0,
				goal: 2000,
			},
			unit: "cals"
		},
		sleep: {
			day1: {
				weekday: 'Mo',
				value: 0,
				goal: 8000,
			},
			day2: {
				weekday: 'Tu',
				value: 0,
				goal: 8000,
			},
			day3: {
				weekday: 'We',
				value: 0,
				goal: 8000,
			},
			day4: {
				weekday: 'Th',
				value: 0,
				goal: 8000,
			},
			day5: {
				weekday: 'Fr',
				value: 0,
				goal: 8000,
			},
			day6: {
				weekday: 'Sa',
				value: 0,
				goal: 8000,
			},
			day7: {
				weekday: 'Su',
				value: 0,
				goal: 8000,
			},
			unit: "" // Formatted as HH:MM - no explicit unit
		}
	},

	// Default module config.
	defaults: {
		credentials: {
			clientId: "",
			clientSecret: ""
		},
		resources: [
			"steps",
			"distance",
			"activeMinutes",
			"caloriesOut",
			"caloriesIn",
			"water",
			"restingHeart",
			"sleep"
		],
		debug: false,
		test: false,
		showLastSynced: false,
		updateInterval: 10,
		pythonPath: "python3"	// set this in config.js if you use a virtual environment
	},

	// Define required scripts.
	getStyles: function() {
		return ["MMM-Fitbit2-ext.css"];
	},

	// Get the needed scripts to make graphs.
    getScripts: function () {
        return ["modules/" + this.name + "/node_modules/chart.js/dist/Chart.min.js"];
    },

	// Override socket notification handler.
	socketNotificationReceived: function(notification, payload) {
		if (notification === "API_DATA_RECEIVED") {
			Log.log("Data received")

			if (payload.clientId != this.config.credentials.clientId) {
				// Not for this user
				return
			}

			Log.log("Writing to internal storage...")

			// if the resource sent within the payload is used, write its data into the global variable userData
			resource = payload.resource;
			if (this.inResources(resource)) {
				// TODO: put this into a loop
				this.userData[resource]["day1"]["weekday"] = payload.values.day1.weekday;
				this.userData[resource]["day1"]["value"] = payload.values.day1.data;
				this.userData[resource]["day1"]["goal"] = payload.values.day1.goal;

				this.userData[resource]["day2"]["weekday"] = payload.values.day2.weekday;
				this.userData[resource]["day2"]["value"] = payload.values.day2.data;
				this.userData[resource]["day2"]["goal"] = payload.values.day2.goal;

				this.userData[resource]["day3"]["weekday"] = payload.values.day3.weekday;
				this.userData[resource]["day3"]["value"] = payload.values.day3.data;
				this.userData[resource]["day3"]["goal"] = payload.values.day3.goal;

				this.userData[resource]["day4"]["weekday"] = payload.values.day4.weekday;
				this.userData[resource]["day4"]["value"] = payload.values.day4.data;
				this.userData[resource]["day4"]["goal"] = payload.values.day4.goal;

				this.userData[resource]["day5"]["weekday"] = payload.values.day5.weekday;
				this.userData[resource]["day5"]["value"] = payload.values.day5.data;
				this.userData[resource]["day5"]["goal"] = payload.values.day5.goal;

				this.userData[resource]["day6"]["weekday"] = payload.values.day6.weekday;
				this.userData[resource]["day6"]["value"] = payload.values.day6.data;
				this.userData[resource]["day6"]["goal"] = payload.values.day6.goal;

				this.userData[resource]["day7"]["weekday"] = payload.values.day7.weekday;
				this.userData[resource]["day7"]["value"] = payload.values.day7.data;
				this.userData[resource]["day7"]["goal"] = payload.values.day7.goal;

				Log.log("Wrote " + resource);
			}
		}
		if (notification === "UPDATE_VIEW") {
			Log.log("Updating DOM");
			this.loaded = true;
			this.updateDom(this.fadeSpeed);
		}
	},

	getData: function(trigger) {
		payload = {};
		payload.config = this.config;
		payload.trigger = trigger;
		this.sendSocketNotification("GET DATA", payload);
	},

	// Initialisation
	start: function() {
		Log.info("Starting module: " + this.name);
		this.getData("Initial");

		this.loaded = false;
		this.fadeSpeed = 500;

		// Schedule update interval.
		var self = this;
		setInterval(function() {
			self.updateData();
		}, this.config.updateInterval*60*1000);
	},

	// Updates the data from fitbit
	updateData: function() {
		this.getData("Update");
	},

	// Checks whether the user wants to lookup a resource type
	inResources: function(resource) {
		return this.config.resources.indexOf(resource) > -1;
	},

	// Generate div for icon
	iconDiv: function(resource) {
		const iconPath = "/img/" + resource + ".png";

		var iconDiv = document.createElement("img");
		iconDiv.className = "widgeticon";
		iconDiv.src = "modules/" + this.name + iconPath;

		return iconDiv
	},

	// Add commas to step and calorie count
	formatNumberWithCommas: function(number) {
		return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
	},

	// Converts minutes into HH:MM
	formatMinsToHourMin: function(number) {
		hours = Math.floor(number / 60);
		minutes = number % 60;
		return ("00" + hours.toString()).slice(-2) + ":" + ("00" + minutes.toString()).slice(-2);
	},

	// Standard Doughnut chart for most resources
	StandardChart: function(value, goal) {
		var chart = document.createElement("div");
		chart.className = "chart";
		chart.style.width = "50px";		//TODO: move to CSS
		chart.style.height = "50px";	//TODO: move to CSS

		var ctx = document.createElement("canvas");
		chart.appendChild(ctx);

		// make sure that goal is not empty
		if (goal > 0) {
			nonZeroGoal = goal;
		} else {
			// if there is no goal, set value = goal
			nonZeroGoal = value
		}

		timesReached = Math.floor(value/nonZeroGoal);

		if (timesReached==0){
			backgroundColorFull = 'rgb(30, 136, 229)';
			backgroundColorEmpty = 'rgb(255,255,255)';

			chartValue = value;
			chartRemaining = nonZeroGoal - value;

		} else if (timesReached==1) {
			backgroundColorFull = 'rgb(147, 219, 64)';
			backgroundColorEmpty = 'rgb(30, 136, 229)';

			chartValue = value - nonZeroGoal;
			chartRemaining = nonZeroGoal - chartValue;
	
		} else {
			// if the goal has been reached at least 2 times, make full circle green
			backgroundColorFull = 'rgb(147, 219, 64)';
			backgroundColorEmpty = 'rgb(147, 219, 64)';

			chartValue = 100;
			chartRemaining = 0;
		}

		chartObject = new Chart(ctx, {
			type: 'doughnut',
			data: {
				labels: [
				  'value',
				  'goal'
				],
				datasets: [{
				  label: 'Chart',
				  data: [chartValue, chartRemaining],
				  backgroundColor: [
					backgroundColorFull,
					backgroundColorEmpty
				  	]
				}]
			},
			options: {
				legend: {display: false}, 
			  	tooltips: {enabled: false}
			}
		  });

		  return chart;
	},

	// Heart Rate doesn't have a goal to be reached in percent, so it is only heart symbol
	HeartRateChart: function(value){
		var heartDiv = document.createElement("div");
		heartDiv.className = "heartElement";

		if (value > 0){
			heartIcon = '<i class="fa-solid fa-heart"></i>';
		} else {
			heartIcon = '<i class="fa-regular fa-heart"></i>';
		}

		heartDiv.innerHTML = '<p> ' + heartIcon + '</p>';

		return heartDiv;
	},

	// Create a chart representing the value reached per goal for a day, with day above and number below
	ChartElement: function(resource, day, value, goal) {

		var chartDiv = document.createElement("div");
		chartDiv.className = "chartelement";

		// Day
		var dayDiv = document.createElement("div");
		dayDiv.innerHTML = day;
		chartDiv.appendChild(dayDiv);

		// Chart
		if (resource == "restingHeart") {
			chartDiv.appendChild(this.HeartRateChart(value));
		} else {
			chartDiv.appendChild(this.StandardChart(value, goal));
		}

		// Value
		var dataValueDiv = document.createElement("div");
		dataValueDiv.className = "chartvalue";

		if (["steps", "caloriesOut", "caloriesIn"].indexOf(resource) > -1) {
			dataValueDiv.innerHTML = this.formatNumberWithCommas(value);
		} else if (resource == "sleep") {
			dataValueDiv.innerHTML = this.formatMinsToHourMin(value);
		} else {
			dataValueDiv.innerHTML = value;
		}

		chartDiv.appendChild(dataValueDiv);

		return chartDiv;

	},

	// Create a row of charts (one chart per day), preceded by the icon
	ChartRowElement: function(resource){
		var chartRowDiv = document.createElement("div");
		chartRowDiv.className = "chartrow";

		// add icon
		chartRowDiv.appendChild(this.iconDiv(resource));

		//TODO: make this in a loop
		day1chart = this.ChartElement(resource, this.userData[resource]["day1"]['weekday'], this.userData[resource]["day1"]["value"], this.userData[resource]["day1"]["goal"]);
		chartRowDiv.appendChild(day1chart);

		day2chart = this.ChartElement(resource, this.userData[resource]["day2"]['weekday'], this.userData[resource]["day2"]["value"], this.userData[resource]["day2"]["goal"]);
		chartRowDiv.appendChild(day2chart);

		day3chart = this.ChartElement(resource, this.userData[resource]["day3"]['weekday'], this.userData[resource]["day3"]["value"], this.userData[resource]["day3"]["goal"]);
		chartRowDiv.appendChild(day3chart);

		day4chart = this.ChartElement(resource, this.userData[resource]["day4"]['weekday'], this.userData[resource]["day4"]["value"], this.userData[resource]["day4"]["goal"]);
		chartRowDiv.appendChild(day4chart);

		day5chart = this.ChartElement(resource, this.userData[resource]["day5"]['weekday'], this.userData[resource]["day5"]["value"], this.userData[resource]["day5"]["goal"]);
		chartRowDiv.appendChild(day5chart);

		day6chart = this.ChartElement(resource, this.userData[resource]["day6"]['weekday'], this.userData[resource]["day6"]["value"], this.userData[resource]["day6"]["goal"]);
		chartRowDiv.appendChild(day6chart);

		day7chart = this.ChartElement(resource, this.userData[resource]["day7"]['weekday'], this.userData[resource]["day7"]["value"], this.userData[resource]["day7"]["goal"]);
		chartRowDiv.appendChild(day7chart);

		return chartRowDiv;

	},

	// Make each resource element for the UI
	UIElement: function(resource) {
		var widgetDiv = document.createElement("div");
		widgetDiv.className = "widget";

		// Header = Resource name
		var textDiv = document.createElement("div");
		textDiv.className = "widgetheader";
		textDiv.innerHTML = resource

		widgetDiv.appendChild(textDiv);

		// Line: make widgetheader have a border-bottom in css
		//TODO: css: border-bottom: 1px solid black;
	

		// Row of Charts
		widgetDiv.appendChild(this.ChartRowElement(resource));

		return widgetDiv;
	},

	LastSyncedElement: function(resource) {
		var lastSyncedWrapperDiv = document.createElement("div");
		lastSyncedWrapperDiv.className = "lastsynced";

		var textBottomWrapperDiv = document.createElement("div");
		textBottomWrapperDiv.className = "textbottomwrapper";

		var currentDate = new Date();

		var date = ('0' + currentDate.getDate()).slice(-2) + "/"
			+ ('0' + (currentDate.getMonth()+1)).slice(-2) + "/"
			+ currentDate.getFullYear();

		var lastSyncedDateDiv = document.createElement("div");
		lastSyncedDateDiv.innerHTML = date;
		lastSyncedDateDiv.className = "dimmed light xsmall textbottom";

		var time = ('0' + currentDate.getHours()).slice(-2) + ":"
			+ ('0' + currentDate.getMinutes()).slice(-2) + ":"
			+ ('0' + currentDate.getSeconds()).slice(-2);

		var lastSyncedTimeDiv = document.createElement("div");
		lastSyncedTimeDiv.innerHTML = time;
		lastSyncedTimeDiv.className = "dimmed light xsmall textbottom";

		textBottomWrapperDiv.appendChild(lastSyncedDateDiv);
		textBottomWrapperDiv.appendChild(lastSyncedTimeDiv);

		lastSyncedWrapperDiv.appendChild(textBottomWrapperDiv);

		return lastSyncedWrapperDiv;
	},

	// Override DOM generator
	getDom: function() {
		var wrapper = document.createElement("div");

		if (this.loaded) {
			wrapper.className = "wrapper"

			for (resource in this.config.resources) {
				wrapper.appendChild(this.UIElement(this.config.resources[resource]));
			}

			if (this.config.showLastSynced) {
				wrapper.appendChild(this.LastSyncedElement());
			}
		}
		else {
			wrapper.innerHTML = "Loading...";
			wrapper.className = "dimmed light small";
		}
		return wrapper;
	},
});
