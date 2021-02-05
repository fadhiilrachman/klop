/*
 * Klop
 * Developed by Fadhiil Rachman
 */

const express = require('express')
const bodyparser = require('body-parser')
const app = express()

app.set('view engine', 'pug')
app.use(bodyparser.urlencoded({ extended: false }))
app.use(bodyparser.json())

// default port is 3000
let port=process.env.PORT || 3000;
let app_name='Klop';

let runKlopPython = function(pilihan) {
	return new Promise(function(resolve, reject) {

		const { spawn } = require('child_process');
		const pyprog = spawn('python', ['klopclass.py', pilihan]);

		pyprog.stdout.on('data', function(data) {
			resolve(data);
		});
		pyprog.stderr.on('data', (data) => {
			reject(data);
		});
	});
}

app.use('/assets', express.static(__dirname + '/assets'));

app.get('/', (req, res) => {
	res.status(200).render('index', { app_name: app_name, page_title: app_name + ': Your Digital Social Currency' });
})

app.get('/about-us', (req, res) => {
	res.status(200).render('about-us', { app_name: app_name, page_title: 'Tentang Kami - ' + app_name });
})

app.get('/api', (req, res) => {
	res.status(200).render('api', { app_name: app_name, page_title: 'API for Analyze - ' + app_name });
})

app.post('/api/analyze', (req, res) => {
	res.setHeader('Content-Type', 'application/json');
	if (!(req.body.u)) {
		res.status(400).json({ error: 'Username tidak ditemukan' });
	}
	req_u = req.body.u;
	runKlopPython(req_u).then(function(fromRunPy) {
		var data = fromRunPy.toString();
		data = data.replace("\r\n", "");
		data = JSON.parse(data);
		res.status(200).json(data);
	});
})

app.listen(port, () => console.log('[klop]', 'App listening to port ' + port))
