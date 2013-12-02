/*jslint browser: true*/
/*global angular, $, jQuery*/
/*global alert, console*/

'use strict';

//alert('boe');
angular.module('app', []).config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
}).

controller('appCtrl', function ($scope) {
    //alert('boe');
    console.log('boe');
    $scope.panelState = "view";
    $scope.sessionType = "live";
    $scope.activityType = "study";
    $scope.courselistcompare = [{
        "data1": [
            {
                x: 0.2,
                y: 0.2
  },
            {
                x: 0.3,
                y: 0.2
  },
            {
                x: 0.4,
                y: 0.2
  },
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
  },
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
  },
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
  },
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
  },
    ]
 }];
    $scope.courselist = [{
        "data1": [
            {
                x: 0.2,
                y: 0.5
  },
            {
                x: 0.3,
                y: 0.4
  },
            {
                x: 0.4,
                y: 0.1
  },
    ],
        "data2": [
            {
                x: 0.2,
                y: 0.5
  },
            {
                x: 0.3,
                y: 0.6
  },
            {
                x: 0.4,
                y: 0.8
  },
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
  },
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
  },
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
  },
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
})
/*.

directive('dashboardPanel', function ($scope) {
	return {
		restrict: "EA",
		replace: true,
		template:
	}
})*/

.directive("coursepanel", function () {
    return {
        restrict: 'EA',
        replace: true,
        templateUrl: "dashboard_course-list.tpl",
        link: function (scope, element, attrs) {
            scope.$watch('selectedItem', function (newVal, oldVal) {
                if (typeof nevVal === "undefined" && newVal == null) {
                    console.log("hey fa" + newVal + " " + oldVal);
                    //scope.chartdata = scope.item.data2;
                } else {
                    console.log("jmjklm")
                    scope.chartdata1 = scope.item["data" + newVal.id];
                    scope.chartdata2 = scope.courselistcompare[scope.$index]["data" + newVal.id];
                    console.log(scope.chartdata2)
                    console.log(scope.chartdata1)
                    scope.chartdata = {
                        "profile": scope.chartdata1,
                        "compare": scope.chartdata2
                    }
                }
            });
        },
        controller: function ($scope) {
            $scope.chartdata1 = $scope.item.data1;
            $scope.chartdata2 = $scope.courselistcompare[$scope.$index].data1;
            $scope.chartdata = {
                "profile": $scope.chartdata1,
                "compare": $scope.chartdata2
            };
            //  console.log($scope.chartdata2)
            //		console.log($scope.chartdata1)

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

.directive("sessionpanel", function () {
    return {
        restrict: 'EA',
        replace: true,
        templateUrl: "dashboard_session-list.tpl",
        link: function (scope, element, attrs) {

        },
        controller: function ($scope) {
            $scope.chartdata = $scope.item;
            //console.log($scope.chartdata)
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