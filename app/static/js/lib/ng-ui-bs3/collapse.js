angular.module('ui.bootstrap.collapse', ['ui.bootstrap.transition'])

  .directive('collapse', ['$transition', function ($transition, $timeout) {

    return {
      link: function (scope, element, attrs) {

        var initialAnimSkip = true;
        var currentTransition;

        function resetCurrentTransition() {
          currentTransition = undefined;
        }

        function doTransition(change) {
          if (currentTransition) {
            currentTransition.cancel();
          }
          (currentTransition = $transition(element, change)).then(resetCurrentTransition, resetCurrentTransition);
          return currentTransition;
        }

        function expand() {
          if (initialAnimSkip) {
            initialAnimSkip = false;
            element.removeClass('collapsing');
            element.addClass('collapse in');
            element.css({height: 'auto'});
          } else {
            element.removeClass('collapse').addClass('collapsing');
            doTransition({ height: element[0].scrollHeight + 'px' }).then(function () {
              element.removeClass('collapsing');
              element.addClass('collapse in');
              element.css({height: 'auto'});
            });
          }
        }

        function collapse() {
          if (initialAnimSkip) {
            element.removeClass('collapsing');
            element.addClass('collapse');
            element.css({height: 0});
          } else {
            // CSS transitions don't work with height: auto, so we have to manually change the height to a specific value
            element.css({ height: element[0].scrollHeight + 'px' });
            //trigger reflow so a browser relaizes that height was updated from auto to a specific value
            var x = element[0].offsetWidth;

            element.removeClass('collapse in').addClass('collapsing');

            doTransition({ height: 0 }).then(function () {
              element.removeClass('collapsing');
              element.addClass('collapse');
            });
          }
        }

        scope.$watch(attrs.collapse, function (shouldCollapse) {
          if (shouldCollapse) {
            collapse();
          } else {
            expand();
          }
          initialAnimSkip = false;
        });

      }
    };
  }]);

//TODO:
//- refactor to remove code duplication
//- corner cases - what happens in animation is in progress?
//- tests based on the DOM state / classes