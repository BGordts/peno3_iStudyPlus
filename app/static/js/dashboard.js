/*jslint browser: true*/
/*global angular, $, jQuery*/
/*global alert, console*/
/* 'ui.bootstrap.tooltip', 'ui.bootstrap.accordion', 'ui.bootstrap.buttons', 'ui.bootstrap.carousel', 'ui.bootstrap.timepicker',  */
'use strict';

//alert('boe');
angular.module('app', ['ngRoute', 'ngTouch', 'ui.utils', 'ui.bootstrap.transition', 'ui.bootstrap.collapse', 'ui.bootstrap.dropdownToggle', 'ui.bootstrap.position', 'ui.bootstrap.datepicker', 'ui.bootstrap.rating']).config(function ($interpolateProvider, $locationProvider, $routeProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
    $locationProvider.html5Mode(true);
    $routeProvider.when("/app/:user/:appviewstate", /* /:user/:appviewstate */ {
	        templateUrl: "panels.tpl",
	        //template: "<div>hello world</div>",
	        controller: "viewCtrl"
	});
//	.when("/user/:page", /* /:user/:appviewstate */ {
//	        redirectTo: function(params) {
//	                alert('/user/' + params.page);
//	                return '/user/' + params.page;
//	        }
//	});
})

.controller('viewCtrl', function ($scope, $routeParams) {
	console.log('rhoeteParamiëters');
	console.log($routeParams.appviewstate);
	$scope.$emit('routeChange', $routeParams);
	$scope.appViewState = $routeParams.appviewstate;

	//$scope.courselist = [{"a": "b"}];
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
		
		//In sessionsview, make sure the correct course is selected
		var urlParameter = parseInt(($location.search()).course);	
		
		if(undefined == urlParameter || isNaN(urlParameter)){
			$scope.courseFilter.selected = 0;
		}
		else{
			$scope.courseFilter.selected = urlParameter;
		}
	}

	$scope.courselist = [];
	$scope.courselistcompare = [];
	$scope.selectableCourseList = [];
	$scope.sessionlist = null;
	$scope.name = "";
	$scope.commonStudents = [];
	
	$scope.courseFilter = {selected: -1};
	
	$scope.init = function(){		
		serverConnectionService.getCoStudents(function(data){
			console.log("kaka");
			$scope.commonStudents = data;
		})
		
		serverConnectionService.getCurrentUser(function(data){
			$scope.loggedInProfile = data;
		})
	}
	
	$scope.$watch('viewedProfile', function (newVal, oldVal) {		
		//Voeg nog een exta if toe om te zien of het gegeven object neit leeg is :)
		if(undefined == newVal || newVal == null || Object.keys(newVal).length == 0){
			console.log("hey fa" + newVal + " " + oldVal);
		}
		else{							
			serverConnectionService.getCoursesSimple($scope.viewedProfile.userID, function(data){
				//Fill in the courselist
				$scope.courselist = data;
				
				 $scope.sessionCourses = { courses : data };
				
				//Fill in the options for the courseselector in the sessionspanel
				$scope.selectableCourseList = angular.copy(data);
				
				//Now add the option to see the sessions of all the courses
				$scope.selectableCourseList.unshift({"id":0, "name": "Alle vakken"})
			});
		}
    });
	
	/**
	 * Filter which sessions are displayed
	 */
	$scope.courseFilterFunction = function(session){		
		if($scope.courseFilter.selected == 0){
			return true;
		}
		else{
			return session.sessionData.course_id == $scope.courseFilter.selected;
		}
	}
})

.controller('CreateSessionCtrl', function ($scope, $timeout, serverConnectionService) {
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
	
        $scope.activityType = '';
        $scope.sessionType = '';
        $scope.newSession = {
                sessionType: 'live',
                activityType: '',
                course: ''
        };
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
		  
		  $scope.description = "";
		  
		  $scope.startButtonClicked = function(){
			  //sessionName, courseID, callback
			  serverConnectionService.sessionCreateTracked($scope.description, $scope.newSession.course, function(data){
				  serverConnectionService.sessionStart(function(data){
					  console.log("session created and started");
					  console.log(data);
					  
					  window.location.href = "/session/tracking";
				  })
			  })
		  }
		  
		  $scope.saveButtonClicked = function(){
			  console.log($scope.description);
			  console.log($scope.newSession.course);
			  console.log($scope.dt);
			  console.log($scope.newSession.ST);
			  console.log($scope.newSession.ET);
			  console.log($scope.rate.value / 10);
			  
			  var theDate = moment($scope.dt.getTime())
			  var stHour = parseInt(("" + $scope.newSession.ST).substring(0,2));
			  var stMinute = parseInt(("" + $scope.newSession.ST).substring(2,4));
			  
			  var etHour = parseInt(("" + $scope.newSession.ET).substring(0,2));
			  var etMinute = parseInt(("" + $scope.newSession.ET).substring(2,4));
			  
			  var startCopy = moment(theDate);
			  startCopy.hours(stHour);
			  startCopy.minutes(stMinute);
			  
			  var endCopy = moment(theDate);
			  endCopy.hours(etHour);
			  endCopy.minutes(etMinute);
			  
			  console.log(startCopy.format("dddd, MMMM Do YYYY, h:mm:ss a"));
			  console.log(endCopy.format("dddd, MMMM Do YYYY, h:mm:ss a"));
			  
			  serverConnectionService.sessionCreateUntracked($scope.description, $scope.newSession.course, $scope.rate.value / 10, startCopy.valueOf(), endCopy.valueOf(), function(data){
				  console.log("SENT");
				  console.log(data);
				  
				  //Refresh the page so the user gets visual feedback of the completion
				  location.reload();
			  })
		  }        
})

.controller('coursecontroller', function ($scope, serverConnectionService ) {
	$scope.$watch('viewedProfile', function (newVal, oldVal) {		
		if(undefined == newVal || newVal == null || Object.keys(newVal).length == 0){
			console.log("hey fa" + newVal + " " + oldVal);
		}
		else{								
			//Get the courses
			serverConnectionService.getCourses($scope.viewedProfile.userID, function(data){
				$scope.courselist = data;
			});
		}
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

	//$scope.courseFilter.selected = parseInt(($location.search()).course);
})

.controller('sessionTrackingCtrl', function($scope, serverConnectionService){
	$scope.tracking = { state : 'active'};
	$scope.sessionID = -1;
	$scope.rate = {value: 0};
	
	$scope.pause = function(){
		serverConnectionService.sessionPause(function(data){
			console.log("Paused");
			$scope.tracking.state = 'pause';
		});
	}
	
	$scope.resume = function(){
		serverConnectionService.sessionResume(function(data){
			console.log("Resume");
			$scope.tracking.state = 'active';
		});
	}
	
	$scope.end = function(){
		serverConnectionService.sessionEnd(function(data){
			$scope.sessionID = data;
			$scope.tracking.state = 'end';
		});
	}
	
	$scope.commit = function(){
		serverConnectionService.sessionPostFeedback($scope.rate.value/10, function(data){
			serverConnectionService.sessionCommit(function(data){
				window.location.href = "/";
			});
		});
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
	this.URL_GET_USER = '/user/getUser';
	this.URL_GET_CURRENT_USER = '/user/getCurrentUser';
	this.URL_GET_ALL_SESSIONS = '/session/getAllSessions';
	this.URL_GET_COURSES = '/user/courses';
	this.URL_GET_SENSOR_DATA = '/sensorData/getSensordataForSession';
	this.URL_SESSION_CREATE_TRACKED = '/session/createTracked';
	this.URL_SESSION_CREATE_UNTRACKED = '/session/createUntracked';
	this.URL_SESSION_START = '/session/start';
	this.URL_SESSION_PAUSE = '/session/pause';
	this.URL_SESSION_RESUME = '/session/resume';
	this.URL_SESSION_POST_FEEDBACK = '/session/postFeedback';
	this.URL_SESSION_END = '/session/end';
	this.URL_SESSION_COMMIT = '/session/commit';
	this.URL_MODIFY_TRACKED_SESSION = '/session/modifyTSession';
	this.URL_MODIFY_UNTRACKED_SESSION = '/session/modifyUSession';
	this.URL_SESSION_DELETE = '/session/deleteUSession';
	
	// Basic method: call the server with the specified url, parameters and callback
	this.requestData = function(path, parameters, callback){
		var httpParameters = {method: 'GET', url: path};
		
		var params = {};
		if(Object.keys(parameters) != 0){
			httpParameters['params'] = parameters;
		}
		
		$http(httpParameters)
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
	
	this.sessionCreateUntracked = function(sessionName, courseID, feedback, start_time, end_time, callback){
		this.requestData(this.URL_SESSION_CREATE_UNTRACKED, {'sessionName': sessionName, 'courseID': courseID, 'feedback': feedback, 'start_time':start_time, 'end_time':end_time}, function(data){
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
	
	this.sessionPostFeedback = function(feedback, callback){
		this.requestData(this.URL_SESSION_POST_FEEDBACK, {'feedback': feedback}, function(data){
			callback(data);
		})
	}
	
	this.sessionEnd = function(callback){
		this.requestData(this.URL_SESSION_END, {}, function(data){
			callback(data);
		})
	}
	
	this.sessionCommit = function(callback){
		this.requestData(this.URL_SESSION_COMMIT, {}, function(data){
			callback(data);
		})
	}
	
	this.sessionModifyTracked = function(sessionID, description, courseID,callback){
		this.requestData(this.URL_MODIFY_TRACKED_SESSION, {"sessionID":sessionID, "description":description, "courseID":courseID}, function(data){
			callback(data);
		})
	}
	
	this.sessionModifyUntrackedTracked = function(sessionID, description, courseID, feedback, startDate, endDate, callback){
		this.requestData(this.URL_MODIFY_UNTRACKED_SESSION, {"sessionID":sessionID, "description":description, "courseID":courseID, "feedback":feedback, "startDate":startDate, "endDate":endDate}, function(data){
			callback(data);
		})
	}
	
	this.sessionDeleteUntracked = function(sessionID,callback){
		this.requestData(this.URL_SESSION_DELETE, {"sessionID":sessionID}, function(data){
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
			$scope.Math = window.Math;
			
			$scope.formatTime = function(timeint){
				var hours = ~~timeint;
				var minutes = Math.round((timeint - hours)*100);
				
				return hours + "u " + minutes + "min";
			};
			
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
			$scope.Math = window.Math;
			
			$scope.formatTime = function(timeint){
				var hours = ~~timeint;
				var minutes = Math.round((timeint - hours)*100);
				
				return hours + "u " + minutes + "min";
			};
			
			$scope.chartdata1 = [];
            $scope.chartdata2 = [];
            $scope.chartdata = {
                "profile": $scope.chartdata1,
                "compare": $scope.chartdata2
            };
            $scope.isCollapsed = { value: true };
			$scope.title = $scope.course.name;
			
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
                controller: function ($scope, serverConnectionService) { 
                	$scope.Math = window.Math;
        			
        			$scope.formatTime = function(timeint){
        				var hours = ~~timeint;
        				var minutes = Math.round((timeint - hours)*100);
        				
        				return hours + "u " + minutes + "min";
        			};
                	
                		console.log("searchfilter: ");
                		console.log($scope.courseFilter);
                        
                        $scope.data = {headerdata: {activityType: "class", sessionID: "5"}}; //Boris
                        $scope.course = "analyse";
                        console.log("the il: ");
                        console.log($scope.session.sessionData.sessionIll);
                        $scope.tracked = $scope.session.sessionData.sessionIll != 0;
                        
                        $scope.panelState = "view";
                        
                        if($scope.tracked){
                        	$scope.sessionType = "live";
                        } else{
                        	$scope.sessionType = "past";
                        }
                        
                        
                        
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


                        $scope.savethis = "saveedit" + $scope.session.sessionID;
                        $scope.saveid = "emitsave" + $scope.session.sessionID;

                        console.log($scope.savethis);
                        $scope.save = function() {
		                    console.log("save");
		                    $scope.$broadcast($scope.savethis);
		                    $scope.panelState='view';
		                    
		                    $scope.session.sessionData.feedback_score = $scope.session.sessionData.feedback_score/10;
		                    
		                    var description = $scope.session.sessionData.description;
                        	var sessionID = $scope.session.sessionID;
                        	var courseID = $scope.session.sessionData.course_id;
                        	var feedback = $scope.session.sessionData.feedback_score;
                        	
                        	if($scope.tracked){
                        		serverConnectionService.sessionModifyTracked(sessionID, description, courseID,function(data){
                            		console.log("saved!");
                            		console.log(data);
                            	});
                        	} else{
                        		console.log("is dit een date:");
                        		console.log($scope.session);
                        		console.log($scope.session.sessionData.start_date);
                        		console.log($scope.session.formattedStartTime);
                        		console.log($scope.session.formattedEndTime);
                        		console.log(feedback);
                        		
                        		  var theDate = moment($scope.session.sessionData.start_date);
                        		  
                        		  if(isNaN($scope.session.formattedStartTime)){
                        			  var stHour = parseInt(("" + $scope.session.formattedStartTime).substring(0,2));
    	                  			  var stMinute = parseInt(("" + $scope.session.formattedStartTime).substring(3,5));
                        		  } else{
                        			  var stHour = parseInt(("" + $scope.session.formattedStartTime).substring(0,2));
    	                  			  var stMinute = parseInt(("" + $scope.session.formattedStartTime).substring(2,4));
                        		  }
                        		  
                        		  if(isNaN($scope.session.formattedEndTime)){
                        			  var etHour = parseInt(("" + $scope.session.formattedEndTime).substring(0,2));
    	                  			  var etMinute = parseInt(("" + $scope.session.formattedEndTime).substring(3,5));
                        		  } else{
                        			  var etHour = parseInt(("" + $scope.session.formattedEndTime).substring(0,2));
    	                  			  var etMinute = parseInt(("" + $scope.session.formattedEndTime).substring(2,4));
                        		  }

	                  			  var startCopy = moment(theDate);
	                  			  startCopy.hours(stHour);
	                  			  startCopy.minutes(stMinute);
	                  			  
	                  			  var endCopy = moment(theDate);
	                  			  endCopy.hours(etHour);
	                  			  endCopy.minutes(etMinute);
	                  			  
	                  			  console.log(startCopy.format("dddd, MMMM Do YYYY, h:mm:ss a"));
	                  			  console.log(endCopy.format("dddd, MMMM Do YYYY, h:mm:ss a"));
                        		
                        		serverConnectionService.sessionModifyUntrackedTracked(sessionID, description, courseID, feedback, startCopy.valueOf(), endCopy.valueOf(), function(data){
                            		console.log("saved!");
                            		console.log(data);
                            	});
                        	}        
                        };
                        $scope.$on($scope.saveid, function(event, data) {console.log("remit"); console.log(data); $scope.session = data})
			            $scope.cancel = function() {
			                                $scope.panelState='view';
			            };
			            $scope.delete = function() {
//			            	console.log("please delete");
//			            					serverConnectionService.sessionDeleteUntracked($scope.session.sessionID, function(data){
//			            						console.log("Deleted!");
//			            						location.reload();
//			            					})
			            };
			            
			            $scope.collapseController = function(){
			            	$scope.isCollapsed.value = !$scope.isCollapsed.value
			            	console.log("collapse");
			            	serverConnectionService.getSensorDataForSession($scope.session.sessionID, function(data){
			            		console.log("jeej");
			            		$scope.chartdata = data;
			            	})
			            }
                }
        }
})

.directive('sessionEdit', function() {
        return {
                restrict: 'EA',
                replace: true,
                scope: {
                                sessiontype: "=",
                        editdata: "=",
                        courses: "="
                },
                templateUrl: "sessionEdit.tpl",
                link: function (scope, element, attrs) {
                        scope.editeddata = angular.copy(scope.editdata);
                        scope.editeddata.sessionData.feedback_score = scope.editeddata.sessionData.feedback_score * 10;
                        
                        console.log("lescope");
                        console.log(scope);

                },
                controller: function ($scope, $timeout, serverConnectionService) {
                		
                		$scope.description = "";
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


                        $scope.broadcastid = "saveedit" + $scope.editdata.sessionID;
                        $scope.emitid = "emitsave" + $scope.editdata.sessionID;
                        
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

.directive('staticGraph', function () {
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
                    top: 10,
                    right: 0,
                    bottom: 0,
                    left: 0
                },
                    width = 320,
                    height = 80,
                    gap = 0,
                    ease = 'cubic-in-out';
                var svg, duration = 500;

                var dispatch = d3.dispatch('customHover');

                function exports(_selection) {
                    _selection.each(function (_data) {

                        var chartW = width - margin.left - margin.right,
                            chartH = height - margin.top - margin.bottom;

                        var x1 = d3.scale.linear()
                            .domain([d3.min(_data, function (d, i) {
                                return d.x
                            }), d3.max(_data, function (d, i) {
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
                            });
                        var area = d3.svg.area()
                            .defined(line.defined())
                            .x(line.x())
                            .y(line.y())
                            .y0(y1(0));



                        //var barW = chartW / _data.length;

                        if (!svg) {
                            svg = d3.select(this)
                                .append('svg')
                                .classed('chart', true);

                            var container = svg.append('g').classed('container-group', true);
                            container.append('g').classed('chart-group', true);

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
                        svg.select('.chart-group').append("path")
                            .attr("class", "area")
                            .attr("d", area);
                        svg.select('.chart-group')
                            .selectAll(".dot").data(_data.filter(function (d) {
                                return d.y;
                            }))
                            .enter().append("circle")
                            .attr("class", "dot")
                            .attr("cx", line.x())
                            .attr("cy", line.y())
                            .attr("r", 3.5);

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

.directive('tweet', function() {
        return {
                restrict: 'EA',
                replace: true,
                scope: {
                                text: "=",
                        hashtags: "=",
                        tweeturl: "="
                },
                templateUrl: "tweet.tpl",
                controller: function ($scope, $timeout) {
                        console.log($scope.text);
                                        $scope.fbs_click = function() {
                                                var twtText = $scope.text;
                                                console.log(twtText.length);
                                                var maxLength = 140 - ($scope.tweeturl.length + 1);
                                                if (twtText.length > maxLength) {
                                                        twtText = twtText.substr(0, (maxLength - 3)) + '...';
                                                }
                                                console.log(twtText)
                                                var twtLink = 'http://twitter.com/home?status=' + encodeURIComponent(twtText + ' ' + $scope.tweeturl);
                                                window.open(twtLink);
                                        }
                }
        }
});

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