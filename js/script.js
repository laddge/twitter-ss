function action() {
    document.getElementById('msg').innerHTML = '';
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
            let msg = 'まだ大丈夫';
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
                    msg = 'ツイ廃ですね';
                } else if (n >= 70) {
                    output.classList.remove('text-warning');
                    output.classList.add('text-danger');
                    msg = '(=_=;';
                }
                output.innerHTML = (String(n) + '0').substr(0, 4);
                if (n >= ss) {
                    setTimeout(() => {
                        document.getElementById('msg').innerHTML = msg;
                        setTimeout(() => {
                            document.getElementById('msg').innerHTML += '<br>' + String(d.twh).substr(0, 4) + ' ツイート/h';
                            setTimeout(() => {
                                document.getElementById('msg').innerHTML += '<br>平均: ' + String(d.ave).substr(0, 4) + ' ツイート/h';
                                setTimeout(() => {
                                    document.getElementById('msg').innerHTML += '<br>標準偏差: ' + String(d.std).substr(0, 4);
                                    setTimeout(() => {
                                        document.getElementById('msg').innerHTML += '<br><a href="https://twitter.com/intent/tweet?text=' + screen_name + 'さんのツイ廃偏差値は ' + output.innerHTML + ' です%0D%0A%23ツイ廃偏差値%0D%0Ahttps://twss.laddge.net/" target="_blank"><div class="btn btn-outline-dark"><i class="bi-twitter"></i> 結果をシェア！</div></a>';
                                    }, 300);
                                }, 300);
                            }, 300);
                        }, 300);
                    }, 500);
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
