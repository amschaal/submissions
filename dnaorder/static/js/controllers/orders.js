angular.module("dnaorder",["ngTable"])
.controller("SubmissionsController", ['$scope', 'DRFNgTableParams','NgTableParams',function($scope, DRFNgTableParams,NgTableParams) {
	this.tableParams = DRFNgTableParams('/api/submissions/',{sorting: { submitted: "desc" },filter:{}});
//	var data = [{id:'1',name:'One'},{id:'2',name:'Two'},{id:'3',name:'Three'}];
//	this.tableParams = NgTableParams({},{dataset:data});
	console.log($scope.tableParams);
	this.init = function(){
		
	}
 }]);