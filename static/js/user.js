console.log('User.js working')

const onSubmit = (e) => {
    const form = new FormData(e.target);
    const name = form.get("name");
    console.log(name);
    return false
};