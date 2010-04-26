function Petals(config){
	_config = {
		debug: false
	}
	$.extend(_config,config)
	
	log = function(msg){
		if (_config.debug){
			method = console.log || alert;
			return method(msg);
		}
	};
	
	MODE_DEFAULT = 'default';
	MODE_MEASURE = 'measure';
	MODE_SCALE = 'scale';
	
	_valid_modes = [MODE_DEFAULT, MODE_MEASURE, MODE_SCALE];
	_mode = null;
	
	function distance(x1,y1,x2,y2) {
			//find horizontal distance (x)
			var x = x2 - x1;
			//find vertical distance (y)
			var y = y2 - y1;
			//do calculation
			var hyp = Math.sqrt(x*x + y*y);
			return hyp;
	}
	
	
	_public = {
		setMode: function(mode){
			if(-1 == _valid_modes.indexOf(mode)){
				throw 'invalid mode: '+mode;
			} else {
				log('mode set: '+mode)
			}
		},
	};
	return _public;
}
