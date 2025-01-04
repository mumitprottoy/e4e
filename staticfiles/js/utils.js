const slideHorizontally = (id) => {
    element = document.getElementById(id);
    element.style.left = {
        '-100%': '0%',
        '0%': '-100%'
    }[element.style.left];
    console.log('slided');
}

const toggleVisibility = _id => {
    const displayMap = {'block': 'none', 'none': 'block'};
    const element = document.getElementById(_id);
    element.style.display = displayMap[element.style.display];
}

const togglePasswordVisibility = (form_id, pwd_name='password', conf_pwd_name='confirm_password') => {
    const form = document.getElementById(form_id);
    const type_map = {'password': 'text', 'text': 'password'};
    form[pwd_name].type = type_map[form[pwd_name].type];
    form[conf_pwd_name].type = type_map[form[conf_pwd_name].type];
}


const toggleMaxHeight = _id => {
    const maxHeightMap = {'0px': '99999px', '99999px': '0px'};
    const element = document.getElementById(_id);
    element.style.maxHeight = maxHeightMap[element.style.maxHeight];
}