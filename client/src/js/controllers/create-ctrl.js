/**
 * Create Controller
 */

angular
    .module('RDash')
    .controller('CreateCtrl', ['$scope', CreateCtrl]);

function CreateCtrl($scope) {
    $scope.sendPost = function() {
        var data = {
            meta: {
                project: $scope.project,
                module: $scope.module,
                name: $scope.name
            },
            unikernel: $scope.unikernel,
            config: $scope.config,
            backend: $scope.backend
        };

        alert(JSON.stringify(data));

        //$http.post("/echo/json/", data).success(function(data, status) {
        //    $scope.hello = data;
        //})
    };
}