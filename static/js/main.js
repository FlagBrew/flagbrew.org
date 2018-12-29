angular.module('main', ['ngSanitize'])

function orderByDate(arr, dateProp) {
    return arr.slice().sort(function (b, a) {
      return a[dateProp] < b[dateProp] ? -1 : 1;
    });
  }


angular.module('main').controller('twitterCtrl', function($scope, $http, $interval) {
    $scope.current = 0;
    $scope.tweets = []
    $http.get('/api/tweets').then(function(response) {
        $scope.tweets = response.data.data;
        $scope.tweets = orderByDate($scope.tweets, "created_at")
    });
    $scope.tweets = []
    $interval(function() {
        if (($scope.current + 1) >= $scope.tweets.length) {
            $scope.current = 0;
        } else {
            $scope.current = ++$scope.current;
        }
    }, 10000);

})
