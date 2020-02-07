var ngrok = require('ngrok');
var util = require('util');
var secrets = require('../ansible-pi/secret_files/secret.json');


function _log(msg) {
	console.log(msg)
}

// log console messages
var console_msg = util.format('++ attempting to connect with ngrok');
_log(console_msg);

ngrok.connect({
	proto: 'tcp', // http|tcp|tls
	addr: 22, // port or network address
	auth: 'user:pwd', // http basic authentication for tunnel
	authtoken: secrets['NGROK_TOKEN']
	//subdomain: 'alex', // reserved tunnel name https://alex.ngrok.io,
	//authtoken: '12345' // your authtoken from ngrok.com
}, function (err, url) {
	_log('++ ngrok connected');
	_log(util.format('++ error: %j', err));
	_log(util.format('++ url: %s', url));
	// tcp://0.tcp.ngrok.io:12747
	var myRegexp = /tcp:\/\/(\d+\.tcp\.ngrok\.io)\:(\d+?)$/g;
	var match = myRegexp.exec(url);
	var cmd_str = util.format('ssh pi@%s -p%s', match[1], match[2]);
	_log('++ ' + cmd_str);
	twitter_helper.post_tweet(cmd_str);
});
