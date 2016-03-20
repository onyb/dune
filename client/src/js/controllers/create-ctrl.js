/**
 * Create Controller
 */

angular
    .module('RDash')
    .controller('CreateCtrl', ['$scope', '$http', CreateCtrl]);

function CreateCtrl($scope, $http) {
    $scope.sendPost = function() {
        var payload = {
            meta: {
                project: $scope.project,
                module: $scope.module,
                name: $scope.name
            },
            unikernel: $scope.unikernel,
            config: $scope.config,
            backend: $scope.backend
        };

        $http.post("http://localhost:5000/api/unikernel/create", payload).success(function(data, status) {
            $scope.addAlert('success', '[code ' + data.code + '] [ID ' + data._id + '] ' + data.message);
        }).error(function(data, status) {
            $scope.addAlert('danger', '[code ' + data.code + '] ' + data.message);
        });
    };
}