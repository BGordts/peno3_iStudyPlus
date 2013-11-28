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
    $scope.courselist = [{'data': [1,2,3,4]}, [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []];
    $scope.sessionlist = [{data: [1,2,3,4]}, [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []];
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
        link: function () {

            },
        controller: function ($scope) {
            $scope.chartdata = $scope.item.data;
            console.log($scope.chartdata)
        },
    }
})

.directive("sessionpanel", function () {
    return {
        restrict: 'EA',
        replace: true,
        templateUrl: "dashboard_session-list.tpl",
        link: function () {

        },
        controller: function ($scope) {
            $scope.chartdata = $scope.item.data;
            console.log($scope.chartdata)
        }
    }
})

/*.controller('mainCtrl', function AppCtrl($scope) {
    $scope.options = {
        width: 500,
        height: 300,
        'bar': 'aaa'
    };
    $scope.data = [1, 2, 3, 4];
    console.log(data)
    $scope.hovered = function (d) {
        $scope.barValue = d;
        $scope.$apply();
    };
    $scope.barValue = 'None'; 
}) */
    .directive('dynamicGraph', function () {
        var chart = d3.custom.barChart();
        return {
            restrict: 'E',
            replace: true,
            template: '<div class="chart"></div>',
            scope: {
                height: '=height',
                data: '=',
                hovered: '&hovered'
            },
            link: function (scope, element, attrs) {
              /*  console.log(attrs.data) */
                var chartEl = d3.select(element[0]);
                chart.on('customHover', function (d, i) {
                    scope.hovered({
                        args: d
                    });
                });
chartEl.datum(    [
        {x:0.2 ,y:0.5},
        {x:0.3 ,y:0.10},
        {x:0.4 ,y:0.12},
    ]).call(chart)
                scope.$watch(attrs.data, function (newVal, oldVal) {
                    chartEl.datum(newVal).call(chart);
                });

                scope.$watch('height', function (d, i) {
                    chartEl.call(chart.height(scope.height));
                })
            }
        }
    })
/*    .directive('chartForm', function () {
        return {
            restrict: 'E',
            replace: true,
            controller: function AppCtrl($scope) {
                $scope.update = function (d, i) {
                    $scope.data = randomData();
                };

                function randomData() {
                    return d3.range(~~(Math.random() * 50) + 1).map(function (d, i) {
                        return~~ (Math.random() * 1000);
                    });
                }
            },
            template: '<div class="form">' +
                'Height: {{options.height}}<br />' +
                '<input type="range" ng-model="options.height" min="100" max="800"/>' +
                '<br /><button ng-click="update()">Update Data</button>' +
                '<br />Hovered bar data: {{barValue}}</div>'
        }
    });*/
              

d3.custom = {};

d3.custom.barChart = function module() {
    var margin = {
        top: 20,
        right: 20,
        bottom: 30,
        left: 40
    },
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom,
        gap = 0,
        ease = 'cubic-in-out';
    var svg;

    var dispatch = d3.dispatch('customHover');

    function exports(_selection) {
        _selection.each(function (_data) {

            var chartW = width - margin.left - margin.right,
                chartH = height - margin.top - margin.bottom;



            var x = d3.scale.linear()
                .range([0, width]);
            var y = d3.scale.linear()
                .range([height, 0]);

            var xAxis = d3.svg.axis()
                .scale(x)
                .orient('bottom');

            var yAxis = d3.svg.axis()
                .scale(y)
                .orient('left');

            var barW = chartW / _data.length;
            var line = d3.svg.line()
                .defined(function (d) {
                    return d.y != null;
                })
                .x(function (d) {
                    return x(d.x);
                })
                .y(function (d) {
                    return y(d.y);
                });

            var area = d3.svg.area()
                .defined(line.defined())
                .x(line.x())
                .y1(line.y())
                .y0(y(0));

            if (!svg) {
                svg = d3.select(this)
                    .append('svg')
                    .classed('chart', true)
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
                var container = svg.append('g').classed('container-group', true);
                container.append('g').classed('chart-group', true);
            }



            svg.append("path")
                .attr("class", "area")
                .attr("d", area);

            svg.append("g")
                .attr("class", "xAxis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            svg.append("g")
                .attr("class", "yAxis")
                .call(yAxis);

            svg.append("path")
                .attr("class", "line")
                .attr("d", line);

            var bars = svg.select('.chart-group')
                .selectAll(".dot")
                .data(_data);
            bars.enter().append("circle")
                .attr("class", "dot")
                .attr("cx", line.x())
                .attr("cy", line.y())
                .attr("r", 3.5)
                .on('mouseover', dispatch.customHover);


        });
    }
    exports.width = function (_x) {
        if (!arguments.length) return width;
        width = parseInt(_x);
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

        