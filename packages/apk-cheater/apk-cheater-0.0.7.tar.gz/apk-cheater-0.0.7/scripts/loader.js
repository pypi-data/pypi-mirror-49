'use strict';

console.log("apk-cheater hi");

var scan_address = [1,2];
rpc.exports = {
	scan: function(pattern) {
		console.log("[Scan] Starting.. ");
		scan_address = []; // remove history
		var ranges = Process.enumerateRangesSync({protection: 'r--', coalesce: true});
		var range;
		function processNext(){
			range = ranges.pop();
			if(!range){
				return false;
			}

			Memory.scan(range.base, range.size, pattern, { // Memory.scanSync is so slow..
				onMatch: function(address, size){
					scan_address.push(address);
				}, 
				onError: function(reason){
					// console.log('[!] There was an error scanning memory');
				}, 
				onComplete: function(){
					if (!processNext()){
						console.log("[Scan] All done");
					}
				}
			});

			return true;
		}
		processNext();
	},
	show: function() {
		console.log("Size: " + scan_address.length);
		if (scan_address.length <= 10) {
			for(var i=0; i<scan_address.length; i++){
				try{
					console.log(scan_address[i] + ": " + scan_address[i].readInt());
				} catch(err) {
				}
			}
		}
	},
	next: function(x) {
		var address;
		var temp = [];
		for (var idx in scan_address){
			try{
				address = scan_address[idx];
				if (x == address.readInt()){
					temp.push(address);
				}
			} catch(err) {
				// console.log(err);
			}
		}

		scan_address = temp; // replace
	},
	edit: function(x) {
		var address;
		for (var idx in scan_address){
			try{
				address = scan_address[idx];
				address.writeInt(x);
				console.log("Edit: " + address);
			} catch(err) {
				// console.log(err);
			}
		}
	},
};
