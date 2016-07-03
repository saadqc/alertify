/**
 * Created by Hp on 12/6/2015.
 */


var registrationApp = angular.module('registrationApp', [
]);

registrationApp.controller('RegisterCtrl', function ($scope) {

    $scope.register = function () {
        var form = angular.element(document.getElementById("reg_form"));

        //send form data
        Dajaxice.Registrations.register_user_form(function(data){
            if(data.message == "VALID"){
                form.submit();
            }
            else{
                document.getElementById("error").innerHTML = 'Invalid Form';
            }
        }, {'form': form.serializeForm(true)});
    }
});

registrationApp.controller('LoginCtrl', function ($scope) {
    $scope.login = function () {

        var form = angular.element(document.getElementById("login_form"));

        //send form data
        Dajaxice.Registrations.login_user_form(function (data) {

            if (data.message == "VALID") {
                form.submit();
            }
            else {
                $('#error').css('display', 'block');
            }
        }, {'form': form.serializeForm(true)});
    }
});