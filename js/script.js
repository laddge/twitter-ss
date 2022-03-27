function action() {
    const output = document.getElementById('output');
    output.classList.remove('display-1');
    output.classList.remove('fw-bold');
    output.classList.remove('text-success');
    output.classList.remove('text-warning');
    output.classList.remove('text-danger');
    output.innerHTML = 'Loading...';
    const screen_name = document.getElementById('screen_name').value;
    fetch('/u/' + screen_name)
        .then(r => {
            return r.json();
        })
        .then(d => {
            console.log(JSON.stringify(d));
            const ss = (d.twh - d.ave) / d.std * 10 + 50;
            output.classList.remove('text-warning');
            output.classList.remove('text-danger');
            output.classList.add('text-success');
            let n = 0;
            output.innerHTML = 0.0;
            output.classList.add('display-1');
            output.classList.add('fw-bold');
            const intervalId = setInterval(() => {
                if (n >= 50) {
                    output.classList.remove('text-success');
                    output.classList.add('text-warning');
                } else if (n >= 70) {
                    output.classList.remove('text-warning');
                    output.classList.add('text-danger');
                }
                output.innerHTML = (String(n) + '0').substr(0, 4);
                if (n >= ss) {
                    clearInterval(intervalId);
                }
                n = n + 0.1
            }, 10);
        })
        .catch(e => {
            output.innerHTML = 'Error!';
            console.log(e);
        });
}
