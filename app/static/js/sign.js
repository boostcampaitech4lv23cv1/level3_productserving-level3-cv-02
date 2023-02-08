
// sign up
function signUp(e) {
    debugger;
    const user_password = document.getElementById('user_password');
    const password_check = document.getElementById('password_check');

    if (user_password.value !== password_check.value) {
        alert('패스워드 및 확인 패스워드가 일치하지 않습니다.');
        return false;
    }
    else {
        document.form_ex.submit();
    }
}