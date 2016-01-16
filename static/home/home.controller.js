(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['ItemService', '$rootScope', '$scope', '$http', 'FlashService'];
    function HomeController(ItemService, $rootScope, $scope, $http, FlashService) {
	    
	// create a book Object
  $scope.books = {};
   
   // We want to make a call and get
  // the books
  $http({
    method: 'GET',
    url: '/api/getBook'
  })
  .success(function (data, status, headers, config) {
    // See here, we are now assigning this books
    // to our existing model!
    $scope.books = data;
  })
  .error(function (data, status, headers, config) {
    // something went wrong :(
  });
  
  $scope.remove = function(book){
	   $http({
		  method: 'DELETE',
			url: '/api/DeleteBook'
 })
 .success(function (data, status, headers, config) { 
    $scope.books.splice($scope.books.indexOf(book),1);
})
 .error(function (data, status, headers, config) {
    // something went wrong :(
  });
  }
   
 
  
	
		

	    
      $scope.addbook = function (elem) {
		    
      // initial values
      $scope.error = false;
      $scope.disabled = true;

      // call register from service
      ItemService.addbook($scope.addBook.name, $scope.addBook.price)
        // handle success
        .success(function () {
		$scope.addBook = {};
				
	
          $scope.disabled = false;
          
        })
        // handle error
        .catch(function () {
          $scope.error = true;
          $scope.errorMessage = "Something went wrong!";
          $scope.disabled = false;
          $scope.addBook = {};
        });
	    
	    }
   


	    }

})();