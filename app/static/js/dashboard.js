/*jslint browser: true*/
/*global angular, $, jQuery*/
/*global alert, console*/

'use strict';

//alert('boe');
angular.module('dashboard', []).config(function($interpolateProvider){
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
    }
).

controller('dashboardCtrl', function ($scope) {
	//alert('boe');
	console.log('boe');
	$scope.name = "You";
	$scope.commonStudents = [{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"}]
});


angular.module('myApp', []).config(function($interpolateProvider){
        $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
    }
);