var ahs= angular.module("angularhotschema", ['Models']);
angular.module('main').requires.push("angularhotschema")
ahs.directive('hotSchemaTable', function() {
	return {
		restrict: 'AE',
//		templateUrl: '/static/templates/notes_container.html',
		scope: {
			bind: '='
		},
		controller: function ($scope,$rootScope) {
			console.log('testing schema');
			console.log('hot',$scope.hotEl);
			//var hst = new HotSchemaTable($scope.hot, example_schemas.veggie);

		},
		link: function(scope, element, attrs, ctrl, transclude) {
	        var wrapper = angular.element('<div class="wrapper"></div>');
	        var hotEl = angular.element('<div></div>')[0];
	        console.log('hot el',hotEl);
	        element.after(wrapper);
	        wrapper.prepend(element);
	        wrapper.append(hotEl);
	        scope.hotEl = hotEl;
	        var hst = new HotSchemaTable(hotEl, example_schemas.veggie);
	        scope.$on("$destroy", function() {
	          wrapper.after(element);
	          wrapper.remove();
	        });
	      }
	}
});
