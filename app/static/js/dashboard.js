/*jslint browser: true*/
/*global angular, $, jQuery*/
/*global alert, console*/

'use strict';

//alert('boe');
angular.module('app', []).config(function($interpolateProvider){
        $interpolateProvider.startSymbol('[[').endSymbol(']]');
    }
).

controller('appCtrl', function ($scope) {
	//alert('boe');
	console.log('boe');
	$scope.name = "You";
	$scope.commonStudents = [{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"},{"name":"ik"},{"name":"jij"},{"name":"hij"},{"name":"of zij"},{"name":"jeroen"}]
});