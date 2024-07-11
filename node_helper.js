/* Magic Mirror
 * Node Helper: MMM-Fitbit2-ext
 *
 * MIT Licensed.
 */

var NodeHelper = require("node_helper");
const PythonShell = require("python-shell");

module.exports = NodeHelper.create({

	// Subclass socketNotificationReceived received.
	socketNotificationReceived: function(notification, payload) {
		if (notification === "GET DATA") {
			console.log("MMM-Fitbit2-ext: " + payload.trigger + " request to get data received");
			this.getData(payload.config);
		}
	},

	getData: function (config) {
		const self = this;
		let fileName;
		if (config.test) {
			fileName = "test_data.py";
		} else {
			fileName = "get_data.py";
		}

		if (config.debug) {
			console.log("MMM-Fitbit2-ext: Data to receive: " + JSON.stringify(config));
		}
		console.log("MMM-Fitbit2-ext: START " + fileName);

		var pyArgs = []

		if (config.debug) {
			pyArgs.push("--debug")
		}
		if (config.test) {
			pyArgs.push("--test")
		}

		pyArgs.push(config.credentials.clientId)
		pyArgs.push(config.credentials.clientSecret)

		pyArgs.push("--resources")
		pyArgs = pyArgs.concat(config.resources)

		if (config.debug) {
			console.log("MMM-Fitbit2-ext: " + JSON.stringify(pyArgs))
		}

		const fitbitPyShell = new PythonShell(
			fileName, {
				mode: "json",
				scriptPath: "modules/MMM-Fitbit2-ext/python",
				pythonPath: config.pythonPath,
				pythonOptions: ["-u"], // get print results in real-time
				args: pyArgs
			}
		);

		fitbitPyShell.on("message", function (message) {
			if (config.debug) {
				console.log("MMM-Fitbit2-ext: Message received: " + JSON.stringify(message))
			}
			if (message.type == "data") {
				console.log("API-Data received, sending Nofification...")
				message.clientId = config.credentials.clientId
				self.sendSocketNotification("API_DATA_RECEIVED", message);
				console.log("API-Data Nofification sent.")
			}
		});

		fitbitPyShell.end(function (err) {
			if (err) {
				throw err;
			}
			self.sendSocketNotification("UPDATE_VIEW", "Finished getting data from Fitbit API");
			console.log("MMM-Fitbit2-ext: END " + fileName);
		});
	},
});
