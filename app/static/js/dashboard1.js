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


.controller('mainCtrl', function AppCtrl($scope) {
    $scope.options = {
        width: 500,
        height: 300,
        'bar': 'aaa'
    };
    $scope.data = d3.range(40).map(function(i) {
  return {x: i / 39, y: i % 5 ? (Math.sin(i / 3) + 2) / 4 : null};
});
    console.log($scope.data)

})
    .directive('barChart', function () {
        var chart = d3.custom.barChart();
        return {
            restrict: 'E',
            replace: true,
            template: '<div class="chart"></div>',
            scope: {
                height: '=height',
                data: '=data',
            },
            link: function (scope, element, attrs) {
                var chartEl = d3.select(element[0]);

                scope.$watch('data', function (newVal, oldVal) {
                    chartEl.datum(newVal).call(chart);
                });
            }
        }
    })
    .directive('chartForm', function () {
        return {
            restrict: 'E',
            replace: true,
            controller: function AppCtrl($scope) {
                $scope.update = function (d, i) {
                    $scope.data = randomData();
                };

                function randomData() {
                    d3.range(40).map(function (i) {
                        return {
                            x: i / 39,
                            y: i % 5 ? (Math.sin(i / 3) + 2) / 4 : null
                        };
                    });
                }
            },
            template: '<div class="form">' +
                'Height: {{options.height}}<br />' +
                '<input type="range" ng-model="options.height" min="100" max="800"/>' +
                '<br /><button ng-click="update()">Update Data</button>' +
                '<br />Hovered bar data: {{barValue}}</div>'
        }
    });

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
            console.log(_data)

            var margin = {
                top: 20,
                right: 20,
                bottom: 30,
                left: 40
            },
                width = 960 - margin.left - margin.right,
                height = 500 - margin.top - margin.bottom;

            var x = d3.scale.linear()
                .range([0, width]);

            var y = d3.scale.linear()
                .range([height, 0]);

            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom");

            var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left");

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

            var svg = d3.select("body").append("svg")
                .datum(_data)
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            svg.append("path")
                .attr("class", "area")
                .attr("d", area);

            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis);

            svg.append("path")
                .attr("class", "line")
                .attr("d", line);

            svg.selectAll(".dot")
                .data(_data.filter(function (d) {
                    return d.y;
                }))
                .enter().append("circle")
                .attr("class", "dot")
                .attr("cx", line.x())
                .attr("cy", line.y())
                .attr("r", 3.5);
        });
    }
};
