var app = angular.module('main', ['ngSanitize']);

angular.module('main').controller('projectsCtrl', function($scope, $http){
    $http.get('https://cachebox.fm1337.com/api/repos').then(function(response){
        $scope.projects = response.data
    });
});


angular.module('main').controller('aboutCtrl', function($scope){
    $scope.people = [];
})
