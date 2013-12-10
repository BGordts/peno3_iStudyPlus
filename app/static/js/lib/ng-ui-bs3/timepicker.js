angular.module('ui.bootstrap.timepicker', ['ui.bootstrap.position'])

.constant('timepickerConfig', {
  hourStep: 1,
  minuteStep: 1,
  showMeridian: true,
  meridians: ['AM', 'PM'],
  readonlyInput: false,
  mousewheel: true,

  dayFormat: 'dd',
  monthFormat: 'MMMM',
  yearFormat: 'yyyy',
  dayHeaderFormat: 'EEE',
  dayTitleFormat: 'MMMM yyyy',
  monthTitleFormat: 'yyyy',
  showWeeks: true,
  startingDay: 0,
  yearRange: 20,
  minDate: null,
  maxDate: null
})

.controller('TimepickerController', ['$scope', '$attrs', 'dateFilter', 'timepickerConfig', function($scope, $attrs, dateFilter, dtConfig) {
//  var format = {
//    day:        getValue($attrs.dayFormat,        dtConfig.dayFormat),
//    month:      getValue($attrs.monthFormat,      dtConfig.monthFormat),
//    year:       getValue($attrs.yearFormat,       dtConfig.yearFormat),
//    dayHeader:  getValue($attrs.dayHeaderFormat,  dtConfig.dayHeaderFormat),
//    dayTitle:   getValue($attrs.dayTitleFormat,   dtConfig.dayTitleFormat),
//    monthTitle: getValue($attrs.monthTitleFormat, dtConfig.monthTitleFormat)
//  },
//  startingDay = getValue($attrs.startingDay,      dtConfig.startingDay),
//  yearRange =   getValue($attrs.yearRange,        dtConfig.yearRange);
//
//  this.minDate = dtConfig.minDate ? new Date(dtConfig.minDate) : null;
//  this.maxDate = dtConfig.maxDate ? new Date(dtConfig.maxDate) : null;
//
//  function getValue(value, defaultValue) {
//    return angular.isDefined(value) ? $scope.$parent.$eval(value) : defaultValue;
//  }
//
//  function getDaysInMonth( year, month ) {
//    return new Date(year, month, 0).getDate();
//  }
//
//  function getDates(startDate, n) {
//    var dates = new Array(n);
//    var current = startDate, i = 0;
//    while (i < n) {
//      dates[i++] = new Date(current);
//      current.setDate( current.getDate() + 1 );
//    }
//    return dates;
//  }
//
//  function makeDate(date, format, isSelected, isSecondary) {
//    return { date: date, label: dateFilter(date, format), selected: !!isSelected, secondary: !!isSecondary };
//  }
//
//  this.modes = [
//    {
//      name: 'day',
//      getVisibleDates: function(date, selected) {
//        var year = date.getFullYear(), month = date.getMonth(), firstDayOfMonth = new Date(year, month, 1);
//        var difference = startingDay - firstDayOfMonth.getDay(),
//        numDisplayedFromPreviousMonth = (difference > 0) ? 7 - difference : - difference,
//        firstDate = new Date(firstDayOfMonth), numDates = 0;
//
//        if ( numDisplayedFromPreviousMonth > 0 ) {
//          firstDate.setDate( - numDisplayedFromPreviousMonth + 1 );
//          numDates += numDisplayedFromPreviousMonth; // Previous
//        }
//        numDates += getDaysInMonth(year, month + 1); // Current
//        numDates += (7 - numDates % 7) % 7; // Next
//
//        var days = getDates(firstDate, numDates), labels = new Array(7);
//        for (var i = 0; i < numDates; i ++) {
//          var dt = new Date(days[i]);
//          days[i] = makeDate(dt, format.day, (selected && selected.getDate() === dt.getDate() && selected.getMonth() === dt.getMonth() && selected.getFullYear() === dt.getFullYear()), dt.getMonth() !== month);
//        }
//        for (var j = 0; j < 7; j++) {
//          labels[j] = dateFilter(days[j].date, format.dayHeader);
//        }
//        return { objects: days, title: dateFilter(date, format.dayTitle), labels: labels };
//      },
//      compare: function(date1, date2) {
//        return (new Date( date1.getFullYear(), date1.getMonth(), date1.getDate() ) - new Date( date2.getFullYear(), date2.getMonth(), date2.getDate() ) );
//      },
//      split: 7,
//      step: { months: 1 }
//    },
//    {
//      name: 'month',
//      getVisibleDates: function(date, selected) {
//        var months = new Array(12), year = date.getFullYear();
//        for ( var i = 0; i < 12; i++ ) {
//          var dt = new Date(year, i, 1);
//          months[i] = makeDate(dt, format.month, (selected && selected.getMonth() === i && selected.getFullYear() === year));
//        }
//        return { objects: months, title: dateFilter(date, format.monthTitle) };
//      },
//      compare: function(date1, date2) {
//        return new Date( date1.getFullYear(), date1.getMonth() ) - new Date( date2.getFullYear(), date2.getMonth() );
//      },
//      split: 3,
//      step: { years: 1 }
//    },
//    {
//      name: 'year',
//      getVisibleDates: function(date, selected) {
//        var years = new Array(yearRange), year = date.getFullYear(), startYear = parseInt((year - 1) / yearRange, 10) * yearRange + 1;
//        for ( var i = 0; i < yearRange; i++ ) {
//          var dt = new Date(startYear + i, 0, 1);
//          years[i] = makeDate(dt, format.year, (selected && selected.getFullYear() === dt.getFullYear()));
//        }
//        return { objects: years, title: [years[0].label, years[yearRange - 1].label].join(' - ') };
//      },
//      compare: function(date1, date2) {
//        return date1.getFullYear() - date2.getFullYear();
//      },
//      split: 5,
//      step: { years: yearRange }
//    }
//  ];
//
//  this.isDisabled = function(date, mode) {
//    var currentMode = this.modes[mode || 0];
//    return ((this.minDate && currentMode.compare(date, this.minDate) < 0) || (this.maxDate && currentMode.compare(date, this.maxDate) > 0) || ($scope.dateDisabled && $scope.dateDisabled({date: date, mode: currentMode.name})));
//  };
}])

.directive('timepicker', ['$parse', '$log', 'timepickerConfig', 'dateFilter', function ($parse, $log, timepickerConfig, dateFilter) {
  return {
    restrict: 'EA',
    replace: true,
    templateUrl: 'timepicker.tpl',
    scope: {
      dateDisabled: '&'
    },
    require: ['?^ngModel'], //'timepicker',
    //controller: 'TimepickerController',
    link: function(scope, element, attrs, ctrls) { // ngModel
      // from date
      //
      var timepickerCtrl = ctrls[0], ngModel = ctrls[1];
      // end

      if ( !ngModel ) {
        return; // do nothing if no ng-model
      }

      var selected = new Date(), meridians = timepickerConfig.meridians;

      var hourStep = timepickerConfig.hourStep;
      if (attrs.hourStep) {
        scope.$parent.$watch($parse(attrs.hourStep), function(value) {
          hourStep = parseInt(value, 10);
        });
      }

      var minuteStep = timepickerConfig.minuteStep;
      if (attrs.minuteStep) {
        scope.$parent.$watch($parse(attrs.minuteStep), function(value) {
          minuteStep = parseInt(value, 10);
        });
      }

      // 12H / 24H mode
      scope.showMeridian = timepickerConfig.showMeridian;
      if (attrs.showMeridian) {
        scope.$parent.$watch($parse(attrs.showMeridian), function(value) {
          scope.showMeridian = !!value;

          if ( ngModel.$error.time ) {
            // Evaluate from template
            var hours = getHoursFromTemplate(), minutes = getMinutesFromTemplate();
            if (angular.isDefined( hours ) && angular.isDefined( minutes )) {
              selected.setHours( hours );
              refresh();
            }
          } else {
            updateTemplate();
          }
        });
      }

      // Get scope.hours in 24H mode if valid
      function getHoursFromTemplate ( ) {
        var hours = parseInt( scope.hours, 10 );
        var valid = ( scope.showMeridian ) ? (hours > 0 && hours < 13) : (hours >= 0 && hours < 24);
        if ( !valid ) {
          return undefined;
        }

        if ( scope.showMeridian ) {
          if ( hours === 12 ) {
            hours = 0;
          }
          if ( scope.meridian === meridians[1] ) {
            hours = hours + 12;
          }
        }
        return hours;
      }

      function getMinutesFromTemplate() {
        var minutes = parseInt(scope.minutes, 10);
        return ( minutes >= 0 && minutes < 60 ) ? minutes : undefined;
      }

      function pad( value ) {
        return ( angular.isDefined(value) && value.toString().length < 2 ) ? '0' + value : value;
      }

      // Input elements
      var inputs = element.find('input'), hoursInputEl = inputs.eq(0), minutesInputEl = inputs.eq(1);

      // Respond on mousewheel spin
      var mousewheel = (angular.isDefined(attrs.mousewheel)) ? scope.$eval(attrs.mousewheel) : timepickerConfig.mousewheel;
      if ( mousewheel ) {

        var isScrollingUp = function(e) {
          if (e.originalEvent) {
            e = e.originalEvent;
          }
          //pick correct delta variable depending on event
          var delta = (e.wheelDelta) ? e.wheelDelta : -e.deltaY;
          return (e.detail || delta > 0);
        };

        hoursInputEl.bind('mousewheel wheel', function(e) {
          scope.$apply( (isScrollingUp(e)) ? scope.incrementHours() : scope.decrementHours() );
          e.preventDefault();
        });

        minutesInputEl.bind('mousewheel wheel', function(e) {
          scope.$apply( (isScrollingUp(e)) ? scope.incrementMinutes() : scope.decrementMinutes() );
          e.preventDefault();
        });
      }

      scope.readonlyInput = (angular.isDefined(attrs.readonlyInput)) ? scope.$eval(attrs.readonlyInput) : timepickerConfig.readonlyInput;
      if ( ! scope.readonlyInput ) {

        var invalidate = function(invalidHours, invalidMinutes) {
          ngModel.$setViewValue( null );
          ngModel.$setValidity('time', false);
          if (angular.isDefined(invalidHours)) {
            scope.invalidHours = invalidHours;
          }
          if (angular.isDefined(invalidMinutes)) {
            scope.invalidMinutes = invalidMinutes;
          }
        };

        scope.updateHours = function() {
          var hours = getHoursFromTemplate();

          if ( angular.isDefined(hours) ) {
            selected.setHours( hours );
            refresh( 'h' );
          } else {
            invalidate(true);
          }
        };

        hoursInputEl.bind('blur', function(e) {
          if ( !scope.validHours && scope.hours < 10) {
            scope.$apply( function() {
              scope.hours = pad( scope.hours );
            });
          }
        });

        scope.updateMinutes = function() {
          var minutes = getMinutesFromTemplate();

          if ( angular.isDefined(minutes) ) {
            selected.setMinutes( minutes );
            refresh( 'm' );
          } else {
            invalidate(undefined, true);
          }
        };

        minutesInputEl.bind('blur', function(e) {
          if ( !scope.invalidMinutes && scope.minutes < 10 ) {
            scope.$apply( function() {
              scope.minutes = pad( scope.minutes );
            });
          }
        });
      } else {
        scope.updateHours = angular.noop;
        scope.updateMinutes = angular.noop;
      }

      ngModel.$render = function() {
        var date = ngModel.$modelValue ? new Date( ngModel.$modelValue ) : null;

        if ( isNaN(date) ) {
          ngModel.$setValidity('time', false);
          $log.error('Timepicker directive: "ng-model" value must be a Date object, a number of milliseconds since 01.01.1970 or a string representing an RFC2822 or ISO 8601 date.');
        } else {
          if ( date ) {
            selected = date;
          }
          makeValid();
          updateTemplate();
        }
      };

      // Call internally when we know that model is valid.
      function refresh( keyboardChange ) {
        makeValid();
        ngModel.$setViewValue( new Date(selected) );
        updateTemplate( keyboardChange );
      }

      function makeValid() {
        ngModel.$setValidity('time', true);
        scope.invalidHours = false;
        scope.invalidMinutes = false;
      }

      function updateTemplate( keyboardChange ) {
        var hours = selected.getHours(), minutes = selected.getMinutes();

        if ( scope.showMeridian ) {
          hours = ( hours === 0 || hours === 12 ) ? 12 : hours % 12; // Convert 24 to 12 hour system
        }
        scope.hours =  keyboardChange === 'h' ? hours : pad(hours);
        scope.minutes = keyboardChange === 'm' ? minutes : pad(minutes);
        scope.meridian = selected.getHours() < 12 ? meridians[0] : meridians[1];
      }

      function addMinutes( minutes ) {
        var dt = new Date( selected.getTime() + minutes * 60000 );
        selected.setHours( dt.getHours(), dt.getMinutes() );
        refresh();
      }

      scope.incrementHours = function() {
        addMinutes( hourStep * 60 );
      };
      scope.decrementHours = function() {
        addMinutes( - hourStep * 60 );
      };
      scope.incrementMinutes = function() {
        addMinutes( minuteStep );
      };
      scope.decrementMinutes = function() {
        addMinutes( - minuteStep );
      };
      scope.toggleMeridian = function() {
        addMinutes( 12 * 60 * (( selected.getHours() < 12 ) ? 1 : -1) );
      };




      // from date
      //
//      var timepickerCtrl = ctrls[0], ngModel = ctrls[1];

//      if (!ngModel) {
//        return; // do nothing if no ng-model
//      }

      // Configuration parameters
//      var mode = 0, selected = new Date(), showWeeks = timepickerConfig.showWeeks;

//      if (attrs.showWeeks) {
//        scope.$parent.$watch($parse(attrs.showWeeks), function(value) {
//          showWeeks = !! value;
//          updateShowWeekNumbers();
//        });
//      } else {
//        updateShowWeekNumbers();
//      }

//      if (attrs.min) {
//        scope.$parent.$watch($parse(attrs.min), function(value) {
//          timepickerCtrl.minDate = value ? new Date(value) : null;
//          refill();
//        });
//      }
//      if (attrs.max) {
//        scope.$parent.$watch($parse(attrs.max), function(value) {
//          timepickerCtrl.maxDate = value ? new Date(value) : null;
//          refill();
//        });
//      }

      function updateShowWeekNumbers() {
//        scope.showWeekNumbers = mode === 0 && showWeeks;
      }

      // Split array into smaller arrays
      function split(arr, size) {
//        var arrays = [];
//        while (arr.length > 0) {
//          arrays.push(arr.splice(0, size));
//        }
//        return arrays;
      }

      function refill( updateSelected ) {
//        var date = null, valid = true;
//
//        if ( ngModel.$modelValue ) {
//          date = new Date( ngModel.$modelValue );
//
//          if ( isNaN(date) ) {
//            valid = false;
//            $log.error('Datepicker directive: "ng-model" value must be a Date object, a number of milliseconds since 01.01.1970 or a string representing an RFC2822 or ISO 8601 date.');
//          } else if ( updateSelected ) {
//            selected = date;
//          }
//        }
//        ngModel.$setValidity('date', valid);
//
////        var currentMode = timepickerCtrl.modes[mode], data = currentMode.getVisibleDates(selected, date);
////        angular.forEach(data.objects, function(obj) {
////          obj.disabled = timepickerCtrl.isDisabled(obj.date, mode);
////        });
////
////        ngModel.$setValidity('date-disabled', (!date || !timepickerCtrl.isDisabled(date)));
//
//        scope.rows = split(data.objects, currentMode.split);
//        scope.labels = data.labels || [];
//        scope.title = data.title;
      }

      function setMode(value) {
//        mode = value;
//        updateShowWeekNumbers();
//        refill();
      }

      ngModel.$render = function() {
//        refill( true );
      };

      scope.select = function( date ) {
//        if ( mode === 0 ) {
//          var dt = new Date( ngModel.$modelValue );
//          dt.setFullYear( date.getFullYear(), date.getMonth(), date.getDate() );
//          ngModel.$setViewValue( dt );
//          refill( true );
//        } else {
//          selected = date;
//          setMode( mode - 1 );
//        }
      };
//      scope.move = function(direction) {
//        var step = timepickerCtrl.modes[mode].step;
//        selected.setMonth( selected.getMonth() + direction * (step.months || 0) );
//        selected.setFullYear( selected.getFullYear() + direction * (step.years || 0) );
//        refill();
//      };
//      scope.toggleMode = function() {
//        setMode( (mode + 1) % timepickerCtrl.modes.length );
//      };
//      scope.getWeekNumber = function(row) {
//        return ( mode === 0 && scope.showWeekNumbers && row.length === 7 ) ? getISO8601WeekNumber(row[0].date) : null;
//      };
//
//      function getISO8601WeekNumber(date) {
//        var checkDate = new Date(date);
//        checkDate.setDate(checkDate.getDate() + 4 - (checkDate.getDay() || 7)); // Thursday
//        var time = checkDate.getTime();
//        checkDate.setMonth(0); // Compare with Jan 1
//        checkDate.setDate(1);
//        return Math.floor(Math.round((time - checkDate) / 86400000) / 7) + 1;
//      }
    }
  };
}])

.constant('timepickerPopupConfig', {
  dateFormat: 'dd-MM-yyyy',
  closeOnTimeSelection: true
})

.directive('timepickerPopup', ['$compile', '$parse', '$document', '$position', 'dateFilter', 'timepickerPopupConfig',
function ($compile, $parse, $document, $position, dateFilter, timepickerPopupConfig) {
  return {
    restrict: 'EA',
    require: 'ngModel',
    link: function(originalScope, element, attrs, ngModel) {
//      scope.hours = ngModel.getHours();
//      scope.minutes = ngModel.getMinutes();

      var closeOnTimeSelection = angular.isDefined(attrs.closeOnTimeSelection) ? scope.$eval(attrs.closeOnTimeSelection) : timepickerPopupConfig.closeOnTimeSelection;
      var dateFormat = attrs.datepickerPopup || timepickerPopupConfig.dateFormat;

     // create a child scope for the datepicker directive so we are not polluting original scope
      var scope = originalScope.$new();
      originalScope.$on('$destroy', function() {
        scope.$destroy();
      });

      var getIsOpen, setIsOpen;
      if ( attrs.isOpen ) {
        getIsOpen = $parse(attrs.isOpen);
        setIsOpen = getIsOpen.assign;

        originalScope.$watch(getIsOpen, function updateOpen(value) {
          scope.isOpen = !! value;
        });
      }
      scope.isOpen = getIsOpen ? getIsOpen(originalScope) : false; // Initial state

      function setOpen( value ) {
        if (setIsOpen) {
          setIsOpen(originalScope, !!value);
        } else {
          scope.isOpen = !!value;
        }
      }

      var documentClickBind = function(event) {
        if (scope.isOpen && event.target !== element[0]) {
          scope.$apply(function() {
            setOpen(false);
          });
        }
      };

      var elementFocusBind = function() {
        scope.$apply(function() {
          setOpen( true );
        });
      };

      // popup element used to display calendar
      var popupEl = angular.element('<timepicker-popup-wrap ng-model="max">[[max]]<timepicker></timepicker></timepicker-popup-wrap>');
      popupEl.attr({
        'ng-model': 'myStartTime',
        'ng-change': 'dateSelection()'
      });
      var datepickerEl = popupEl.find('timepicker');
      if (attrs.datepickerOptions) {
        datepickerEl.attr(angular.extend({}, originalScope.$eval(attrs.datepickerOptions)));
      }

      // TODO: reverse from dateFilter string to Date object
      function parseDate(viewValue) {
        if (!viewValue) {
          ngModel.$setValidity('date', true);
          return null;
        } else if (angular.isDate(viewValue)) {
          ngModel.$setValidity('date', true);
          return viewValue;
        } else if (angular.isString(viewValue)) {
          var date = new Date(viewValue);
          if (isNaN(date)) {
            ngModel.$setValidity('date', false);
            return undefined;
          } else {
            ngModel.$setValidity('date', true);
            return date;
          }
        } else {
          ngModel.$setValidity('date', false);
          return undefined;
        }
      }
      ngModel.$parsers.unshift(parseDate);

      // Inner change
      scope.dateSelection = function() {
        ngModel.$setViewValue(scope.date);
        ngModel.$render();

        if (closeOnTimeSelection) {
          setOpen( false );
        }
      };

      element.bind('input change keyup', function() {
        scope.$apply(function() {
          updateCalendar();
        });
      });

      // Outter change
      ngModel.$render = function() {
        var date = ngModel.$viewValue ? dateFilter(ngModel.$viewValue, dateFormat) : '';
        element.val(date);

        updateCalendar();
      };

      function updateCalendar() {
        scope.date = ngModel.$modelValue;
        updatePosition();
      }

      function addWatchableAttribute(attribute, scopeProperty, datepickerAttribute) {
        if (attribute) {
          originalScope.$watch($parse(attribute), function(value){
            scope[scopeProperty] = value;
          });
          datepickerEl.attr(datepickerAttribute || scopeProperty, scopeProperty);
        }
      }
      addWatchableAttribute(attrs.min, 'min');
      addWatchableAttribute(attrs.max, 'max');
      if (attrs.showWeeks) {
        addWatchableAttribute(attrs.showWeeks, 'showWeeks', 'show-weeks');
      } else {
        scope.showWeeks = true;
        datepickerEl.attr('show-weeks', 'showWeeks');
      }
      if (attrs.dateDisabled) {
        datepickerEl.attr('date-disabled', attrs.dateDisabled);
      }

      function updatePosition() {
        scope.position = $position.position(element);
        scope.position.top = scope.position.top + element.prop('offsetHeight');
      }

      var documentBindingInitialized = false, elementFocusInitialized = false;
      scope.$watch('isOpen', function(value) {
        if (value) {
          updatePosition();
          $document.bind('click', documentClickBind);
          if(elementFocusInitialized) {
            element.unbind('focus', elementFocusBind);
          }
          element[0].focus();
          documentBindingInitialized = true;
        } else {
          if(documentBindingInitialized) {
            $document.unbind('click', documentClickBind);
          }
          element.bind('focus', elementFocusBind);
          elementFocusInitialized = true;
        }

        if ( setIsOpen ) {
          setIsOpen(originalScope, value);
        }
      });

      var $setModelValue = $parse(attrs.ngModel).assign;

      scope.today = function() {
//        $setModelValue(originalScope, new Date());
      };
      scope.clear = function() {
//        $setModelValue(originalScope, null);
      };

      element.after($compile(popupEl)(scope));
    }
  };
}])

.directive('timepickerPopupWrap', [function() {
  return {
    restrict:'E',
    replace: true,
    transclude: true,
    templateUrl: 'timepopup.tpl',
    link:function (scope, element, attrs) {
      element.bind('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
      });
    }
  };
}])

.directive('timeDisplay', [function() {
	return {
	  require: 'ngModel',
	  link: function(scope, element, attrs, ngModelController) {
		ngModelController.$parsers.push(function(data) {
		  //convert data from view format to model format
		  return data; //converted
		});

		ngModelController.$formatters.push(function(data) {
		  //convert data from model format to view format
		  return data; //converted
		});
	  }
	}
}]);
