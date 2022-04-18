let current_date

(function(selector) {
    initCalendar(document.querySelector(selector));

    function initCalendar(calendar) {
        let date = new Date(),
            showedYear = date.getFullYear(),
            showedMonth = date.getMonth();

        let currentMoment = {
            year: showedYear,
            month: showedMonth,
            date: date.getDate()
        };

        let dates = calendar.querySelector('.dates'),
            infoMonth = calendar.querySelector('.month-info'),
            infoYear = calendar.querySelector('.year-info');
        drawCalendar(showedYear, showedMonth, currentMoment, calendar);

        let prev = calendar.querySelector('.prev'),
            next = calendar.querySelector('.next');

        prev.addEventListener('click', function() {
            showedYear = getPrevYear(showedYear, showedMonth);
            showedMonth = getPrevMonth(showedMonth);

            drawCalendar(showedYear, showedMonth, currentMoment, calendar)
        });

        next.addEventListener('click', function() {
            showedYear = getNextYear(showedYear, showedMonth);
            showedMonth = getNextMonth(showedMonth);

            drawCalendar(showedYear, showedMonth, currentMoment, calendar)
        });

        function drawCalendar(showedYear, showedMonth, currentMoment, calendar) {
            current_date = [showedYear, showedMonth]
            drawDates(showedYear, showedMonth, dates);
            showInfo(showedYear, showedMonth, infoMonth, infoYear);
            showCurrentDate(showedYear, showedMonth, currentMoment, dates);
        }
    }

    function showCurrentDate(showedYear, showedMonth, currentMoment, dates) {
        if (
            showedYear == currentMoment['year'] &&
            showedMonth == currentMoment['month']
        ) {
            let tds = dates.querySelectorAll('td');
            for (let i = 0; i < tds.length; i++) {
                if (tds[i].innerHTML == currentMoment['date']) {
                    tds[i].classList.add('active');
                    break;
                }
            }
        }
    }

    function getPrevYear(year, month) {
        if (month == 0) {
            return year - 1;
        } else {
            return year;
        }
    }

    function getPrevMonth(month) {
        if (month == 0) {
            return 11;
        } else {
            return month - 1;
        }
    }

    function getNextYear(year, month) {
        if (month == 11) {
            return year + 1;
        } else {
            return year;
        }
    }

    function getNextMonth(month) {
        if (month == 11) {
            return 0;
        } else {
            return month + 1;
        }
    }

    function showInfo(year, month, elemMonth, elemYear) {
        elemMonth.innerHTML = getMonthName(month);
        elemYear.innerHTML = year;
    }

    function getMonthName(num) {
        let month = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]
        return month[num];
    }

    function drawDates(year, month, dates) {
        let arr = [],
            firstDateOfMonth = 1,
            lastDateOfMonth = getLastDayOfMonth(year, month);

        let unshiftElemsNum = getUnshiftElemsNum(year, month),
            pushElemsNum = getPushElemsNum(year, month);

        arr = createArr(firstDateOfMonth, lastDateOfMonth);
        arr = unshiftElems(unshiftElemsNum, '', arr);
        arr = pushElems(pushElemsNum, '', arr);
        arr = chunkArr(7, arr);

        createTable(arr, dates);
    }

    function createTable(arr, parent) {
        parent.innerHTML = '';
        for (let i = 0; i < arr.length; i++) {
            let tr = document.createElement('tr');

            for (let j = 0; j < arr[i].length; j++) {
                let td = document.createElement('td');
                td.innerHTML = arr[i][j];
                tr.appendChild(td);
            }
            parent.appendChild(tr);
        }
    }

    function createArr(from, to) {
        let arr = [];
        for (let i = from; i <= to; i++) {
            arr.push(i);
        }
        return arr;
    }

    function unshiftElems(num, elem, arr) {
        for (let i = 0; i < num; i++) {
            arr.unshift(elem);
        }
        return arr;
    }

    function unshiftElems(num, elem, arr) {
        for (let i = 0; i < num; i++) {
            arr.unshift(elem);
        }
        return arr;
    }

    function pushElems(num, elem, arr) {
        for (let i = 0; i < num; i++) {
            arr.push(elem);
        }
        return arr;
    }

    function getLastDayOfMonth(year, month) {
        let date = new Date(year, month + 1, 0);
        return date.getDate();
    }

    function getUnshiftElemsNum(year, month) {
        let jsDayNum = getFirstWeekDayOfMonthNum(year, month),
            realDayNum = getRealDayOfWeekNum(jsDayNum);

        return realDayNum - 1;

    }

    function getPushElemsNum(year, month) {
        let jsDayNum = getLastWeekDayOfMonthNum(year, month),
            realDayNum = getRealDayOfWeekNum(jsDayNum);

        return 7 - realDayNum;
    }

    function chunkArr(num, arr) {
        let result = [],
            chunk = [],
            iterCount = arr.length / num;

        for (let i = 0; i < iterCount; i++) {
            chunk = arr.splice(0, num);
            result.push(chunk);
        }
        return result;
    }

    function getRealDayOfWeekNum(jsNumOfDay) {
        if (jsNumOfDay == 0) {
            return 7;
        } else {
            return jsNumOfDay;
        }
    }

    function getFirstWeekDayOfMonthNum(year, month) {
        let date = new Date(year, month, 1);
        return date.getDay();
    }

    function getLastWeekDayOfMonthNum(year, month) {
        let date = new Date(year, month + 1, 0);
        return date.getDate();
    }
}('#calendar'));


function fix_num (num) {
    if (num < 10) {
        return "0" + num
    } else {
        return num
    }
}

function getCookie(name) {
            let matches = document.cookie.match(new RegExp(
                "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
            ));
            return matches ? decodeURIComponent(matches[1]) : undefined;
        }


document.getElementById('dates')
    .addEventListener('click', event => {
        if (event.target.tagName === 'TD') {
        let tds = document.querySelectorAll('td');
            tds.forEach(
                function(td) {
                    td.style.outline = '1px solid #fff'
                    td.style.outlineOffset = '-2px'
                });
            console.log(event.target.outerText, current_date)

            const calendar_title = document.getElementById('calendar_title')
            console.log(calendar_title)
            calendar_title.innerText = "Задачи на " +
                fix_num(event.target.outerText) + "." + fix_num(current_date[1] + 1) + "." + current_date[0]

            var jwtoken = getCookie("jwt")
            const date = [+event.target.outerText, current_date[1] + 1, current_date[0]]
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/api/tasks/by_date/' + date.join("-"), false);
            xhr.setRequestHeader('Authorization', 'Bearer ' + jwtoken);
            xhr.onload = function (event) {
                const data = JSON.parse(xhr.response)
                const container = document.getElementById('calendar_tasks')
                while (container.firstChild) {
                    container.removeChild(container.firstChild);
                }
                if (!data.length) {
                    container.insertAdjacentHTML('afterbegin', '<p style="margin-top: 12px">Кажется, тут пусто</p>')
                }
                for (const task of data) {
                    let div = document.createElement("div");
                    div.className = "task"
                    div.style.display = "flex"
                    container.appendChild(div)
                    if (task.complete) {
                        div.insertAdjacentHTML('afterbegin',
                        '<div class="form-check"><input class="form-check-input" checked type="checkbox" value="" id="' + task.id + '" style="cursor: pointer"></div>' +
                        '<label class="form-check-label" for="' + task.id + '" style="cursor: pointer">' + task.title + '</label>'
                        )
                    } else {
                        div.insertAdjacentHTML('afterbegin',
                        '<div class="form-check"><input class="form-check-input" type="checkbox" value="" id="' + task.id + '" style="cursor: pointer"></div>' +
                        '<label class="form-check-label" for="' + task.id + '" style="cursor: pointer">' + task.title + '</label>'
                        )
                    }


                    document.getElementById(task.id).addEventListener("click", (event) => {
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/api/tasks/change/' + task.id, false);
                    xhr.setRequestHeader('Authorization', 'Bearer ' + jwtoken);
                    xhr.send();
                })

                }
            }
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send();

            event.target.style.outline = '1px solid #4E68EF';
            event.target.style.outline = '-2px'
        }
    });