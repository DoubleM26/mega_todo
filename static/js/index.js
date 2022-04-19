function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

var jwtoken = getCookie("jwt")

const form = document.getElementById("task_create")
form.addEventListener("keydown", (event) => {
    if (event.code === "Enter") {
        form.submit()
    }
})

const task_search = document.getElementById("search_task")
task_search.addEventListener('click', () => {
    search.addEventListener("search", (event) => {
        const href = window.location.href.split("/")
            console.log(href)
            if (search.value) {
                if (href[3] === "complete_task") {
                    window.location.replace(href.slice(0, 3).join("/") + "/" + "complete_tasks" + "/" + search.value)
                } else if (href[3] === "task") {
                    window.location.replace(href.slice(0, 3).join("/") + "/" + "todo" + "/" + search.value)
                } else {
                    window.location.replace(href.slice(0, 4).join("/") + "/" + search.value)
                }
            } else {
                if (href[3] === "complete_task") {
                    window.location.replace(href.slice(0, 3).join("/") + "/" + "complete_tasks")
                } else if (href[3] === "task") {
                    window.location.replace(href.slice(0, 3).join("/") + "/" + "todo")
                } else {
                    window.location.replace(href.slice(0, 4).join("/"))
                }
            }
    })
})