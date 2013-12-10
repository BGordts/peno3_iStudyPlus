/*jslint browser: true*/
/*global angular, $, jQuery*/
/*global alert, console*/
/* 'ui.bootstrap.tooltip', 'ui.bootstrap.accordion', 'ui.bootstrap.buttons', 'ui.bootstrap.carousel',  */
'use strict';

//alert('boe');
angular.module('app', ['ngRoute', 'ngTouch', 'ui.utils', 'ui.bootstrap.transition', 'ui.bootstrap.collapse', 'ui.bootstrap.dropdownToggle', 'ui.bootstrap.position', 'ui.bootstrap.datepicker', 'ui.bootstrap.timepicker', 'ui.bootstrap.rating']).config(function ($interpolateProvider, $locationProvider, $routeProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    $locationProvider.html5Mode(true);
    $routeProvider.when("/app/:user/:appviewstate", /* /:user/:appviewstate */ {
	        templateUrl: "panels.tpl",
	        //template: "<div>hello world</div>",
	        controller: "viewCtrl"
	})
	.when("/user/:page", /* /:user/:appviewstate */ {
	        redirectTo: function(params) {
	                alert('/user/' + params.page);
	                return '/user/' + params.page;
	        }
	});
})

.controller('viewCtrl', function ($scope, $routeParams) {
	console.log('rhoeteParamiëters');
	console.log($routeParams.appviewstate);
	$scope.$emit('routeChange', $routeParams);
	$scope.appViewState = $routeParams.appviewstate;

	$scope.courselist = [{"a": "b"}];
}).

controller('appCtrl', function ($scope, serverConnectionService, $location) {
	// Jeroen
    $scope.rate = 0;
    $scope.hoveringOver = function(value) {
        $scope.overStar = value;
        $scope.percent = 100 * (value / 10);
      };
      $scope.leavereating = function() {
              $scope.percent = $scope.rate * 10;
      };
      // Jeroen
      $scope.trackingState = 'active'
    	  
    $scope.isCollapsedTopnav = { value: true };
    $scope.isCollapsedSidepanel = { value: false };
    $scope.isTransitioningSidepanel = { value: false,
        func: function() {
                $scope.isTransitioningSidepanel.value = true;
                setTimeout(function(){$scope.isTransitioningSidepanel.value = false;}, 350); }
    };

	
	$scope.loggedInProfile = {};
	$scope.viewedProfile = {};

	$scope.$on('routeChange', function(event, data) {appRouteChange(event, data);});
	var appRouteChange = function (event, data) {
		if (data.user != $scope.viewedProfile.user || $scope.viewedProfile.user == undefined) {
			serverConnectionService.getUser(data.user, function(serverData){
				$scope.viewedProfile = serverData;
			});
			//$scope.viewedProfile = loadProfileData(data.user); //Boris
			//$scope.viewedProfile.user = data.user;
		}
		if (data.appviewstate != $scope.appviewstate || $scope.appviewstate == undefined) {
			$scope.appviewstate = data.appviewstate;
		}
	}

	$scope.courselist = [];
	$scope.courselistcompare = [];
	$scope.sessionlist = null;
	$scope.name = "";
	$scope.commonStudents = [];
	
	$scope.courseFilter = {selected: parseInt(($location.search()).course)};
	$scope.protput = ($location.search()).course;
	
	$scope.init = function(){		
		serverConnectionService.getCoStudents(function(data){
			console.log("kaka");
			$scope.commonStudents = data;
		})
		
		serverConnectionService.getCurrentUser(function(data){
			$scope.loggedInProfile = data;
		})
		
		//$scope.courseFilter.selected = parseInt(($location.search()).course);
	}
	
	$scope.$watch('viewedProfile', function (newVal, oldVal) {		
		//Voeg nog een exta if toe om te zien of het gegeven object neit leeg is :)
		if(undefined == newVal || newVal == null || Object.keys(newVal).length == 0){
			console.log("hey fa" + newVal + " " + oldVal);
		}
		else{							
			serverConnectionService.getCoursesSimple($scope.viewedProfile.userID, function(data){
				$scope.courselist = data;
				
				console.log("lolo");
				console.log($scope.courseFilter);
			});
		}
    });
	
	/**
	 * Filter which sessions are displayed
	 */
	$scope.courseFilterFunction = function(session){
		console.log("FUCK FUCK FUCK "  + $scope.courseFilter.selected);
		if(undefined == $scope.courseFilter.selected || isNaN($scope.courseFilter.selected)){
			//When no sessions are selected, show all the sessions
			return true;
		}
		else{			
			return session.sessionData.course_id == $scope.courseFilter.selected;
		}		
	}
})

.controller('coursecontroller', function ($scope, serverConnectionService ) {
	//Get the courses
	serverConnectionService.getCourses(1, function(data){
		$scope.courselist = data;
	});
})

.controller('sessionscontroller', function ($scope, serverConnectionService ) {	
	$scope.$watch('viewedProfile', function (newVal, oldVal) {		
		//Voeg nog een exta if toe om te zien of het gegeven object neit leeg is :)
		if(undefined == newVal || newVal == null || Object.keys(newVal).length == 0){
			console.log("hey fa" + newVal + " " + oldVal);
		}
		else{								
			//Get the sessions
			serverConnectionService.getUserSessions($scope.viewedProfile.userID, function(data){
				$scope.sessionlist = data;
			});
		}
    });
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
	this.URL_GET_USER = '/user/getUser';
	this.URL_GET_CURRENT_USER = '/user/getCurrentUser';
	this.URL_GET_ALL_SESSIONS = '/session/getAllSessions';
	this.URL_GET_COURSES = '/user/courses';
	this.URL_GET_SENSOR_DATA = '/sensorData/getSensordataForSession';
	this.URL_SESSION_CREATE_TRACKED = '/session/createTracked';
	this.URL_SESSION_START = '/session/start';
	this.URL_SESSION_PAUSE = '/session/pause';
	this.URL_SESSION_RESUME = '/session/resume';
	this.URL_SESSION_POST_FEEDBACK = '/session/postFeedback';
	this.URL_SESSION_END = '/session/end';
	this.URL_SESSION_COMMIT = '/session/commit';
	
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
	this.getEfficiencyForSensor = function(userID1, userID2, sensortype, courseID, callback){
		this.requestData(this.URL_EFFICIENCY_FOR_SENSOR, {'userID1':userID1, 'userID2':userID2, 'sensor_type':sensortype, 'courseID':courseID}, function(data){
			// Make a nice dictionary with x and y coordinates
			var linePointArray = {'profile': new Array(), 'compare': new Array()};
			
			console.log("lolololololo-");
			console.log(data);
			
			if(Object.keys(data['1']).length != 0){
				for(var nextDataPoint in data['1']){
					linePointArray.profile.push({x: parseFloat(nextDataPoint), y:parseFloat(data['1'][nextDataPoint])})
				}
			} else {
				linePointArray.profile = [];
			}

			if(Object.keys(data['2']).length != 0){
				for(var nextDataPoint in data['2']){
					linePointArray.compare.push({x: parseFloat(nextDataPoint), y:parseFloat(data['2'][nextDataPoint])})
				}
			} else{
				linePointArray.compare = [];
			}
			
			//The code to show the graph doesn't work with empty data for linePointArray.profile. Therefore, when linePointArray is empty,
			//just give it the same data as the other graph so it is 'invisible'
			if(linePointArray.profile.length == 0){
				linePointArray.profile = linePointArray.compare;
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
	
	// Get all the courses (simple)
	this.getCoursesSimple = function(userid, callback){
		this.requestData(this.URL_GET_COURSES, {"userID":userid}, function(data){
			callback(data);
		})
	}
	
	// Get a user
	this.getUser = function(userid, callback){
		this.requestData(this.URL_GET_USER, {"userID":userid}, function(data){
			callback(data);
		})
	}
	
	// Get the current user
	this.getCurrentUser = function(callback){
		this.requestData(this.URL_GET_CURRENT_USER, {}, function(data){
			callback(data);
		})
	}
	
	// Get the sessions of the user
	this.getUserSessions = function(userID, callback){
		this.requestData(this.URL_GET_ALL_SESSIONS, {'userID': userID}, function(data){
			callback(data);
		})
	}
	
	// Get all the sensorvalues for a session
	this.getSensorDataForSession = function(sessionID, callback){
		this.requestData(this.URL_GET_SENSOR_DATA, {'sessionID': sessionID}, function(data){
			callback(data);
		})
	}
	
	this.sessionCreateTracked = function(sessionName, courseID, callback){
		this.requestData(this.URL_SESSION_CREATE_TRACKED, {'sessionName': sessionName, 'courseID': courseID}, function(data){
			callback(data);
		})
	}
	
	this.sessionStart = function(callback){
		this.requestData(this.URL_SESSION_START, {}, function(data){
			callback(data);
		})
	}
	
	this.sessionPause = function(callback){
		this.requestData(this.URL_SESSION_PAUSE, {}, function(data){
			callback(data);
		})
	}
	
	this.sessionResume = function(callback){
		this.requestData(this.URL_SESSION_RESUME, {}, function(data){
			callback(data);
		})
	}
	
	this.sessionPostFeedback = function(sessionID, feedback, callback){
		this.requestData(this.URL_SESSION_POST_FEEDBACK, {'sessionID': sessionID, 'feedback': feedback}, function(data){
			callback(data);
		})
	}
	
	this.sessionEnd = function(sessionID, callback){
		this.requestData(this.URL_SESSION_END, {'sessionID': sessionID}, function(data){
			callback(data);
		})
	}
	
	this.sessionCommit = function(sessionID, callback){
		this.requestData(this.URL_SESSION_COMMIT, {'sessionID': sessionID}, function(data){
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
				if(undefined == newVal || newVal == null){
					console.log("hey fa" + newVal + " " + oldVal);
				}
				else{
					//Download the new sensordata
					serverConnectionService.getEfficiencyForSensor(scope.viewedProfile.userID, scope.loggedInProfile.userID, newVal.id, -1, function(sensorData){
						scope.chartdata = sensorData;
					});
				}
            });
			
			scope.$watch('viewedProfile', function (newVal, oldVal) {
				//Voeg nog een exta if toe om te zien of het gegeven object neit leeg is :)
				if(undefined == newVal || newVal == null || Object.keys(newVal).length == 0){
					//Nothing interesting happened
				}
				else{					
					//Get the data to fill in
					serverConnectionService.getUserInfo(parseInt(scope.viewedProfile.userID), parseInt(scope.loggedInProfile.userID), function(data){						
						scope.user1 = data.user1;
												
						if(data.user2){
							scope.user2 = data.user2;
						}				
					});	
				}
            });
		},
		controller: function($scope, $http){
			$scope.chartdata1 = [];
            $scope.chartdata2 = [];
            $scope.chartdata = {
                "profile": $scope.chartdata1,
                "compare": $scope.chartdata2
            };
            $scope.isCollapsed = { value: true };
			$scope.title = "Overzicht"
			
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
					serverConnectionService.getEfficiencyForSensor(scope.viewedProfile.userID, scope.loggedInProfile.userID, newVal.id, scope.course.id, function(sensorData){
						scope.chartdata = sensorData;
					});
				}
            });
		},
		controller: function($scope, $http, serverConnectionService){		
			$scope.chartdata1 = [];
            $scope.chartdata2 = [];
            $scope.chartdata = {
                "profile": $scope.chartdata1,
                "compare": $scope.chartdata2
            };
            $scope.isCollapsed = { value: true };
			$scope.title = $scope.course.name
			
			$scope.user1 = $scope.course.statistics;
			
			$scope.user2 = $scope.course.statistics;
			//for (var attrname in $scope.course.statistics) { $scope.user1[attrname] = $scope.course.statistics[attrname]; }
			
			//$scope.chartdata = {x:0, y:0};

			$scope.items = [
			                { id: 'temperature', name: 'Temperatuur' },
			                { id: 'illumination', name: 'Licht' },
			                { id: 'sound', name: 'Geluid' },
			                { id: 'humidity', name: 'Luchtvochtigheid' },
			                { id: 'focus', name: 'Focus' },
			            ];

			$scope.selectedItem = null;
			
			console.log("hihihi");
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
                		console.log("searchfilter: ");
                		console.log($scope.courseFilter);
                        $scope.panelState = "view";
                        $scope.sessionType = "live";
                        $scope.data = {headerdata: {activityType: "class", sessionID: "5"}}; //Boris
                        $scope.course = "analyse";
                        $scope.tracked = true;
                        
                        $scope.session.formattedStartDate = moment($scope.session.sessionData.start_date).format('DD/MM/YYYY')
                        $scope.session.formattedStartTime = moment($scope.session.sessionData.start_date).format('HH:mm')
                        $scope.session.formattedEndTime = moment($scope.session.sessionData.end_date).format('HH:mm')

                        $scope.chartdata = $scope.session.data1;
                        console.log($scope.chartdata)
                        $scope.isCollapsed = { value: true };

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


                        $scope.savethis = "saveedit" + $scope.data.headerdata.sessionID;
                        $scope.saveid = "emitsave" + $scope.data.headerdata.sessionID;

                        console.log($scope.savethis);
                        $scope.save = function() {
		                    console.log("save");
		                    $scope.$broadcast($scope.savethis);
		                    $scope.panelState='view';
                        };
			            $scope.$on($scope.saveid, function(event, data) {console.log("remit"); console.log(data); $scope.data.headerdata = data})
			            $scope.cancel = function() {
			                                $scope.panelState='view';
			            };
			            $scope.delete = function() {
			                                //Boris
			            };
                }
        }
})

.directive('sessionEdit', function() {
        return {
                restrict: 'EA',
                replace: true,
                scope: {
                                sessiontype: "=",
                        editdata: "="
                },
                templateUrl: "sessionEdit.tpl",
                link: function (scope, element, attrs) {
                        scope.editeddata = angular.copy(scope.editdata);

                        scope.lol = "kut" + 'endtime';

                        scope.$watch(scope.lol, function (newVal, oldVal) {
                            console.log(" JAAAAAAA ");
                    });
                },
                controller: function ($scope, $timeout) {
                        console.log("ddfjkqlmsfjklm" + $scope);
                        console.log($scope.editdata.sessionID + 'datepicker');

                        // Datepicker
                        //
                                         $scope.today = function() {
                                                $scope.dt = new Date();
                                         };
                                         $scope.today();

                                         $scope.showWeeks = true;
                                         $scope.toggleWeeks = function () {
                                                 $scope.showWeeks = ! $scope.showWeeks;
                                         };

                                         $scope.open = function() {
                                                $timeout(function() {
                                                  $scope.opened = true;
                                                });
                                          };

                                          $scope.dateOptions = {
                                                'year-format': "'yy'",
                                                'starting-day': 1
                                          };
                                          //
                                          // end

                      // Timepicker
                      //
                      $scope.myStartTime = new Date();
                      $scope.openST = function() {
                                                $timeout(function() {
                                                  $scope.openedST = true;
                                                });
                                          };
                      $scope.myEndTime = new Date();
                      $scope.openET = function() {
                                                $timeout(function() {
                                                  $scope.openedET = true;
                                                });
                                          };
                                          $scope.hstep = 1;
                                          $scope.mstep = 5;
                                          $scope.ismeridian = false;
                                          //
                                          // end


                        $scope.broadcastid = "saveedit" + $scope.editdata.sessionID;
                        $scope.emitid = "emitsave" + $scope.editdata.sessionID;
                        console.log("console");
                   $scope.$on($scope.broadcastid, function(event) {$scope.$emit($scope.emitid, $scope.editeddata)}); //$scope.editdata = angular.copy($scope.editeddata);
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
                        console.log("steven")
                        console.log(_data.profile)

                        var chartW = width - margin.left - margin.right,
                            chartH = height - margin.top - margin.bottom;

                        var x1 = d3.scale.linear()
                            .domain([d3.min(_data.profile, function (d, i) {
                                return d.x
                            }), d3.max(_data.profile, function (d, i) {
                                return d.x;
                            })])
                            .range([0, chartW]);

                        var y1 = d3.scale.linear()
                            .domain([0, d3.max(_data.profile, function (d, i) {
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

                            var path1 = svg.select('.chart-group')
                                .append("path")
                                .data([_data.profile])
                                .attr("class", "line profile")
                                .attr("d", line);

                            var path2 = svg.select('.chart-group')
                                .append("path")
                                .data([_data.compare])
                                .attr("class", "line compare")
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
                            .selectAll('.line.profile')
                            .data([_data.profile])
                            .transition()
                            .attr("d", line);

                        svg.select('.chart-group')
                            .selectAll('.line.compare')
                            .data([_data.compare])
                            .transition()
                            .attr("d", line);

                        //                            var gapSize = x1.rangeBand() / 100 * gap;
                        //                            var barW = x1.rangeBand() - gapSize;
                        //                            var bars = svg.select('.chart-group')
                        //                                .selectAll('.bar')
                        //                                .data(_data);
                        //                            bars.enter().append('rect')
                        //                                .classed('bar', true)
                        //                                .attr({x: chartW,
                        //                                    width: barW,
                        //                                    y: function(d, i) { return y1(d); },
                        //                                    height: function(d, i) { return chartH - y1(d); }
                        //                                })
                        //                                .on('mouseover', dispatch.customHover);
                        //                            bars.transition()
                        //                                .duration(duration)
                        //                                .ease(ease)
                        //                                .attr({
                        //                                    width: barW,
                        //                                    x: function(d, i) { return x1(i) + gapSize/2; },
                        //                                    y: function(d, i) { return y1(d); },
                        //                                    height: function(d, i) { return chartH - y1(d); }
                        //                                });
                        //                            bars.exit().transition().style({opacity: 0}).remove();

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


var DatepickerDemoCtrl = function ($scope, $timeout) {
  $scope.today = function() {
    $scope.dt = new Date();
  };
  $scope.today();

  $scope.showWeeks = true;
  $scope.toggleWeeks = function () {
    $scope.showWeeks = ! $scope.showWeeks;
  };

  $scope.open = function() {
    $timeout(function() {
      $scope.opened = true;
    });
  };

  $scope.dateOptions = {
    'year-format': "'yy'",
    'starting-day': 1
  };

};


var TimepickerDemoCtrl = function ($scope) {
  $scope.mytime = new Date();

  $scope.hstep = 1;
  $scope.mstep = 5;

  $scope.ismeridian = false;
};