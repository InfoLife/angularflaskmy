(function () {
    'use strict';

    angular
        .module('app')
        .factory('ItemService', ItemService);

    ItemService.$inject = ['$http', '$q', '$timeout'];
    function ItemService($http, $q, $timeout) {

	var service = {};
	service.addbook = addbook;

        return service;

		 
	

function addbook(name, price){
	  var deferred = $q.defer();
	  
	  $http.post('/api/addbook', {name: name, price: price})
	  
	  .success(function(data){
		  if(data.result){
			  deferred.resolve();
		  } else {
			  deferred.reject();
		  }
	  })
	  .error(function (data) {
		  deferred.reject();
	  });
	  
	  return deferred.promise;
  }
  
  

  }
  
  
  
        // private functions

        function handleSuccess(res) {
            return res.data;
        }

        function handleError(error) {
            return function () {
                return { success: false, message: error };
            };
        }
	
	
	

  
  })();