var app = angular.module('main', []);


app.controller('projectsCtrl', function($scope){
    $scope.projects = ["PKSM", "CheckPoint", "Testing"];
});