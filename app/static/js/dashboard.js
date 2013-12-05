/*jslint browser: true*/
/*global angular, $, jQuery*/
/*global alert, console*/

'use strict';

//alert('boe');
angular.module('app', ['ngRoute', 'ngTouch']).config(function ($interpolateProvider, $locationProvider, $routeProvider) {
	$interpolateProvider.startSymbol('[[').endSymbol(']]');
	$locationProvider.html5Mode(true);
	$routeProvider.when("/app/:user/:appviewstate", /* /:user/:appviewstate */ {
		templateUrl: "panels.tpl",
		//template: "<div>hello world</div>",
		controller: "viewCtrl"
	});
}).

controller('viewCtrl', function ($scope, $routeParams) {
	console.log('rhoeteParamiëters');
	console.log($routeParams.appviewstate);
	$scope.$emit('routeChange', $routeParams);
	$scope.appViewState = $routeParams.appviewstate;

	$scope.courselist = [{
		"data1": [
            {
			x: 0.2,
			y: 0.6
		},
            {
			x: 0.2,
			y: 0.6
		},
            {
			x: 0.2,
			y: 0.6
		}
    ],
		"data2": [
            {
			x: 0.2,
			y: 0.3
		},
            {
			x: 0.3,
			y: 0.10
		},
            {
			x: 0.4,
			y: 0.12
		}
    ]
	}, {
		"data1": [
            {
			x: 0.2,
			y: 0.2
		},
            {
			x: 0.3,
			y: 0.4
		},
            {
			x: 0.4,
			y: 0.8
		}
    ],
		"data2": [
            {
			x: 0.2,
			y: 0.5
		},
            {
			x: 0.3,
			y: 0.9
		},
            {
			x: 4,
			y: 12
		}
    ]
	}, {
		"data1": [
            {
			x: 0.2,
			y: 0.2
		},
            {
			x: 0.3,
			y: 0.6
		},
            {
			x: 0.4,
			y: 0.6
		}
    ],
		"data2": [
            {
			x: 0.2,
			y: 0.5
		},
            {
			x: 0.3,
			y: 0.10
		},
            {
			x: 0.4,
			y: 0.12
		}
    ]
	}];
}).

controller('appCtrl', function ($scope, serverConnectionService) {
	console.log('rhoeteParams');
	$scope.viewedProfile = {user: ""};

	$scope.$on('routeChange', function(event, data) {appRouteChange(event, data);});
	var appRouteChange = function (event, data) {
		if (data.user != $scope.viewedProfile.user || $scope.viewedProfile.user == undefined) {
			//$scope.viewedProfile = loadProfileData(data.user); //Boris
			$scope.viewedProfile.user = data.user;
		}
		if (data.appviewstate != $scope.appviewstate || $scope.appviewstate == undefined) {
			$scope.appviewstate = data.appviewstate;
		}
	}


	//	$scope.panelState = "view";
	//	$scope.sessionType = "live";
	//	$scope.activityType ="study";
	$scope.courselist = [{
		"data1": [
            {
			x: 0.2,
			y: 0.6
		},
            {
			x: 0.2,
			y: 0.6
		},
            {
			x: 0.2,
			y: 0.6
		}
    ],
		"data2": [
            {
			x: 0.2,
			y: 0.3
		},
            {
			x: 0.3,
			y: 0.10
		},
            {
			x: 0.4,
			y: 0.12
		}
    ]
	}, {
		"data1": [
            {
			x: 0.2,
			y: 0.2
		},
            {
			x: 0.3,
			y: 0.4
		},
            {
			x: 0.4,
			y: 0.8
		}
    ],
		"data2": [
            {
			x: 0.2,
			y: 0.5
		},
            {
			x: 0.3,
			y: 0.9
		},
            {
			x: 4,
			y: 12
		}
    ]
	}, {
		"data1": [
            {
			x: 0.2,
			y: 0.2
		},
            {
			x: 0.3,
			y: 0.6
		},
            {
			x: 0.4,
			y: 0.6
		},
    ],
		"data2": [
            {
			x: 0.2,
			y: 0.5
		},
            {
			x: 0.3,
			y: 0.10
		},
            {
			x: 0.4,
			y: 0.12
		}
    ]
	}];
	$scope.sessionlist = [{
		"data": [1, 2, 3, 4]
	}, {
		"data": [2, 2, 2, 2]
	}, {
		"data": [5, 200, 3, 4]
	}];
	/*alert('zever');*/
	$scope.name = "You";
	$scope.commonStudents = [{
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}, {
		"name": "ik"
	}, {
		"name": "jij"
	}, {
		"name": "hij"
	}, {
		"name": "of zij"
	}, {
		"name": "jeroen"
	}]
	
	$scope.init = function(){		
		serverConnectionService.getCoStudents(function(data){
			console.log("kaka");
			$scope.commonStudents = data;
		})
	}
})

/**
 * A service that provides the connection with the server. Every call with the server
 * should pas here.
 */
.service('serverConnectionService', function($http) {
	this.URL_EFFICIENCY_FOR_SENSOR = '/statistics/getEfficiencyForSensor';
	this.URL_GENERAL_USER_STATISTICS = '/statistics/getGeneralUserStatistics';
	this.URL_GE_CO_STUDENTS = '/user/getCoStudents';
	this.URL_GET_DETAILED_COURSES = '/user/getDetailedCourses';
	
	// Basic method: call the server with the specified url, parameters and callback
	this.requestData = function(path, parameters, callback){
		$http({method: 'GET', url: path, params: parameters})
	  	  .success(function(data, status, headers, config) {
	  		  callback(data);
	  	  })
	  	  .error(function(data, status, headers, config) {
	      	    console.log("Error on server request!");
	  	  });
	}
	
	// Get the efficiency for the specified sensor value
	this.getEfficiencyForSensor = function(sensortype, callback){
		this.requestData(this.URL_EFFICIENCY_FOR_SENSOR, {'userID':1, 'sensor_type':sensortype}, function(data){
			// Make a nice dictionary with x and y coordinates
			var linePointArray = new Array();
			for(var nextDataPoint in data){
				linePointArray.push({x: parseFloat(nextDataPoint), y:parseFloat(data[nextDataPoint])})
			}
			
			callback(linePointArray);
			})
	}
	
	// Get the general information of the user
	this.getUserInfo = function(userid1, userid2, callback){
		this.requestData(this.URL_GENERAL_USER_STATISTICS, {'userID1':userid1, 'userID2':userid2}, function(data){
			callback(data);
		})
	}
	
	// Get the costudents
	this.getCoStudents = function(callback){
		this.requestData(this.URL_GE_CO_STUDENTS, {}, function(data){
			callback(data);
		})
	}
	
	// Get all the courses
	this.getCourses = function(userid, callback){
		this.requestData(this.URL_GET_DETAILED_COURSES, {"userID":userid}, function(data){
			callback(data);
		})
	}
})

.directive("dashboardpanel", function(serverConnectionService) {
	return {
		restrict: 'EA',
		replace: true,
		templateUrl: "dashboard_overview.tpl",
		link: function(scope, element, attrs) {
			//Watches the selector to change the plotted efficiency/sensor
			scope.$watch('selectedItem', function (newVal, oldVal) {
				if(typeof nevVal === "undefined" && newVal == null){
					console.log("hey fa" + newVal + " " + oldVal);
				}
				else{
					//Download the new sensordata
					serverConnectionService.getEfficiencyForSensor(newVal.id, function(sensorData){
						scope.chartdata = sensorData;
					});
				}
            });
			
			//Get the data to fill in
			serverConnectionService.getUserInfo(1, 2, function(data){
				console.log(data);
				
				scope.user1 = {};
				scope.user2 = {};
				
				for (var attrname in data.user1) { scope.user1[attrname] = data.user1[attrname]; }
				
				if(data.user2){
					for (var attrname in data.user2) { scope.user2[attrname] = data.user2[attrname]; }
				}				
			});	
		},
		controller: function($scope, $http){
			$scope.title = "Overzicht"
			
			$scope.chartdata = {x:0, y:0};

			$scope.items = [
			                { id: 'temperature', name: 'Temperatuur' },
			                { id: 'illumination', name: 'Licht' },
			                { id: 'sound', name: 'Geluid' },
			                { id: 'humidity', name: 'Luchtvochtigheid' },
			                { id: 'focus', name: 'Focus' },
			            ];

			$scope.selectedItem = null;
		}
	}
})

.directive("coursepanel", function(serverConnectionService) {
	return {
		restrict: 'EA',
		replace: true,
		templateUrl: "dashboard_course-list.tpl",
		link: function(scope, element, attrs) {
			console.log(element);
			console.log(attrs);
			
			scope.$watch('selectedItem', function (newVal, oldVal) {
				if(typeof nevVal === "undefined" && newVal == null){
					console.log("hey fa" + newVal + " " + oldVal);
				}
				else{
					//Download the new sensordata
					serverConnectionService.getEfficiencyForSensor(newVal.id, function(sensorData){
						scope.chartdata = sensorData;
					});
				}
            });
			
			scope.$watch('courselist', function (newVal, oldVal) {
				if(typeof nevVal === "undefined" && newVal == null){
					console.log("hey fa" + newVal + " " + oldVal);
				}
				else{
					//Download the new sensordata
					serverConnectionService.getEfficiencyForSensor(newVal.id, function(sensorData){
						scope.chartdata = sensorData;
					});
				}
            });
		},
		controller: function($scope, $http, serverConnectionService){
			$scope.title = "Overzicht"
			
			$scope.chartdata = {x:0, y:0};

			$scope.items = [
			                { id: 'temperature', name: 'Temperatuur' },
			                { id: 'illumination', name: 'Licht' },
			                { id: 'sound', name: 'Geluid' },
			                { id: 'humidity', name: 'Luchtvochtigheid' },
			                { id: 'focus', name: 'Focus' },
			            ];

			$scope.selectedItem = null;
			
			//Get the courses
			serverConnectionService.getCourses(1, function(data){
				console.log("kjkmldfsjql fjkdf qjsd fjqk fjqk fjK FJQSKFJQS FDLMQJKQSJKLM");
				console.log(data);
				$scope.courselist = data;
			});
		}
	}
})

.directive("sessionpanel", function () {
	return {
		restrict: 'EA',
		replace: true,
		templateUrl: "dashboard_session-list.tpl",
		link: function (scope, element, attrs) {
			scope.$watch('selectedItem', function (newVal, oldVal) {
				if (typeof nevVal === "undefined" && newVal == null) {
					console.log("hey fa" + newVal + " " + oldVal);
					//scope.chartdata = scope.session.data2;
				} else {
					console.log("jmjklm")
					scope.chartdata = scope.session["data" + newVal.id];
				}
			});
		},
		controller: function ($scope) {
			$scope.panelState = "view";
			$scope.sessionType = "live";
			$scope.data = {headerdata: {activityType: "study"}};
			$scope.tracked = false;

			$scope.chartdata = $scope.session.data1;
			console.log($scope.chartdata)

			$scope.items = [
			                {
				id: 1,
				name: 'Foo'
			},
			                {
				id: 2,
				name: 'Bar'
			}
			            ];

			$scope.selectedItem = null;
		}
	}
})

.directive('sessionEdit', function() {
	return {
		restrict: 'EA',
		replace: true,
		scope: {
			editdata: "="
		},
		templateUrl: "sessionEdit.tpl",
		link: function (scope, element, attrs) {

		},
		controller: function ($scope) {

		}
	}
})

//.controller('mainCtrl', function AppCtrl ($scope) {
//            $scope.options = {width: 500, height: 300, 'bar': 'aaa'};
//            $scope.data = [1, 2, 3, 4];
//            $scope.hovered = function(d){
//                $scope.barValue = d;
//                $scope.$apply();
//            };
//            $scope.barValue = 'None';
//        })
.directive('dynamicGraph', function () {
	var integer = 0;
	return {
		restrict: 'E',
		replace: true,
		template: '<div class="chart"></div>',
		scope: {
			chartdata: '=',
		},
		link: function (scope, element, attrs) {
			d3.custom = {};
			d3.custom.barChart = function module() {
				var margin = {
					top: 20,
					right: 20,
					bottom: 40,
					left: 40
				},
				width = 500,
					height = 500,
					gap = 0,
					ease = 'cubic-in-out';
				var svg, duration = 500;

				var dispatch = d3.dispatch('customHover');

				function exports(_selection) {
					_selection.each(function (_data) {

						var chartW = width - margin.left - margin.right,
							chartH = height - margin.top - margin.bottom;

						var x1 = d3.scale.linear()
							.domain([0, d3.max(_data, function (d, i) {
							return d.x;
						})])
							.range([0, chartW]);

						var y1 = d3.scale.linear()
							.domain([0, d3.max(_data, function (d, i) {
							return d.y;
						})])
							.range([chartH, 0]);

						var xAxis = d3.svg.axis()
							.scale(x1)
							.orient('bottom');

						var yAxis = d3.svg.axis()
							.scale(y1)
							.orient('left');

						var line = d3.svg.line()
							.defined(function (d) {
							return d.y != null;
						})
							.x(function (d) {
							return x1(d.x);
						})
							.y(function (d) {
							return y1(d.y);
						})
							.interpolate("bundle");

						//var barW = chartW / _data.length;

						if (!svg) {
							svg = d3.select(this)
								.append('svg')
								.classed('chart', true);

							var container = svg.append('g').classed('container-group', true);
							container.append('g').classed('chart-group', true);
							container.append('g').classed('x-axis-group axis', true);
							container.append('g').classed('y-axis-group axis', true);

							var path = svg.select('.chart-group')
								.append("path")
								.data([_data])
								.attr("class", "line")
								.attr("d", line);
						}

						svg.transition().duration(duration).attr({
							width: width,
							height: height
						})
						svg.select('.container-group')
							.attr({
							transform: 'translate(' + margin.left + ',' + margin.top + ')'
						});

						svg.select('.x-axis-group.axis')
							.transition()
							.duration(duration)
							.ease(ease)
							.attr({
							transform: 'translate(0,' + (chartH) + ')'
						})
							.call(xAxis);

						svg.select('.y-axis-group.axis')
							.transition()
							.duration(duration)
							.ease(ease)
							.call(yAxis);

						svg.select('.chart-group')
							.selectAll('.line')
							.data([_data])
							.transition()
							.attr("d", line);

						//        	            var gapSize = x1.rangeBand() / 100 * gap;
						//        	            var barW = x1.rangeBand() - gapSize;
						//        	            var bars = svg.select('.chart-group')
						//        	                .selectAll('.bar')
						//        	                .data(_data);
						//        	            bars.enter().append('rect')
						//        	                .classed('bar', true)
						//        	                .attr({x: chartW,
						//        	                    width: barW,
						//        	                    y: function(d, i) { return y1(d); },
						//        	                    height: function(d, i) { return chartH - y1(d); }
						//        	                })
						//        	                .on('mouseover', dispatch.customHover);
						//        	            bars.transition()
						//        	                .duration(duration)
						//        	                .ease(ease)
						//        	                .attr({
						//        	                    width: barW,
						//        	                    x: function(d, i) { return x1(i) + gapSize/2; },
						//        	                    y: function(d, i) { return y1(d); },
						//        	                    height: function(d, i) { return chartH - y1(d); }
						//        	                });
						//        	            bars.exit().transition().style({opacity: 0}).remove();

						duration = 500;

					});
				}
				exports.width = function (_x) {
					if (!arguments.length) return width;
					width = parseInt(_x);
					return this;
				};
				exports.height = function (_x) {
					if (!arguments.length) return height;
					height = parseInt(_x);
					duration = 0;
					return this;
				};
				exports.gap = function (_x) {
					if (!arguments.length) return gap;
					gap = _x;
					return this;
				};
				exports.ease = function (_x) {
					if (!arguments.length) return ease;
					ease = _x;
					return this;
				};
				d3.rebind(exports, dispatch, 'on');
				return exports;
			};

			var chart = d3.custom.barChart();
			var chartEl = d3.select(element[0]);

			scope.$watch('chartdata', function (newVal, oldVal) {
				chartEl.datum(newVal).call(chart);
				integer = integer + 1;
				console.log(integer)
			});
		}
	}
})

//d3.custom = {};