var transformDjangoRestResponse = function(data, headers){
	try {
        var jsonObject = angular.fromJson(data); // verify that json is valid
        return jsonObject.results;
    }
    catch (e) {
        console.log("did not receive valid Json: " + e)
    }
    return {};
}
angular.module('Models', ['ngResource'])
.factory('Note', ['$resource', function ($resource) {
  return $resource('/api/notes/:id/', {id:'@id'}, {
    query: { method: 'GET', isArray:true, transformResponse:transformDjangoRestResponse }, //, transformResponse:transformDjangoRestResponse
    save : { method : 'PUT'},
    create : { method : 'POST'},
    remove : { method : 'DELETE' }
  });
}]);

